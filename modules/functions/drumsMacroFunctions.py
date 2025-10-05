import threading
import json
import customtkinter
import os
import platform
import datetime
import keyboard
import logging
from tkinter import filedialog
from mido import MidiFile

from pynput import keyboard as pynputKeyboard
from modules import configuration
from modules.functions import mainFunctions
from ui.drumsMacro import DrumsMacroTab
from ui.settings import SettingsTab
from ui import customTheme

logger = logging.getLogger(__name__)
osName = platform.system()

if osName == 'Windows':
    from modules.midiHandler import drumsWindows as midiHandler
elif osName == 'Darwin':
    from modules.midiHandler import drumsDarwin as midiHandler
elif osName == "Linux":
    from modules.midiHandler import drumsLinux as midiHandler

app = mainFunctions.getApp()

def selectFile():
    logger.info("selectFile called")
    try:
        DrumsMacroTab.midiPathDropdown.set("")
        unbindControls()
        stopPlayback()
        DrumsMacroTab.timelineIndicator.configure(text="0:00:00 / 0:00:00")
        DrumsMacroTab.playButton.configure(text="Play")

        filePath = filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid"), ("MIDI files", "*.midi")])
        logger.debug(f"filePath selected: {filePath}")
        if filePath:
            currentVAL = list(DrumsMacroTab.midiPathDropdown.cget("values"))
            if filePath not in currentVAL:
                currentVAL.append(filePath)
                DrumsMacroTab.midiPathDropdown.configure(values=currentVAL)

            DrumsMacroTab.midiPathDropdown.set(filePath)
            midiFile = MidiFile(filePath)

            timeLength = midiFile.length
            timelineText = (
                f"0:00:00 / {str(datetime.timedelta(seconds=int(timeLength)))}"
                if configuration.configData['appUI']['timestamp']
                else f"X:XX:XX / {str(datetime.timedelta(seconds=int(timeLength)))}"
            )
            DrumsMacroTab.timelineIndicator.configure(text=timelineText)

            configuration.configData['drumsMacro']['currentFile'] = filePath

            if 'midiList' not in configuration.configData['drumsMacro']:
                configuration.configData['drumsMacro']['midiList'] = []
            if filePath not in configuration.configData['drumsMacro']['midiList']:
                configuration.configData['drumsMacro']['midiList'].append(filePath)
            with open(configuration.configPath, 'w') as config_file:
                json.dump(configuration.configData, config_file, indent=2)

            bindControls()
    except Exception as e:
        logger.exception(f"selectFile error: {e}")

def loadSavedFile():
    logger.info("loadSavedFile called")
    try:
        midiList = configuration.configData['drumsMacro'].get('midiList', [])
        currentFile = configuration.configData['drumsMacro'].get('currentFile', '')

        midiList = [f for f in midiList if os.path.exists(f)]
        configuration.configData['drumsMacro']['midiList'] = midiList

        if currentFile and not os.path.exists(currentFile):
            currentFile = ""
            configuration.configData['drumsMacro']['currentFile'] = ""

        with open(configuration.configPath, 'w') as config_file:
            json.dump(configuration.configData, config_file, indent=2)

        entryValues = list(DrumsMacroTab.midiPathDropdown.cget("values"))
        for p in midiList:
            if p not in entryValues:
                entryValues.append(p)
        DrumsMacroTab.midiPathDropdown.configure(values=entryValues)

        if currentFile:
            if currentFile not in entryValues:
                entryValues.append(currentFile)
                DrumsMacroTab.midiPathDropdown.configure(values=entryValues)
            DrumsMacroTab.midiPathDropdown.set(currentFile)
            midiFileData = MidiFile(currentFile)
            totalTime = midiFileData.length
            timelineText = f"0:00:00 / {str(datetime.timedelta(seconds=int(totalTime)))}" if configuration.configData['appUI']['timestamp'] else f"X:XX:XX / {str(datetime.timedelta(seconds=int(totalTime)))}"
            DrumsMacroTab.timelineIndicator.configure(text=timelineText)
            logger.debug(f"loaded currentFile: {currentFile}")
            return

        if midiList:
            firstFile = midiList[0]
            DrumsMacroTab.midiPathDropdown.set(firstFile)
            configuration.configData['drumsMacro']['currentFile'] = firstFile
            with open(configuration.configPath, 'w') as config_file:
                json.dump(configuration.configData, config_file, indent=2)
            midiFileData = MidiFile(firstFile)
            totalTime = midiFileData.length
            timelineText = f"0:00:00 / {str(datetime.timedelta(seconds=int(totalTime)))}" if configuration.configData['appUI']['timestamp'] else f"X:XX:XX / {str(datetime.timedelta(seconds=int(totalTime)))}"
            DrumsMacroTab.timelineIndicator.configure(text=timelineText)
            logger.debug(f"loaded firstFile: {firstFile}")
            return

        DrumsMacroTab.midiPathDropdown.set("None")
        DrumsMacroTab.timelineIndicator.configure(text="0:00:00 / 0:00:00")
        logger.debug("no saved files found")
    except Exception as e:
        logger.exception(f"loadSavedFile error: {e}")

def switchMidiEvent(event=None):
    logger.info("switchMidiEvent called")
    try:
        midiFile = DrumsMacroTab.midiPathDropdown.get()
        configuration.configData['drumsMacro']['currentFile'] = midiFile
        with open(configuration.configPath, 'w') as file:
            json.dump(configuration.configData, file, indent=2)

        midiFileData = MidiFile(midiFile)
        totalTime = midiFileData.length
        timelineText = f"0:00:00 / {str(datetime.timedelta(seconds=int(totalTime)))}" if configuration.configData['appUI']['timestamp'] else f"X:XX:XX / {str(datetime.timedelta(seconds=int(totalTime)))}"
        DrumsMacroTab.timelineIndicator.configure(text=timelineText)
        bindControls()
        logger.debug(f"switched midi file to: {midiFile}")
    except Exception as e:
        logger.exception(f"switchMidiEvent error: {e}")

def bindControls():
    logger.info("bindControls called")
    try:
        unbindControls()
        playKey = configuration.configData["hotkeys"].get("play", "F1").upper()
        pauseKey = configuration.configData["hotkeys"].get("pause", "F2").upper()
        stopKey = configuration.configData["hotkeys"].get("stop", "F3").upper()
        speedUpKey = configuration.configData["hotkeys"].get("speedup", "F4").upper()
        slowDownKey = configuration.configData["hotkeys"].get("slowdown", "F5").upper()

        if osName == "Windows":
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(playKey.lower(), lambda e: startPlayback()))
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(pauseKey.lower(), lambda e: pausePlayback()))
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(stopKey.lower(), lambda e: stopPlayback()))
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(speedUpKey.lower(), lambda e: decreaseSpeed()))
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(slowDownKey.lower(), lambda e: increaseSpeed()))
        else:
            global listener, activeHotkeys

            activeHotkeys = {
                playKey: startPlayback,
                pauseKey: pausePlayback,
                stopKey: stopPlayback,
                speedUpKey: decreaseSpeed,
                slowDownKey: increaseSpeed
            }

            def onPress(key):
                try:
                    if hasattr(key, "char") and key.char:
                        keyStr = key.char.upper()
                    else:
                        keyStr = str(key).replace("Key.", "").upper()
                    if keyStr in activeHotkeys:
                        activeHotkeys[keyStr]()
                except Exception as e:
                    logger.debug(f"onPress error: {e}")

            if listener is None:
                listener = pynputKeyboard.Listener(on_press=onPress)
                listener.daemon = True
                listener.start()
        logger.debug("bindControls complete")
    except Exception as e:
        logger.exception(f"bindControls error: {e}")

def bindControls():
    try:
        playKey = configuration.configData["hotkeys"].get("play", "F1").upper()
        pauseKey = configuration.configData["hotkeys"].get("pause", "F2").upper()
        stopKey = configuration.configData["hotkeys"].get("stop", "F3").upper()
        speedUpKey = configuration.configData["hotkeys"].get("speedup", "F4").upper()
        slowDownKey = configuration.configData["hotkeys"].get("slowdown", "F5").upper()

        if osName == "Windows":
            unbindControls()
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(playKey.lower(), lambda e: startPlayback()))
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(pauseKey.lower(), lambda e: pausePlayback()))
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(stopKey.lower(), lambda e: stopPlayback()))
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(speedUpKey.lower(), lambda e: decreaseSpeed()))
            midiHandler.keyboardHandlers.append(keyboard.on_press_key(slowDownKey.lower(), lambda e: increaseSpeed()))
        else:
            from modules.functions import mainFunctions
            mainFunctions.activeHotkeys.clear()
            mainFunctions.activeHotkeys.update({
                playKey: startPlayback,
                pauseKey: pausePlayback,
                stopKey: stopPlayback,
                speedUpKey: decreaseSpeed,
                slowDownKey: increaseSpeed
            })
            mainFunctions.startGlobalListener()
    except Exception as e:
        logger.exception(f"bindControls error: {e}")

def unbindControls():
    try:
        if osName == "Windows":
            for h in list(midiHandler.keyboardHandlers):
                try:
                    keyboard.unhook(h)
                except Exception:
                    pass
            midiHandler.keyboardHandlers.clear()
        else:
            from modules.functions import mainFunctions
            mainFunctions.activeHotkeys.clear()
    except Exception as e:
        logger.exception(f"unbindControls error: {e}")

def playButton():
    logger.info("playButton called")
    try:
        if not app.isRunning:
            startPlayback()
        else:
            pausePlayback()
    except Exception as e:
        logger.exception(f"playButton error: {e}")

def startPlayback():
    logger.info("startPlayback called")
    try:
        midiFile = DrumsMacroTab.midiPathDropdown.get()
        logger.debug(f"startPlayback midiFile: {midiFile}")
        if not os.path.exists(midiFile):
            logger.warning("MIDI File does not exist.")
            threading.Thread(target=mainFunctions.insertConsoleText, args=("MIDI File does not exist.", True)).start()
            return

        if app and not app.isRunning:
            app.isRunning = True
            DrumsMacroTab.playButton.configure(
                text="Playing",
                fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PlayingColor"],
                hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PlayingColorHover"]
            )
            DrumsMacroTab.stopButton.configure(state="normal", fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["StopColor"])

            def updateTimeline(text):
                DrumsMacroTab.timelineIndicator.after(0, lambda: DrumsMacroTab.timelineIndicator.configure(text=text))

            midiHandler.startPlayback(midiFile, updateCallback=updateTimeline)
            logger.debug("midiHandler.startPlayback called")
    except Exception as e:
        logger.exception(f"startPlayback error: {e}")

def stopPlayback():
    logger.info("stopPlayback called")
    try:
        if not app.isRunning:
            return

        midiHandler.stopPlayback()
        app.isRunning = False
        bindControls()
        DrumsMacroTab.stopButton.configure(
            state="disabled",
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["StopColorDisabled"]
        )
        DrumsMacroTab.playButton.configure(
            text="Play",
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PlayColor"],
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PlayColorHover"]
        )

        midiFile = DrumsMacroTab.midiPathDropdown.get()
        if os.path.exists(midiFile):
            midiFileData = MidiFile(midiFile)
            totalTime = midiFileData.length
            timelineText = (
                f"0:00:00 / {str(datetime.timedelta(seconds=int(totalTime)))}"
                if configuration.configData['appUI']['timestamp']
                else f"X:XX:XX / {str(datetime.timedelta(seconds=int(totalTime)))}"
            )
            DrumsMacroTab.timelineIndicator.configure(text=timelineText)
        logger.debug("stopPlayback completed")
    except Exception as e:
        logger.exception(f"stopPlayback error: {e}")

def pausePlayback():
    logger.info("pausePlayback called")
    try:
        if not app.isRunning:
            return

        paused = False
        midiHandler.pausePlayback()
        paused = midiHandler.paused
        logger.debug(f"midiHandler.paused: {paused}")

        if paused:
            DrumsMacroTab.playButton.configure(
                text="Paused",
                fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PausedColor"],
                hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PausedColorHover"]
            )
        else:
            DrumsMacroTab.playButton.configure(
                text="Playing",
                fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PlayingColor"],
                hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PlayingColorHover"]
            )
        logger.debug("pausePlayback state updated")
    except Exception as e:
        logger.exception(f"pausePlayback error: {e}")

def setSpeed(speed):
    logger.info(f"setSpeed called with speed: {speed}")
    try:
        midiHandler.playbackSpeed = max(0.01, min(5.0, speed / 100.0))
        app.playbackSpeed = round(midiHandler.playbackSpeed * 100)

        DrumsMacroTab.speedSlider.set(app.playbackSpeed)
        DrumsMacroTab.speedValueEntry.delete(0, "end")
        DrumsMacroTab.speedValueEntry.insert(0, str(app.playbackSpeed))
        logger.debug(f"playbackSpeed set to: {midiHandler.playbackSpeed}, app.playbackSpeed: {app.playbackSpeed}")
    except Exception as e:
        logger.exception(f"setSpeed error: {e}")

def decreaseSpeed():
    logger.info("decreaseSpeed called")
    try:
        midiHandler.changeSpeed(-(configuration.configData["drumsMacro"]["decreaseSize"] / 100))
        app.playbackSpeed = round(midiHandler.playbackSpeed * 100)

        DrumsMacroTab.speedSlider.set(app.playbackSpeed)
        DrumsMacroTab.speedValueEntry.delete(0, "end")
        DrumsMacroTab.speedValueEntry.insert(0, str(app.playbackSpeed))
        logger.debug(f"decreased speed to: {midiHandler.playbackSpeed}")
    except Exception as e:
        logger.exception(f"decreaseSpeed error: {e}")

def increaseSpeed():
    logger.info("increaseSpeed called")
    try:
        midiHandler.changeSpeed(configuration.configData["drumsMacro"]["decreaseSize"] / 100)
        app.playbackSpeed = round(midiHandler.playbackSpeed * 100)

        DrumsMacroTab.speedSlider.set(app.playbackSpeed)
        DrumsMacroTab.speedValueEntry.delete(0, "end")
        DrumsMacroTab.speedValueEntry.insert(0, str(app.playbackSpeed))
        logger.debug(f"increased speed to: {midiHandler.playbackSpeed}")
    except Exception as e:
        logger.exception(f"increaseSpeed error: {e}")
