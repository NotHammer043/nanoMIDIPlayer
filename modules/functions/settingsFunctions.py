import customtkinter
import json
import ctypes
import sys
import logging
from modules import configuration
from modules.functions import mainFunctions
from ui.settings import SettingsTab
from ui.midiPlayer import MidiPlayerTab
from ui.drumsMacro import DrumsMacroTab
from ui.midiToQWERTY import MidiToQwertyTab
from ui import customTheme

logger = logging.getLogger(__name__)

switchTopMostvar = customtkinter.StringVar(value="off")
switchConsolevar = customtkinter.StringVar(value="off")
switchToolTipvar = customtkinter.StringVar(value="off")
switchTimestampvar = customtkinter.StringVar(value="off")
switchForceThemevar = customtkinter.StringVar(value="off")

try:
    switchTopMostvar.set("on" if configuration.configData.get('appUI', {}).get('topmost', False) else "off")
    switchConsolevar.set("on" if configuration.configData.get('appUI', {}).get('console', False) else "off")
    switchToolTipvar.set("on" if configuration.configData.get('appUI', {}).get('tooltip', False) else "off")
    switchTimestampvar.set("on" if configuration.configData.get('appUI', {}).get('timestamp', False) else "off")
    switchForceThemevar.set("on" if configuration.configData.get('appUI', {}).get('forceTheme', False) else "off")
except Exception as e:
    logger.exception("Error setting initial switch states")

def switchTopMost():
    try:
        configuration.configData['appUI']['topmost'] = switchTopMostvar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("TopMost switched to %s", switchTopMostvar.get())
    except Exception as e:
        logger.exception("Error in switchTopMost")

def switchTopMost():
    from modules.functions import mainFunctions
    app = mainFunctions.getApp()
    try:
        state = switchTopMostvar.get() == "on"
        app.wm_attributes("-topmost", state)

        configuration.configData['appUI']['topmost'] = state
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("TopMost switched to %s", state)
    except Exception as e:
        logger.exception("Error in switchTopMost: %s", e)

def switchConsole():
    try:
        configuration.configData['appUI']['console'] = switchConsolevar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("Console switched to %s", switchConsolevar.get())
    except Exception as e:
        logger.exception("Error in switchConsole")

def switchToolTip():
    try:
        configuration.configData['appUI']['tooltip'] = switchToolTipvar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("ToolTip switched to %s", switchToolTipvar.get())
    except Exception as e:
        logger.exception("Error in switchToolTip")

def switchTimestamp():
    try:
        configuration.configData['appUI']['timestamp'] = switchTimestampvar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("Timestamp switched to %s", switchTimestampvar.get())
    except Exception as e:
        logger.exception("Error in switchTimestamp")

def switchForceTheme():
    try:
        configuration.configData['appUI']['forceTheme'] = switchForceThemevar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("ForceTheme switched to %s", switchForceThemevar.get())
    except Exception as e:
        logger.exception("Error in switchForceTheme")

switchMidiCustomHoldLengthvar = customtkinter.StringVar(value="off")
switchMidiRandomFailvar = customtkinter.StringVar(value="off")
switchMidiLoopSongvar = customtkinter.StringVar(value="off")
switchMidiReleaseOnPausevar = customtkinter.StringVar(value="off")

try:
    switchMidiCustomHoldLengthvar.set("on" if configuration.configData.get('midiPlayer', {}).get('customHoldLength', {}).get('enabled', False) else "off")
    switchMidiRandomFailvar.set("on" if configuration.configData.get('midiPlayer', {}).get('randomFail', {}).get('enabled', False) else "off")
    switchMidiLoopSongvar.set("on" if configuration.configData.get('midiPlayer', {}).get('loopSong', {}) else "off")
    switchMidiReleaseOnPausevar.set("on" if configuration.configData.get('midiPlayer', {}).get('releaseOnPause', {}) else "off")
except Exception as e:
    logger.exception("Error setting MIDI switch states")

def switchMidiCustomHoldLength():
    try:
        configuration.configData["midiPlayer"]['customHoldLength']['enabled'] = switchMidiCustomHoldLengthvar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        midiCustomHoldLengthStatus()
        logger.info("MidiCustomHoldLength switched to %s", switchMidiCustomHoldLengthvar.get())
    except Exception as e:
        logger.exception("Error in switchMidiCustomHoldLength")

def switchMidiRandomFail():
    try:
        configuration.configData["midiPlayer"]['randomFail']['enabled'] = switchMidiRandomFailvar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        midiRandomFailStatus()
        logger.info("MidiRandomFail switched to %s", switchMidiRandomFailvar.get())
    except Exception as e:
        logger.exception("Error in switchMidiRandomFail")

def switchMidiLoopSong():
    try:
        configuration.configData['midiPlayer']['loopSong'] = switchMidiLoopSongvar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("MidiLoopSong switched to %s", switchMidiLoopSongvar.get())
    except Exception as e:
        logger.exception("Error in switchMidiLoopSong")

def switchMidiReleaseOnPause():
    try:
        configuration.configData['midiPlayer']['releaseOnPause'] = switchMidiReleaseOnPausevar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("MidiReleaseOnPause switched to %s", switchMidiReleaseOnPausevar.get())
    except Exception as e:
        logger.exception("Error in switchMidiReleaseOnPause")

def midiModuleSelect(value):
    try:
        configuration.configData["midiPlayer"]["inputModule"] = value
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("MidiModule selected: %s", value)
    except Exception as e:
        logger.exception("Error in midiModuleSelect")

def midiClearMidiList():
    try:
        from modules.functions import midiPlayerFunctions
        configuration.configData["midiPlayer"]["midiList"] = []
        configuration.configData["midiPlayer"]["currentFile"] = ""
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        MidiPlayerTab.filePathEntry.configure(values=[])
        MidiPlayerTab.filePathEntry.set("")
        midiPlayerFunctions.loadSavedFile()
        mainFunctions.log("MIDI list fully cleared")
        logger.info("MIDI list cleared")
    except Exception as e:
        logger.exception("Error in midiClearMidiList")

switchDrumsLoopSongvar = customtkinter.StringVar(value="off")
switchDrumsReleaseOnPausevar = customtkinter.StringVar(value="off")
switchDrumsCustomHoldLengthvar = customtkinter.StringVar(value="off")
switchDrumsRandomFailvar = customtkinter.StringVar(value="off")

try:
    switchDrumsLoopSongvar.set("on" if configuration.configData.get('drumsMacro', {}).get('loopSong', {}) else "off")
    switchDrumsReleaseOnPausevar.set("on" if configuration.configData.get('drumsMacro', {}).get('releaseOnPause', {}) else "off")
    switchDrumsCustomHoldLengthvar.set("on" if configuration.configData.get('drumsMacro', {}).get('customHoldLength', {}).get('enabled', False) else "off")
    switchDrumsRandomFailvar.set("on" if configuration.configData.get('midiPlayer', {}).get('randomFail', {}).get('enabled', False) else "off")
except Exception as e:
    logger.exception("Error setting drums switch states")

def switchDrumsLoopSong():
    try:
        configuration.configData['drumsMacro']['loopSong'] = switchDrumsLoopSongvar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("DrumsLoopSong switched to %s", switchDrumsLoopSongvar.get())
    except Exception as e:
        logger.exception("Error in switchDrumsLoopSong")

def switchDrumsReleaseOnPause():
    try:
        configuration.configData['drumsMacro']['releaseOnPause'] = switchDrumsReleaseOnPausevar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("DrumsReleaseOnPause switched to %s", switchDrumsReleaseOnPausevar.get())
    except Exception as e:
        logger.exception("Error in switchDrumsReleaseOnPause")

def switchDrumsCustomHoldLength():
    try:
        configuration.configData["drumsMacro"]['customHoldLength']['enabled'] = switchDrumsCustomHoldLengthvar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        drumsCustomHoldLengthStatus()
        logger.info("DrumsCustomHoldLength switched to %s", switchDrumsCustomHoldLengthvar.get())
    except Exception as e:
        logger.exception("Error in switchDrumsCustomHoldLength")

def switchDrumsRandomFail():
    try:
        configuration.configData["drumsMacro"]['randomFail']['enabled'] = switchDrumsRandomFailvar.get() == "on"
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        drumsRandomFailStatus()
        logger.info("DrumsRandomFail switched to %s", switchDrumsRandomFailvar.get())
    except Exception as e:
        logger.exception("Error in switchDrumsRandomFail")

def drumsModuleSelect(value):
    try:
        configuration.configData["drumsMacro"]["inputModule"] = value
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
        logger.info("DrumsModule selected: %s", value)
    except Exception as e:
        logger.exception("Error in drumsModuleSelect")

def drumsClearMidiList():
    try:
        from modules.functions import drumsMacroFunctions
        configuration.configData["drumsMacro"]["midiList"] = []
        configuration.configData["drumsMacro"]["currentFile"] = ""
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        DrumsMacroTab.midiPathDropdown.configure(values=[])
        DrumsMacroTab.midiPathDropdown.set("")
        drumsMacroFunctions.loadSavedFile()
        mainFunctions.log("MIDI list fully cleared")
        logger.info("Drums MIDI list cleared")
    except Exception as e:
        logger.exception("Error in drumsClearMidiList")

def midiCustomHoldLengthStatus():
    try:
        if configuration.configData["midiPlayer"]['customHoldLength']['enabled']:
            SettingsTab.midiNoteLengthSlider.configure(state="normal")
            SettingsTab.midiResetNoteLength.configure(state="normal")
            SettingsTab.midiNoteLengthEntry.configure(state="normal", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
            SettingsTab.midiNoteLengthLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
        else:
            SettingsTab.midiNoteLengthSlider.configure(state="disabled")
            SettingsTab.midiResetNoteLength.configure(state="disabled")
            SettingsTab.midiNoteLengthEntry.configure(state="disabled", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
            SettingsTab.midiNoteLengthLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
        logger.debug("MidiCustomHoldLength status updated")
    except Exception as e:
        logger.exception("Error in midiCustomHoldLengthStatus")

def drumsCustomHoldLengthStatus():
    try:
        if configuration.configData["drumsMacro"]['customHoldLength']['enabled']:
            SettingsTab.drumsNoteLengthSlider.configure(state="normal")
            SettingsTab.drumsResetNoteLength.configure(state="normal")
            SettingsTab.drumsNoteLengthEntry.configure(state="normal", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
            SettingsTab.drumsNoteLengthLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
        else:
            SettingsTab.drumsNoteLengthSlider.configure(state="disabled")
            SettingsTab.drumsResetNoteLength.configure(state="disabled")
            SettingsTab.drumsNoteLengthEntry.configure(state="disabled", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
            SettingsTab.drumsNoteLengthLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
        logger.debug("DrumsCustomHoldLength status updated")
    except Exception as e:
        logger.exception("Error in drumsCustomHoldLengthStatus")

def midiRandomFailStatus():
    try:
        if configuration.configData["midiPlayer"]['randomFail']['enabled']:
            SettingsTab.midiSpeedFailSlider.configure(state="normal")
            SettingsTab.midiResetSpeedFailButton.configure(state="normal")
            SettingsTab.midiSpeedFailEntry.configure(state="normal", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
            SettingsTab.midiSpeedFailLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
            SettingsTab.midiTransposeFailSlider.configure(state="normal")
            SettingsTab.midiResetTransposeFailButton.configure(state="normal")
            SettingsTab.midiTransposeFailEntry.configure(state="normal", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
            SettingsTab.midiTransposeFailLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
        else:
            SettingsTab.midiSpeedFailSlider.configure(state="disabled")
            SettingsTab.midiResetSpeedFailButton.configure(state="disabled")
            SettingsTab.midiSpeedFailEntry.configure(state="disabled", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
            SettingsTab.midiSpeedFailLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
            SettingsTab.midiTransposeFailSlider.configure(state="disabled")
            SettingsTab.midiResetTransposeFailButton.configure(state="disabled")
            SettingsTab.midiTransposeFailEntry.configure(state="disabled", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
            SettingsTab.midiTransposeFailLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
        logger.debug("MidiRandomFail status updated")
    except Exception as e:
        logger.exception("Error in midiRandomFailStatus")

def drumsRandomFailStatus():
    try:
        if configuration.configData["drumsMacro"]['randomFail']['enabled']:
            SettingsTab.drumsSpeedFailSlider.configure(state="normal")
            SettingsTab.drumsResetSpeedFailButton.configure(state="normal")
            SettingsTab.drumsSpeedFailEntry.configure(state="normal", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
            SettingsTab.drumsSpeedFailLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"])
        else:
            SettingsTab.drumsSpeedFailSlider.configure(state="disabled")
            SettingsTab.drumsResetSpeedFailButton.configure(state="disabled")
            SettingsTab.drumsSpeedFailEntry.configure(state="disabled", text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
            SettingsTab.drumsSpeedFailLabel.configure(text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"])
        logger.debug("DrumsRandomFail status updated")
    except Exception as e:
        logger.exception("Error in drumsRandomFailStatus")

def changeMidiNoteLength(value):
    try:
        val = float(value)
        configuration.configData["midiPlayer"]["customHoldLength"]["noteLength"] = val
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        logger.debug("MidiNoteLength changed to %s", val)
    except Exception as e:
        logger.exception("Error in changeMidiNoteLength")

def changeMidiSpeedFail(value):
    try:
        val = float(value)
        configuration.configData["midiPlayer"]["randomFail"]["speed"] = val
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        logger.debug("MidiSpeedFail changed to %s", val)
    except Exception as e:
        logger.exception("Error in changeMidiSpeedFail")

def changeMidiTransposeFail(value):
    try:
        val = float(value)
        configuration.configData["midiPlayer"]["randomFail"]["transpose"] = val
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        logger.debug("MidiTransposeFail changed to %s", val)
    except Exception as e:
        logger.exception("Error in changeMidiTransposeFail")

def changeMidiDecreaseSize(value):
    try:
        val = float(value)
        configuration.configData["midiPlayer"]["decreaseSize"] = val
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        logger.debug("MidiDecreaseSize changed to %s", val)
    except Exception as e:
        logger.exception("Error in changeMidiDecreaseSize")

def changeDrumsNoteLength(value):
    try:
        val = float(value)
        configuration.configData["drumsMacro"]["customHoldLength"]["noteLength"] = val
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        logger.debug("DrumsNoteLength changed to %s", val)
    except Exception as e:
        logger.exception("Error in changeDrumsNoteLength")

def changeDrumsSpeedFail(value):
    try:
        val = float(value)
        configuration.configData["drumsMacro"]["randomFail"]["speed"] = val
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        logger.debug("DrumsSpeedFail changed to %s", val)
    except Exception as e:
        logger.exception("Error in changeDrumsSpeedFail")

def changeDrumsDecreaseSize(value):
    try:
        val = float(value)
        configuration.configData["drumsMacro"]["decreaseSize"] = val
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        logger.debug("DrumsDecreaseSize changed to %s", val)
    except Exception as e:
        logger.exception("Error in changeDrumsDecreaseSize")

def changeMidiToQWERTYSustainCutoff(value):
    try:
        val = float(value)
        configuration.configData["midiToQwerty"]["sustainCutoff"] = val
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        logger.debug("MidiToQWERTYSustainCutoff changed to %s", val)
    except Exception as e:
        logger.exception("Error in changeMidiToQWERTYSustainCutoff")

def changeMidiToQWERTYNoteLength(value):
    try:
        val = float(value)
        configuration.configData["midiToQwerty"]["customHoldLength"]["noteLength"] = val
        with open(configuration.configPath, "w") as file:
            json.dump(configuration.configData, file, indent=2)
        logger.debug("MidiToQWERTYNoteLength changed to %s", val)
    except Exception as e:
        logger.exception("Error in changeMidiToQWERTYNoteLength")

controlSets = {}

def initControlSets():
    global controlSets
    try:
        from modules.functions import midiPlayerFunctions
        from modules.functions import drumsMacroFunctions
        controlSets = {
            "midiSpeedController": {
                "slider": MidiPlayerTab.speedSlider,
                "entry": MidiPlayerTab.speedValueEntry,
                "default": 100,
                "min": 1,
                "max": 500,
                "type": int,
                "onChange": lambda v: midiPlayerFunctions.setSpeed(v)
            },
            "drumsSpeedController": {
                "slider": DrumsMacroTab.speedSlider,
                "entry": DrumsMacroTab.speedValueEntry,
                "default": 100,
                "min": 1,
                "max": 500,
                "type": int,
                "onChange": lambda v: drumsMacroFunctions.setSpeed(v)
            },
            "midiToQWERTYSustainCutoff": {
                "slider": MidiToQwertyTab.sustainCutoffSlider,
                "entry": MidiToQwertyTab.sustainCutoffEntry,
                "default": 63,
                "min": 0,
                "max": 127,
                "type": int,
                "onChange": lambda v: changeMidiToQWERTYSustainCutoff(v)
            },
            "midiToQWERTYNoteLength": {
                "slider": MidiToQwertyTab.customHoldLengthSlider,
                "entry": MidiToQwertyTab.customHoldLengthEntry,
                "default": 0.1,
                "min": 0.1,
                "max": 10,
                "type": float,
                "onChange": lambda v: changeMidiToQWERTYNoteLength(v)
            },
            "midiNoteLength": {
                "slider": SettingsTab.midiNoteLengthSlider,
                "entry": SettingsTab.midiNoteLengthEntry,
                "default": 0.1,
                "min": 0.1,
                "max": 10,
                "type": float,
                "onChange": lambda v: changeMidiNoteLength(v)
            },
            "midiSpeedFail": {
                "slider": SettingsTab.midiSpeedFailSlider,
                "entry": SettingsTab.midiSpeedFailEntry,
                "default": 5,
                "min": 0,
                "max": 100,
                "type": int,
                "onChange": lambda v: changeMidiSpeedFail(v)
            },
            "midiTransposeFail": {
                "slider": SettingsTab.midiTransposeFailSlider,
                "entry": SettingsTab.midiTransposeFailEntry,
                "default": 5,
                "min": 0,
                "max": 100,
                "type": int,
                "onChange": lambda v: changeMidiTransposeFail(v)
            },
            "midiDecreaseSize": {
                "slider": SettingsTab.midiDecreaseSizeSlider,
                "entry": SettingsTab.midiDecreaseSizeEntry,
                "default": 5,
                "min": 1,
                "max": 100,
                "type": int,
                "onChange": lambda v: changeMidiDecreaseSize(v)
            },
            "drumsNoteLength": {
                "slider": SettingsTab.drumsNoteLengthSlider,
                "entry": SettingsTab.drumsNoteLengthEntry,
                "default": 0.1,
                "min": 0.1,
                "max": 10,
                "type": float,
                "onChange": lambda v: changeDrumsNoteLength(v)
            },
            "drumsSpeedFail": {
                "slider": SettingsTab.drumsSpeedFailSlider,
                "entry": SettingsTab.drumsSpeedFailEntry,
                "default": 5,
                "min": 0,
                "max": 100,
                "type": int,
                "onChange": lambda v: changeDrumsSpeedFail(v)
            },
            "drumsDecreaseSize": {
                "slider": SettingsTab.drumsDecreaseSizeSlider,
                "entry": SettingsTab.drumsDecreaseSizeEntry,
                "default": 5,
                "min": 1,
                "max": 100,
                "type": int,
                "onChange": lambda v: changeDrumsDecreaseSize(v)
            }
        }
        logger.info("Control sets initialized")
    except Exception as e:
        logger.exception("Error in initControlSets")

def resetControl(name, event=None):
    try:
        control = controlSets[name]
        valType = control["type"]
        value = valType(control["default"])
        if valType is float:
            value = round(value, 2)
            display = f"{value:.2f}"
        else:
            display = str(value)
        control["entry"].delete(0, "end")
        control["entry"].insert(0, display)
        control["slider"].set(value)
        control["onChange"](value)
        mainFunctions.log(f"{name} set to {display}")
        logger.info("Control %s reset to %s", name, display)
    except Exception as e:
        logger.exception("Error in resetControl for %s", name)

def updateFromSlider(name, value, event=None):
    try:
        control = controlSets[name]
        valType = control["type"]
        val = valType(value)
        if valType is float:
            val = round(val, 2)
        val = max(control["min"], min(val, control["max"]))
        if valType is float:
            display = f"{val:.2f}"
        else:
            display = str(val)
        control["entry"].delete(0, "end")
        control["entry"].insert(0, display)
        control["onChange"](val)
        mainFunctions.log(f"{name} set to {display}")
        logger.debug("Control %s updated from slider to %s", name, display)
    except Exception as e:
        logger.exception("Error in updateFromSlider for %s", name)

def updateFromEntry(name, event=None):
    try:
        control = controlSets[name]
        valType = control["type"]
        val = valType(control["entry"].get())
        if valType is float:
            val = round(val, 2)
        if control["min"] <= val <= control["max"]:
            control["slider"].set(val)
            control["onChange"](val)
            if valType is float:
                display = f"{val:.2f}"
            else:
                display = str(val)
            mainFunctions.log(f"{name} set to {display}")
            logger.debug("Control %s updated from entry to %s", name, display)
    except ValueError:
        logger.warning("Invalid value entered for control %s", name)
    except Exception as e:
        logger.exception("Error in updateFromEntry for %s", name)

def openConsole(event=None):
    try:
        ctypes.windll.kernel32.AllocConsole()
        sys.stdout = open('CONOUT$', 'w')
        sys.stderr = open('CONOUT$', 'w')
        sys.stdin = open('CONIN$', 'r')
        print("created output.")
        logger.info("Console opened")
    except Exception as e:
        logger.exception("Error opening console")

def closeConsole(event=None):
    try:
        ctypes.windll.kernel32.FreeConsole()
        sys.stdout.close()
        sys.stderr.close()
        sys.stdin.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdin = sys.__stdin__
        print("closed output.")
        logger.info("Console closed")
    except Exception as e:
        logger.exception("Error closing console")