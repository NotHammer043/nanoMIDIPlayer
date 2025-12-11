import platform
import base64
import os
import json
import tkinter as tk

from io import BytesIO
from PIL import Image, ImageTk
from modules import configuration
from modules.functions import mainFunctions
from ui import customTheme

osName = platform.system()
documentsDir = os.path.join(os.path.expanduser("~"), "Documents")
baseDirectory = os.path.join(documentsDir, "nanoMIDIPlayer")
assetsDirectory = os.path.join(baseDirectory, "assets")

class LoadingScreen(tk.Tk):
    def __init__(self):
        currentApp = mainFunctions.getApp()
        super().__init__()
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        if osName == "Windows":
            self.wm_attributes("-transparentcolor", "black")
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        x = (screenWidth // 2) - (256 // 2)
        y = (screenHeight // 2) - (256 // 2)
        self.geometry(f"+{x}+{y}")
        self.showLogo()
        self.after(1500, self.loadMainApp)

    def showLogo(self):
        scriptRoot = os.path.dirname(os.path.abspath(__file__))
        loadingLogoPath = mainFunctions.resourcePath("assets/icons/integrated/loadingLogo.png")
        image = Image.open(loadingLogoPath).convert("RGBA")
        image = image.resize((256, 256), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self, image=self.photo, bg="black")
        self.label.pack()
        activeThemePath = os.path.join(assetsDirectory, "activeTheme.json")
        if configuration.configData["appUI"]["forceTheme"] or not os.path.exists(activeThemePath):
            customTheme.loadTheme()

    def loadMainApp(self):
        from main import App
        self.destroy()
        app = App()
        mainFunctions.registerApp(app)
        app.mainloop()
