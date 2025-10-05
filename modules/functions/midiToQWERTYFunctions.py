import json
import customtkinter
import platform
import threading
import logging

from modules import configuration
from modules.functions import mainFunctions
from ui import customTheme

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

osName = platform.system()

if osName == 'Windows':
    from modules.midiHandler import midiToQWERTYWindows as midiHandler
elif osName == 'Darwin':
    from modules.midiHandler import midiToQWERTYDarwin as midiHandler
elif osName == "Linux":
    from modules.midiHandler import midiToQWERTYLinux as midiHandler
    
app = mainFunctions.getApp()

switchSustainvar = customtkinter.StringVar(value="off")
switchNoDoublesvar = customtkinter.StringVar(value="off")
switchVelocityvar = customtkinter.StringVar(value="off")
switch88Keysvar = customtkinter.StringVar(value="off")
switchCustomHoldLengthvar = customtkinter.StringVar(value="off")

switchSustainvar.set("on" if configuration.configData.get('midiToQwerty', {}).get('sustain', False) else "off")
switchNoDoublesvar.set("on" if configuration.configData.get('midiToQwerty', {}).get('noDoubles', False) else "off")
switchVelocityvar.set("on" if configuration.configData.get('midiToQwerty', {}).get('velocity', False) else "off")
switch88Keysvar.set("on" if configuration.configData.get('midiToQwerty', {}).get('88Keys', False) else "off")
switchCustomHoldLengthvar.set("on" if configuration.configData.get('midiToQwerty', {}).get('customHoldLength', {}).get('enabled', False) else "off")

def switchSustain():
    try:
        configuration.configData['midiToQwerty']['sustain'] = switchSustainvar.get() == "on"
        with open(configuration.configPath, 'w') as config_file:
            json.dump(configuration.configData, config_file, indent=2)
    except Exception as e:
        logger.exception(f"switchSustain error: {e}")

def switchNoDoubles():
    try:
        configuration.configData['midiToQwerty']['noDoubles'] = switchNoDoublesvar.get() == "on"
        with open(configuration.configPath, 'w') as config_file:
            json.dump(configuration.configData, config_file, indent=2)
    except Exception as e:
        logger.exception(f"switchNoDoubles error: {e}")

def switchVelocity():
    try:
        configuration.configData['midiToQwerty']['velocity'] = switchVelocityvar.get() == "on"
        with open(configuration.configPath, 'w') as config_file:
            json.dump(configuration.configData, config_file, indent=2)
    except Exception as e:
        logger.exception(f"switchVelocity error: {e}")

def switch88Keys():
    try:
        configuration.configData['midiToQwerty']['88Keys'] = switch88Keysvar.get() == "on"
        with open(configuration.configPath, 'w') as config_file:
            json.dump(configuration.configData, config_file, indent=2)
    except Exception as e:
        logger.exception(f"switch88Keys error: {e}")

def switchCustomHoldLength():
    try:
        configuration.configData['midiToQwerty']['customHoldLength']['enabled'] = switchCustomHoldLengthvar.get() == "on"
        with open(configuration.configPath, 'w') as config_file:
            json.dump(configuration.configData, config_file, indent=2)
        customHoldLengthStatus()
    except Exception as e:
        logger.exception(f"switchCustomHoldLength error: {e}")

def customHoldLengthStatus():
    try:
        from ui.midiToQWERTY import MidiToQwertyTab
        if configuration.configData["midiToQwerty"]['customHoldLength']['enabled']:
            MidiToQwertyTab.customHoldLengthSlider.configure(state="normal")
            MidiToQwertyTab.resetCustomHoldLength.configure(state="normal")
            MidiToQwertyTab.customHoldLengthEntry.configure(state="normal", text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColor"])
        else:
            MidiToQwertyTab.customHoldLengthSlider.configure(state="disabled")
            MidiToQwertyTab.resetCustomHoldLength.configure(state="disabled")
            MidiToQwertyTab.customHoldLengthEntry.configure(state="disabled", text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColorDisabled"])
    except Exception as e:
        logger.exception(f"customHoldLengthStatus error: {e}")

def onModuleSelect(value):
    try:
        configuration.configData["midiToQwerty"]["inputModule"] = value
        with open(configuration.configPath, 'w') as config_file:
            json.dump(configuration.configData, config_file, indent=2)
    except Exception as e:
        logger.exception(f"onModuleSelect error: {e}")

def playButton():
    try:
        if not app.isRunning:
            startPlayback()
        else:
            stopPlayback()
    except Exception as e:
        logger.exception(f"playButton error: {e}")

def startPlayback():
    try:
        from ui.midiToQWERTY import MidiToQwertyTab
        inputDevice = MidiToQwertyTab.inputDeviceDropdown.get()
        if not inputDevice:
            threading.Thread(target=mainFunctions.insertConsoleText, args=("No MIDI output device selected.", True)).start()
            return

        app.isRunning = True
        MidiToQwertyTab.toggleListener.configure(
            text="Disable",
            fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["StopColor"],
            hover_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["StopColorHover"]
        )
        MidiToQwertyTab.inputDeviceDropdown.configure(state="disabled")

        midiHandler.startMidiInput(inputDevice)
    except Exception as e:
        logger.exception(f"startPlayback error: {e}")

def stopPlayback():
    try:
        from ui.midiToQWERTY import MidiToQwertyTab
        if not app.isRunning:
            return

        midiHandler.stopMidiInput()
        app.isRunning = False
        MidiToQwertyTab.toggleListener.configure(
            text="Enable",
            fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["PlayColor"],
            hover_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["PlayColorHover"]
        )
        MidiToQwertyTab.inputDeviceDropdown.configure(state="normal")
    except Exception as e:
        logger.exception(f"stopPlayback error: {e}")

def pausePlayback():
    try:
        if not app.isRunning:
            return
        stopPlayback()
    except Exception as e:
        logger.exception(f"pausePlayback error: {e}")

def decreaseSpeed():
    try:
        logger.info("decreaseSpeed called (not implemented)")
    except Exception as e:
        logger.exception(f"decreaseSpeed error: {e}")

def increaseSpeed():
    try:
        logger.info("increaseSpeed called (not implemented)")
    except Exception as e:
        logger.exception(f"increaseSpeed error: {e}")
