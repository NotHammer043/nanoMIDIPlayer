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
from modules.functions import mainFunctions

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
    "SPACE": " ",
    "ESC": "ESC",
    "RETURN": "ENTER"
}

def startGlobalListener():
    global listener
    if listener is None:
        def onPress(key):
            if ignoreKeyPress:
                return
            try:
                if hasattr(key, "char") and key.char:
                    keyStr = key.char.upper()
                else:
                    keyStr = str(key).replace("Key.", "").upper()
                    keyStr = specialKeyMap.get(keyStr, keyStr)
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
        mainFunctions.insertConsoleText(msg, False)
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

def tabBind(tab, app=None):
    logger.info(f"tabBind: {tab}")
    clearConsole()
    app = app or getApp()
    from modules.functions import midiPlayerFunctions
    from modules.functions import drumsMacroFunctions
    from modules.functions import midiHubFunctions
    from ui.midiHub import MidiHubTab
    from modules.functions import mainFunctions

    if osName == "Windows":
        if tab == 0:
            drumsMacroFunctions.unbindControls()
            midiPlayerFunctions.bindControls()
            MidiHubTab.searchEntry.unbind("<Return>")
        elif tab == 1:
            threading.Thread(target=mainFunctions.insertConsoleText, args=("Note: This will only work if your MIDI file specifically uses a drum instrument.", True)).start()
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
            threading.Thread(target=mainFunctions.insertConsoleText, args=("Note: This will only work if your MIDI file specifically uses a drum instrument.", True)).start()
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
        from modules.functions import mainFunctions
        mainFunctions.activeHotkeys.clear()
        for key in ["A", "B", "C", "D", "E", "F", "G",
                    "H", "I", "J", "K", "L", "M", "N",
                    "O", "P", "Q", "R", "S", "T", "U",
                    "V", "W", "X", "Y", "Z",
                    "SPACE", "ESC", "RETURN",
                    "F1", "F2", "F3", "F4", "F5",
                    "F6", "F7", "F8", "F9", "F10",
                    "F11", "F12"]:
            mainFunctions.activeHotkeys[key] = lambda k=key: onKeyPressShared(k)
        mainFunctions.startGlobalListener()

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
