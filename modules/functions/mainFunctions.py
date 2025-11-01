import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox
import textwrap
import threading
import time
import queue
import keyboard
import json
import mido
import sys
import os
import logging
import platform

from pynput import keyboard as pynputKeyboard
from modules import configuration
from ui import customTheme
from ui.midiPlayer import MidiPlayerTab
from ui.drumsMacro import DrumsMacroTab
from ui.midiToQWERTY import MidiToQwertyTab
from ui.settings import SettingsTab

osName = platform.system()
appInstance = None
logQueue = queue.Queue(maxsize=1)
logWorkedStarted = False
logCooldown = 0.05
hotkeyButtonActive = None
logger = logging.getLogger(__name__)

from pynput import keyboard as pynputKeyboard

listener = None
activeHotkeys = {}
ignoreKeyPress = False
specialKeyMap = {
    "SPACE": "SPACE",
    "ESC": "ESC",
    "ESCAPE": "ESC",
    "ENTER": "ENTER",
    "RETURN": "ENTER",
    "TAB": "TAB",
    "BACKSPACE": "BACKSPACE",
    "DELETE": "DELETE",
    "INSERT": "INSERT",
    "HOME": "HOME",
    "END": "END",
    "PAGE_UP": "PAGE_UP",
    "PAGE_DOWN": "PAGE_DOWN",

    "LEFT": "LEFT",
    "RIGHT": "RIGHT",
    "UP": "UP",
    "DOWN": "DOWN",

    "SHIFT_L": "LEFT SHIFT",
    "SHIFT_R": "RIGHT SHIFT",
    "SHIFT": "LEFT SHIFT",
    "CTRL_L": "LEFT CTRL",
    "CTRL_R": "RIGHT CTRL",
    "CONTROL": "LEFT CTRL",
    "ALT_L": "LEFT ALT",
    "ALT_R": "RIGHT ALT",
    "ALT": "LEFT ALT",
    "CMD": "CMD",
    "CMD_R": "CMD",

    "F1": "F1", "F2": "F2", "F3": "F3", "F4": "F4", "F5": "F5",
    "F6": "F6", "F7": "F7", "F8": "F8", "F9": "F9", "F10": "F10",
    "F11": "F11", "F12": "F12", "F13": "F13", "F14": "F14", "F15": "F15",

    "NUMPAD0": "NUMPAD0", "NUMPAD1": "NUMPAD1", "NUMPAD2": "NUMPAD2",
    "NUMPAD3": "NUMPAD3", "NUMPAD4": "NUMPAD4", "NUMPAD5": "NUMPAD5",
    "NUMPAD6": "NUMPAD6", "NUMPAD7": "NUMPAD7", "NUMPAD8": "NUMPAD8",
    "NUMPAD9": "NUMPAD9",
    "ADD": "NUMPAD+",
    "SUBTRACT": "NUMPAD-",
    "MULTIPLY": "NUMPAD*",
    "DIVIDE": "NUMPAD/",
    "DECIMAL": "NUMPAD.",

    "CAPS_LOCK": "CAPSLOCK",
    "CAPSLOCK": "CAPSLOCK",
    "NUM_LOCK": "NUMLOCK",
    "NUMLOCK": "NUMLOCK",
    "SCROLL_LOCK": "SCROLLLOCK",
    "SCROLLLOCK": "SCROLLLOCK"
}

def startGlobalListener():
    global listener
    if listener is None:
        def onPress(key):
            if ignoreKeyPress:
                return
            try:
                keyStr = None
                if hasattr(key, "char") and key.char:
                    keyStr = key.char.upper()

                else:
                    rawName = str(key).replace("Key.", "").replace(" ", "_").upper()
                    if rawName in ("CTRL", "CONTROL"):
                        rawName = "CTRL_L"
                    elif rawName == "SHIFT":
                        rawName = "SHIFT_L"
                    elif rawName == "ALT":
                        rawName = "ALT_L"

                    keyStr = specialKeyMap.get(rawName, rawName)

                if keyStr in activeHotkeys:
                    activeHotkeys[keyStr]()

            except Exception as e:
                logger.debug(f"onPress error: {e}")

        listener = pynputKeyboard.Listener(on_press=onPress)
        listener.daemon = True
        listener.start()

class ScrollableFrame(ctk.CTkScrollableFrame):
    def check_if_master_is_canvas(self, widget):
        if isinstance(widget, tk.Widget):
            return super().check_if_master_is_canvas(widget)
        return False

def registerApp(app):
    global appInstance
    appInstance = app

def getApp():
    return appInstance

def resourcePath(relativePath):
    if hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS
    else:
        basePath = os.path.abspath(".")
    return os.path.join(basePath, relativePath)

def logWorker():
    logger.debug("logWorker started")
    while True:
        try:
            msg = logQueue.get()
        except Exception as e:
            logger.error(f"logWorker error: {e}")
            continue
        insertConsoleText(msg, False)
        time.sleep(logCooldown)

def log(string):
    global logWorkedStarted
    if configuration.configData['appUI']['console']:
        if not logWorkedStarted:
            logger.debug("starting logWorker thread")
            threading.Thread(target=logWorker, daemon=True).start()
            logWorkedStarted = True
        try:
            if logQueue.full():
                try:
                    logQueue.get_nowait()
                except Exception as e:
                    logger.error(f"logQueue get_nowait error: {e}")
            logQueue.put_nowait(string)
        except Exception as e:
            logger.error(f"logQueue put_nowait error: {e}")

def insertConsoleText(text, ignoreConsoleCheck=False, app=None):
    logger.debug(text)
    app = app or getApp()

    if not (ignoreConsoleCheck or configuration.configData['appUI']['console']):
        return

    currentPage = getattr(app, "currentPage", 0) if app else 0
    if currentPage == 1:
        consoleLocation = DrumsMacroTab.consoleFrame
    elif currentPage == 3:
        consoleLocation = MidiToQwertyTab.consoleFrame
    else:
        consoleLocation = MidiPlayerTab.consoleFrame
    
    if app:
        if currentPage == 1:
            maxMessages = getattr(app, "maxDrumPlayerConsoleLog", 14)
        elif currentPage == 3:
            maxMessages = getattr(app, "maxMidiToQWERTYLog", 13)
        else:
            maxMessages = getattr(app, "maxMidiPlayerConsoleLog", 8)
    else:
        maxMessages = 15

    if app and (not hasattr(app, "logLabels") or app.logLabels is None):
        app.logLabels = []

    wrappedLines = []
    for line in text.split("\n"):
        wrappedLines.extend(
            textwrap.wrap(line, width=27, break_long_words=True, break_on_hyphens=False)
        )
    wrappedText = "\n".join(wrappedLines)

    def createLabel():
        logLabel = tk.Label(
            consoleLocation,
            text=wrappedText,
            fg=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"],
            bg=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ConsoleBackground"],
            font=customTheme.globalFont12,
            anchor="w",
            justify="left",
            wraplength=0,
        )
        logLabel.pack(anchor="sw", fill="x")

        if app:
            app.logLabels.append(logLabel)
            if len(app.logLabels) > maxMessages:
                oldLabel = app.logLabels.pop(0)
                try:
                    oldLabel.destroy()
                except Exception as e:
                    logger.error(f"destroy oldLabel error: {e}")

        if len(consoleLocation.winfo_children()) > 20:
            for widget in consoleLocation.winfo_children():
                try:
                    widget.destroy()
                except Exception as e:
                    logger.error(f"destroy widget error: {e}")

        consoleLocation.update_idletasks()

    consoleLocation.after(0, createLabel)

def clearConsole(app=None):
    logger.debug("clearConsole")
    app = app or getApp()
    currentPage = getattr(app, "currentPage", 0) if app else 0

    if currentPage == 1:
        consoleLocation = DrumsMacroTab.consoleFrame
    elif currentPage == 3:
        consoleLocation = MidiToQwertyTab.consoleFrame
    else:
        consoleLocation = MidiPlayerTab.consoleFrame

    for widget in consoleLocation.winfo_children():
        try:
            widget.destroy()
        except Exception as e:
            logger.error(f"clearConsole destroy widget error: {e}")
    if app and hasattr(app, "logLabels"):
        app.logLabels.clear()
    consoleLocation.update_idletasks()

def tabBind(tab):
    logger.info(f"tabBind: {tab}")
    clearConsole()
    from modules.functions import midiPlayerFunctions
    from modules.functions import drumsMacroFunctions
    from modules.functions import midiHubFunctions
    from ui.midiHub import MidiHubTab

    if osName == "Windows":
        if tab == 0:
            drumsMacroFunctions.unbindControls()
            midiPlayerFunctions.bindControls()
            MidiHubTab.searchEntry.unbind("<Return>")
        elif tab == 1:
            threading.Thread(target=insertConsoleText, args=("Note: This will only work if your MIDI file specifically uses a drum instrument.", True)).start()
            midiPlayerFunctions.unbindControls()
            drumsMacroFunctions.bindControls()
            MidiHubTab.searchEntry.unbind("<Return>")
        elif tab == 2:
            midiPlayerFunctions.unbindControls()
            drumsMacroFunctions.unbindControls()
            threading.Thread(target=midiHubFunctions.loadMidiData).start()
            MidiHubTab.searchEntry.bind("<Return>", midiHubFunctions.searchBar)
        else:
            MidiHubTab.searchEntry.unbind("<Return>")
            midiPlayerFunctions.unbindControls()
            drumsMacroFunctions.unbindControls()
    else:
        if tab == 0:
            midiPlayerFunctions.bindControls()
            MidiHubTab.searchEntry.unbind("<Return>")
        elif tab == 1:
            threading.Thread(target=insertConsoleText, args=("Note: This will only work if your MIDI file specifically uses a drum instrument.", True)).start()
            drumsMacroFunctions.bindControls()
            MidiHubTab.searchEntry.unbind("<Return>")
        elif tab == 2:
            midiPlayerFunctions.unbindControls()
            drumsMacroFunctions.unbindControls()
            threading.Thread(target=midiHubFunctions.loadMidiData).start()
            MidiHubTab.searchEntry.bind("<Return>", midiHubFunctions.searchBar)
        else:
            MidiHubTab.searchEntry.unbind("<Return>")
            midiPlayerFunctions.unbindControls()
            drumsMacroFunctions.unbindControls()

def setHotkey(keyType):
    logger.info(f"setHotkey: {keyType}")
    from modules.functions import midiPlayerFunctions
    from modules.functions import drumsMacroFunctions
    global hotkeyButtonActive, hotkeyHook
    hotkeyButtonActive = keyType
    hotkeyHook = None

    buttons = {
        'play': [MidiPlayerTab.playHotkeyButton, DrumsMacroTab.playHotkeyButton, SettingsTab.playHotkeyButton],
        'pause': [MidiPlayerTab.pauseHotkeyButton, DrumsMacroTab.pauseHotkeyButton, SettingsTab.pauseHotkeyButton],
        'stop': [MidiPlayerTab.stopHotkeyButton, DrumsMacroTab.stopHotkeyButton, SettingsTab.stopHotkeyButton],
        'speedup': [MidiPlayerTab.speedUpHotkeyButton, DrumsMacroTab.speedUpHotkeyButton, SettingsTab.speedUpHotkeyButton],
        'slowdown': [MidiPlayerTab.slowHotkeyButton, DrumsMacroTab.slowHotkeyButton, SettingsTab.slowHotkeyButton]
    }

    oldHotkey = configuration.configData["hotkeys"][keyType]
    midiPlayerFunctions.unbindControls()
    drumsMacroFunctions.unbindControls()

    for btnType, btnList in buttons.items():
        for btn in btnList:
            if btnType == keyType:
                btn.configure(text="...")
            else:
                btn.configure(state="disabled")

    def resetButtons():
        for btnList in buttons.values():
            for btn in btnList:
                btn.configure(state="normal")

    def finishHotkey(newHotkey):
        currentHotkeys = {k: v for k, v in configuration.configData["hotkeys"].items() if k != keyType}
        if newHotkey in currentHotkeys.values():
            for btn in buttons[keyType]:
                btn.configure(text=oldHotkey.upper(), state="normal")
            configuration.configData["hotkeys"][keyType] = oldHotkey
            with open(configuration.configPath, 'w') as configFile:
                json.dump(configuration.configData, configFile, indent=2)
            conflictAction = [k for k, v in currentHotkeys.items() if v == newHotkey][0]
            tkinter.messagebox.showinfo(title="Keybind Conflict", message=f"This keybind is in use!\n{conflictAction}: {newHotkey}", icon='warning')
        else:
            for btn in buttons[keyType]:
                btn.configure(text=newHotkey.upper(), state="normal")
            configuration.configData["hotkeys"][keyType] = newHotkey
            with open(configuration.configPath, 'w') as configFile:
                json.dump(configuration.configData, configFile, indent=2)

        global hotkeyButtonActive, hotkeyHook
        if osName == "Windows" and hotkeyHook:
            keyboard.unhook(hotkeyHook)
        hotkeyButtonActive = None
        resetButtons()

        app = getApp()
        if app.currentPage == 0:
            midiPlayerFunctions.bindControls()
        elif app.currentPage == 1:
            drumsMacroFunctions.bindControls()

    def onKeyPressWindows(event):
        if hotkeyButtonActive:
            finishHotkey(event.name)

    def onKeyPressShared(keyName):
        if hotkeyButtonActive:
            finishHotkey(keyName.lower())

    if osName == "Windows":
        hotkeyHook = keyboard.on_press(onKeyPressWindows)
    else:
        activeHotkeys.clear()
        supportedKeys = [
            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15",
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",

            "-", "=", "BACKSPACE", "`", "TAB", "[", "]", "ENTER", ";", "'", "\\", ",", ".", "/", 
            "LEFT SHIFT", "RIGHT SHIFT", "LEFT CTRL", "RIGHT CTRL", "CMD", 
            "LEFT ALT", "RIGHT ALT", "INSERT", "HOME", "PAGE_UP", "DELETE", "END", "PAGE_DOWN",

            "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
            "A", "S", "D", "F", "G", "H", "J", "K", "L",
            "Z", "X", "C", "V", "B", "N", "M",

            "NUMPAD1", "NUMPAD2", "NUMPAD3", "NUMPAD4", "NUMPAD5", 
            "NUMPAD6", "NUMPAD7", "NUMPAD8", "NUMPAD9",
            "NUMPAD*", "NUMPAD/", "NUMPAD.", "NUMPAD+", "NUMPAD-",

            "LEFT", "DOWN", "UP", "RIGHT",

            "CAPSLOCK",
            "NUMLOCK",
            "SCROLLLOCK",
        ]

        for key in supportedKeys:
            activeHotkeys[key] = lambda k=key: onKeyPressShared(k)
        startGlobalListener()

def refreshOutputDevices():
    logger.debug("refreshOutputDevices")
    from modules.functions import midiPlayerFunctions
    devices = mido.get_output_names()
    logger.debug(f"output devices: {devices}")
    loopbeDevice = next((device for device in devices if "LoopBe" in device), None)

    if not devices:
        devices = []
        defaultDevice = "No output devices"
        MidiPlayerTab.outputDeviceDropdown.configure(values=[defaultDevice])
        MidiPlayerTab.outputDeviceDropdown.set(defaultDevice)
        MidiPlayerTab.midiToggleSwitch.configure(state="disabled")
        configuration.configData["midiPlayer"]['useMIDIOutput'] = False
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
    else:
        defaultDevice = loopbeDevice if loopbeDevice else devices[0]
        MidiPlayerTab.outputDeviceDropdown.configure(values=devices)
        MidiPlayerTab.outputDeviceDropdown.set(defaultDevice)
        MidiPlayerTab.midiToggleSwitch.configure(state="normal")

    if not configuration.configData["midiPlayer"]['useMIDIOutput']:
        MidiPlayerTab.outputDeviceDropdown.configure(state="disabled")
    elif configuration.configData["midiPlayer"]['useMIDIOutput'] and devices:
        MidiPlayerTab.outputDeviceDropdown.configure(state="normal")

def refreshInputDevices():
    logger.debug("refreshInputDevices")
    devices = mido.get_input_names()
    logger.debug(f"input devices: {devices}")
    loopbeDevice = next((device for device in devices if "LoopBe" in device), None)
    previous = MidiToQwertyTab.inputDeviceDropdown.get() if hasattr(MidiToQwertyTab, "inputDeviceDropdown") else None

    if not devices:
        devices = []
        defaultDevice = "No input devices"
        MidiToQwertyTab.inputDeviceDropdown.configure(values=[defaultDevice], state="disabled")
        MidiToQwertyTab.inputDeviceDropdown.set(defaultDevice)
    else:
        defaultDevice = previous if previous in devices else (loopbeDevice if loopbeDevice else devices[0])
        MidiToQwertyTab.inputDeviceDropdown.configure(values=devices, state="normal")
        MidiToQwertyTab.inputDeviceDropdown.set(defaultDevice)

def playHotkeyCommand():
    logger.debug("playHotkeyCommand")
    setHotkey('play')

def pauseHotkeyCommand():
    logger.debug("pauseHotkeyCommand")
    setHotkey('pause')

def stopHotkeyCommand():
    logger.debug("stopHotkeyCommand")
    setHotkey('stop')

def speedUpHotkeyCommand():
    logger.debug("speedUpHotkeyCommand")
    setHotkey('speedup')

def slowHotkeyCommand():
    logger.debug("slowHotkeyCommand")
    setHotkey('slowdown')
