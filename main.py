import customtkinter as ctk
import platform
import os
import datetime
import logging
import sys
import signal
import threading
import argparse
import time
import errno

from PIL import Image
from ui.midiPlayer import MidiPlayerTab
from ui.drumsMacro import DrumsMacroTab
from ui.midiHub import MidiHubTab
from ui.settings import SettingsTab
from ui.midiToQWERTY import MidiToQwertyTab
from ui.info import InfoTab
from ui.darwinPermission import DarwinPermissionTab
from ui import customTheme
from ui.widget.loadingScreen import LoadingScreen
from modules.functions import mainFunctions
from modules import configuration
from modules import updater
from modules import telemetry

appVersion = "v11.69.67"
osName = platform.system()

if osName == "Darwin":
    mainFunctions.startGlobalListener()

documentsDir = os.path.join(os.path.expanduser("~"), "Documents")

# LOGS
logger = logging.getLogger("nanoMIDIPlayer")

class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

def safeDelete(filepath, retries=3, delay=0.1):
    for attempt in range(retries):
        try:
            os.remove(filepath)
            return True
        except PermissionError:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return False
        except OSError as e:
            if e.errno == errno.ENOENT:
                return True
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return False
    return False

def initLogging():
    logDir = os.path.join(documentsDir, "nanoMIDIPlayer", "logs")
    os.makedirs(logDir, exist_ok=True)

    try:
        logFiles = []
        for f in os.listdir(logDir):
            if f.startswith("nanoMIDIPlayer_") and f.endswith(".log"):
                full_path = os.path.join(logDir, f)
                try:
                    mtime = os.path.getmtime(full_path)
                    logFiles.append((full_path, mtime))
                except (OSError, FileNotFoundError):
                    continue
        
        if logFiles:
            logFiles.sort(key=lambda x: x[1])
            files_to_keep = 9
            
            if len(logFiles) > files_to_keep:
                files_to_delete = logFiles[:-(files_to_keep)]
                for filepath, _ in files_to_delete:
                    safeDelete(filepath)
    
    except Exception as e:
        pass

    logFile = os.path.join(
        logDir,
        f"nanoMIDIPlayer_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    )

    fileHandler = FlushFileHandler(logFile, encoding="utf-8")

    handlers = [fileHandler]
    if sys.stdout:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
        force=True
    )

    logger = logging.getLogger("nanoMIDIPlayer")
    logger.info(f"Logging initialized → {logFile}")
    return logFile

def killApp(sig, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, killApp)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        logger.info("App initialized")

        # WINDOW PROPERTIES
        self.title("nanoMIDIPlayer")
        self.geometry("600x450")
        self.resizable(False, False)

        if osName == "Windows":
            iconPath = os.path.join(os.path.dirname(__file__), "temp_icon.ico")
            customTheme.iconImage.save(iconPath)
            self.iconbitmap(iconPath)

        # - VARIABLES --------------------------------------------
        self.currentPage = None
        self.logLabels = []
        self.maxMidiPlayerConsoleLog = 8
        self.maxDrumPlayerConsoleLog = 14
        self.maxMidiToQWERTYLog = 13
        self.isRunning = False
        self.playbackSpeed = 100
        self.themeNames = customTheme.fetchThemes()
        # --------------------------------------------------------

        self.fg=customTheme.activeThemeData["Theme"]["Navigation"]["BackColor"]
        self.contentFrame = ctk.CTkFrame(self)
        self.contentFrame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        mainFunctions.registerApp(self)
        from modules.functions import midiPlayerFunctions
        from modules.functions import drumsMacroFunctions
        from modules.functions import settingsFunctions

        parser = argparse.ArgumentParser(description='nanoMIDIPlayer')
        parser.add_argument('--debug', action='store_true', help='debug console')
        args = parser.parse_args()

        if args.debug:
            settingsFunctions.openConsole()
            print("console opened.")

        self.frames = {
            "midi": MidiPlayerTab(self.contentFrame),
            "drums": DrumsMacroTab(self.contentFrame),
            "hub": MidiHubTab(self.contentFrame),
            "miditoqwerty": MidiToQwertyTab(self.contentFrame),
            "settings": SettingsTab(self.contentFrame),
            "info": InfoTab(self.contentFrame),
            "darwinpermission": DarwinPermissionTab(self.contentFrame)
        }

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        customTheme.initializeFonts()

        # -- SIDEBAR START --
        # SIDEBAR > NAVIGATIONFRAME
        self.navigationFrame = ctk.CTkFrame(self, corner_radius=0, fg_color=customTheme.activeThemeData["Theme"]["Navigation"]["BackColor"])
        self.navigationFrame.grid(row=0, column=0, sticky="nsew")
        self.navigationFrame.grid_rowconfigure(6, weight=1)

        self.navigationFrameLabel = ctk.CTkLabel(
            self.navigationFrame, text="", image=customTheme.logoImage,
            compound="left", font=("Arial", 20)
        )
        self.navigationFrameLabel.grid(row=0, column=0, padx=20, pady=20)

        # SIDEBAR > HOMEBUTTON
        self.homeButton = ctk.CTkButton(
            self.navigationFrame, corner_radius=0, height=40, border_spacing=10, text="MIDI Player",
            fg_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonColor"], text_color=customTheme.activeThemeData["Theme"]["Navigation"]["TextColor"], hover_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonHoverColor"],
            image=customTheme.pianoImageCTk, anchor="w", font=customTheme.globalFont14, command=lambda: self.showFrame("midi")
        )
        self.homeButton.grid(row=1, column=0, sticky="ew")

        # SIDEBAR > DRUMSBUTTON
        self.drumsButton = ctk.CTkButton(
            self.navigationFrame, corner_radius=0, height=40, border_spacing=10, text="Drums Player",
            fg_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonColor"], text_color=customTheme.activeThemeData["Theme"]["Navigation"]["TextColor"], hover_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonHoverColor"],
            image=customTheme.drumImageCTk, anchor="w", font=customTheme.globalFont14, command=lambda: self.showFrame("drums")
        )
        self.drumsButton.grid(row=2, column=0, sticky="ew")

        # SIDEBAR > MIDIHUBBUTTON
        self.midiHubButton = ctk.CTkButton(
            self.navigationFrame, corner_radius=0, height=40, border_spacing=10, text="MIDI Hub",
            fg_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonColor"], text_color=customTheme.activeThemeData["Theme"]["Navigation"]["TextColor"], hover_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonHoverColor"],
            image=customTheme.pianoImageCTk, anchor="w", font=customTheme.globalFont14, command=lambda: self.showFrame("hub")
        )
        self.midiHubButton.grid(row=3, column=0, sticky="ew")

        # SIDEBAR > MIDITOQWERTY BUTTON
        self.midiToQwertyButton = ctk.CTkButton(
            self.navigationFrame, corner_radius=0, height=40, border_spacing=10, text="MIDI To QWERTY",
            fg_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonColor"], text_color=customTheme.activeThemeData["Theme"]["Navigation"]["TextColor"], hover_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonHoverColor"],
            image=customTheme.keyboardImageCTk, anchor="w", font=customTheme.globalFont14, command=lambda: self.showFrame("miditoqwerty")
        )
        self.midiToQwertyButton.grid(row=4, column=0, sticky="ew")

        # SIDEBAR > SETTINGS BUTTON
        self.settingsButton = ctk.CTkButton(
            self.navigationFrame, corner_radius=0, height=40, border_spacing=10, text="Settings",
            fg_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonColor"], text_color=customTheme.activeThemeData["Theme"]["Navigation"]["TextColor"], hover_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonHoverColor"],
            image=customTheme.settingsImageCTk, anchor="w", font=customTheme.globalFont14, command=lambda: self.showFrame("settings")
        )
        self.settingsButton.grid(row=5, column=0, sticky="ew")

        # SIDEBAR WATERMARK
        self.customThemeWatermarkLine1 = ctk.CTkLabel(
            self.navigationFrame, text=customTheme.activeThemeData["Theme"]["Navigation"]["CustomThemeWatermarkLN1"], fg_color="transparent", text_color=customTheme.activeThemeData["Theme"]["Navigation"]["CustomWatermarkColor"], font=customTheme.globalFont14
        )
        self.customThemeWatermarkLine1.grid(row=7, column=0, padx=0, pady=(0, 0), sticky="n")

        self.customThemeWatermarkLine2 = ctk.CTkLabel(
            self.navigationFrame, text=customTheme.activeThemeData["Theme"]["Navigation"]["CustomThemeWatermarkLN2"], fg_color="transparent", text_color=customTheme.activeThemeData["Theme"]["Navigation"]["CustomWatermarkColor"], font=customTheme.globalFont14
        )
        self.customThemeWatermarkLine2.grid(row=8, column=0, padx=0, pady=(0, 0), sticky="n")

        # SIDEBAR > DARWIN PERMISSION BUTTON
        if osName == "Darwin":
            from ui.darwinPermission import isAccessibility, isInput
            if not isInput or not isAccessibility:
                self.padlockImageCTk = ctk.CTkImage(Image.open(mainFunctions.resourcePath("assets/icons/integrated/padlock-white.png")), size=(18, 18))           
                self.permissionButton = ctk.CTkButton(
                    self.navigationFrame, corner_radius=0, height=40, border_spacing=10, text="PERMISSIONS\nREQUIRED!",
                    fg_color="#6E0000", text_color=("gray90", "gray90"), hover_color="#4D0000",
                    image=self.padlockImageCTk, anchor="w", font=customTheme.globalFont14, command=lambda: self.showFrame("darwinpermission")
                )
                self.permissionButton.grid(row=9, column=0)
        
        # SIDEBAR > WATERMARK
        self.appInfoButton = ctk.CTkButton(
            self.navigationFrame, corner_radius=0, height=40, border_spacing=10, text=f"nanoMIDIPlayer\n{appVersion}",
            fg_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonColor"], text_color=customTheme.activeThemeData["Theme"]["Navigation"]["WatermarkColor"], hover_color=customTheme.activeThemeData["Theme"]["Navigation"]["TabButtonHoverColor"],
            image=customTheme.infoImageCTk, anchor="w", font=customTheme.globalFont14, command=lambda: self.showFrame("info")
        )
        self.appInfoButton.grid(row=10, column=0, sticky="s")
        # -- SIDEBAR END --

        # FINALIZATION
        if configuration.configData['appUI']['topmost'] == True:
            self.wm_attributes("-topmost", True)

        midiPlayerFunctions.loadSavedFile()
        drumsMacroFunctions.loadSavedFile()

        self.after(1000, mainFunctions.refreshInputDevices)
        self.after(1000, mainFunctions.refreshOutputDevices)

        settingsFunctions.initControlSets()
        self.showFrame("midi")

        if configuration.configData['appUI']['sendTelemetry'] == True:
            telemetryThread = threading.Thread(target=telemetry.startPing)
            telemetryThread.daemon = True
            telemetryThread.start()
        
        midiPlayerFunctions.switchUseMIDIvar.set("on" if configuration.configData.get('midiPlayer', {}).get('useMIDIOutput', False) else "off")

        if osName == "Windows" and configuration.configData["appUI"]["checkForUpdates"]:
            threading.Thread(target=updater.runUpdater, args=(appVersion,)).start()

        if osName == "Darwin":
            mainFunctions.log("WARNING: The macOS MIDI Player may run inefficiently due to system restrictions. Please report any issues or bugs to the developer.")

    # FUNCTIONS
    def showFrame(self, name):
        pageIndexMap = {
            "midi": 0,
            "drums": 1,
            "hub": 2,
            "miditoqwerty": 3,
            "settings": 4,
            "info": 5,
            "darwinpermission": 6
        }
        newPageIndex = pageIndexMap[name]

        if self.currentPage == newPageIndex:
            return

        self.currentPage = newPageIndex

        for frame in self.frames.values():
            frame.pack_forget()

        self.frames[name].pack(expand=True, fill="both")
        mainFunctions.tabBind(self.currentPage)
        self.focus_set()

if __name__ == "__main__":
    logFile = initLogging()
    logger.info(f"Application starting, logs at {logFile}")
    loading = LoadingScreen()
    loading.mainloop()