import customtkinter as ctk
import subprocess
import platform
import logging

from ui import customTheme
from PIL import Image
from modules.functions import mainFunctions

logger = logging.getLogger(__name__)
osName = platform.system()

def checkAccessibility():
    logger.debug("checking accessibility")
    script = '''
        tell application "System Events"
            set uiEnabled to UI elements enabled
        end tell
        return uiEnabled
        '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    logger.debug(f"checkAccessibility result: {result.stdout.strip()}")
    return "true" in result.stdout.lower()

if osName == "Darwin":
    import HIServices  # type: ignore
    isInput = HIServices.AXIsProcessTrusted()
    isAccessibility = checkAccessibility()
else:
    isInput = True
    isAccessibility = True

logger.debug(f"isInput: {isInput}")
logger.debug(f"isAccessibility: {isAccessibility}")

class DarwinPermissionTab(ctk.CTkFrame):
    def __init__(self, master):
        logger.debug("initializing DarwinPermissionTab")
        super().__init__(master)
        customTheme.initializeFonts()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mainFrame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["BackgroundColor"]
        )
        self.mainFrame.grid(row=0, column=0, sticky="nsew")
        self.mainFrame.grid_columnconfigure(0, weight=1)

        def accessibility():
            logger.debug("opening accessibility preferences")
            subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"])

        def inputMonitoring():
            logger.debug("opening input monitoring preferences")
            subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_ListenEvent"])

        self.title = ctk.CTkLabel(
            self.mainFrame, text="Required Permissions for macOS", fg_color="transparent", font=customTheme.globalFont20
        )
        self.title.grid(row=0, column=0, padx=(0, 0), pady=(10, 0), sticky="ns")

        self.accessibilityImageCTk = ctk.CTkImage(Image.open(mainFunctions.resourcePath("assets/icons/integrated/accessibility.png")), size=(349, 87))
        self.inputMonitorImageCTk = ctk.CTkImage(Image.open(mainFunctions.resourcePath("assets/icons/integrated/inputmonitor.png")), size=(349, 87))

        self.accessibilityImage = ctk.CTkButton(master=self.mainFrame, text="", fg_color="white", width=100, height=100, state="disabled", image=self.accessibilityImageCTk)
        self.inputMonitoringImage = ctk.CTkButton(master=self.mainFrame, text="", fg_color="white", width=100, height=100, state="disabled", image=self.inputMonitorImageCTk)

        self.accessibilityButton = ctk.CTkButton(self.mainFrame, width=350, text="Allow Accessibility Permission", command=accessibility)
        self.inputMonitoringButton = ctk.CTkButton(self.mainFrame, width=350, text="Allow Input Monitoring Permission", command=inputMonitoring)

        self.accessibilityImage.grid(row=1, column=0, pady=(10, 0), sticky="ns")
        self.accessibilityButton.grid(row=2, padx=0, pady=(10, 0), sticky="ns")

        self.inputMonitoringImage.grid(row=3, column=0, pady=(10, 0), sticky="ns")
        self.inputMonitoringButton.grid(row=4, padx=0, pady=(10, 0), sticky="ns")

        self.permission_tab_frame_label2 = ctk.CTkLabel(
            self.mainFrame, text="Accessibility is required for keypress automation\n\nInput Monitoring is required for Play/Pause, etc hotkeys", fg_color="transparent",
            font=customTheme.globalFont12
        )
        self.permission_tab_frame_label2.grid(row=6, column=0, padx=(0, 0), pady=(10, 0), sticky="n")

        if osName == "Darwin" and isAccessibility:
            logger.debug("accessibility permission granted")
            self.accessibilityButton.configure(state="disabled", text="Accessibility Permission Granted")

        if osName == "Darwin" and isInput:
            logger.debug("input monitoring permission granted")
            self.inputMonitoringButton.configure(state="disabled", text="Input Monitoring Permission Granted")
