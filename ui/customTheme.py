import os
import json
import platform
import io
import base64
import shutil
from PIL import Image
import customtkinter as ctk
import ui.customTheme as customTheme
import importlib
import sys

from modules import configuration
import requests

osName = platform.system()

documentsDir = os.path.join(os.path.expanduser("~"), "Documents")
baseDirectory = os.path.join(documentsDir, "nanoMIDIPlayer")
assetsDirectory = os.path.join(baseDirectory, "assets")
os.makedirs(assetsDirectory, exist_ok=True)

customThemesDir = os.path.join(baseDirectory, "assets", "customThemes")
os.makedirs(customThemesDir, exist_ok=True)

activeThemeFile = "activeTheme.json"
activeThemePath = os.path.join(assetsDirectory, activeThemeFile)

def resourcePath(relativePath):
    if hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS
    else:
        basePath = os.path.abspath(".")
    return os.path.join(basePath, relativePath)

defaultThemePath = resourcePath("assets/defaultTheme.json")

remoteThemeUrl = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/api/theme.json"

class ThemeDict(dict):
    def __init__(self, filePath, defaultPath, remoteUrl):
        self.filePath = filePath
        self.defaultPath = defaultPath
        self.remoteUrl = remoteUrl
        self.images = {}
        self.fonts = {}
        
        if not os.path.exists(self.filePath):
            self.copyDefaultTheme()
        
        self.loadTheme()
        self.updateModuleAttributes()
    
    def loadTheme(self):
        try:
            with open(self.filePath, "r") as themeFile:
                data = json.load(themeFile)
                super().__init__(data)
                self.loadImages()
        except (json.JSONDecodeError, FileNotFoundError):
            self.repairCorruptedTheme()
    
    def copyDefaultTheme(self):
        if os.path.exists(self.defaultPath):
            shutil.copy(self.defaultPath, self.filePath)
        else:
            self.fetchOnlineDefault()
    
    def fetchOnlineDefault(self):
        try:
            response = requests.get(self.remoteUrl, timeout=5)
            if response.status_code == 200:
                themeData = response.json()
                defaultTheme = themeData.get("defaultTheme")
                availableThemes = themeData.get("availableThemes", {})
                defaultThemeUrl = availableThemes.get(str(defaultTheme))
                
                if defaultThemeUrl:
                    themeResponse = requests.get(defaultThemeUrl, timeout=5)
                    if themeResponse.status_code == 200:
                        with open(self.filePath, "w") as file:
                            file.write(themeResponse.text)
                        return
        except:
            pass
        
        if os.path.exists(self.defaultPath):
            shutil.copy(self.defaultPath, self.filePath)
    
    def repairCorruptedTheme(self):
        self.fetchOnlineDefault()
        self.loadTheme()
    
    def b64ToImage(self, b64string):
        if b64string in self.images:
            return self.images[b64string]
        
        data = base64.b64decode(b64string)
        image = Image.open(io.BytesIO(data))
        self.images[b64string] = image
        return image
    
    def loadImages(self):
        try:
            iconB64 = self["Theme"]["Icons"]["icon"]
            bannerB64 = self["Theme"]["Icons"]["banner"]
            resetB64 = self["Theme"]["Icons"]["reset"]
            pianoB64 = self["Theme"]["Icons"]["piano"]
            drumB64 = self["Theme"]["Icons"]["drum"]
            downloadB64 = self["Theme"]["Icons"]["download"]
            searchB64 = self["Theme"]["Icons"]["search"]
            settingsB64 = self["Theme"]["Icons"]["cogwheel"]
            keyboardB64 = self["Theme"]["Icons"]["keyboard"]
            infoB64 = self["Theme"]["Icons"]["info"]
            
            self.iconImage = self.b64ToImage(iconB64)
            self.bannerImage = self.b64ToImage(bannerB64)
            self.resetImage = self.b64ToImage(resetB64)
            self.pianoImage = self.b64ToImage(pianoB64)
            self.drumImage = self.b64ToImage(drumB64)
            self.downloadImage = self.b64ToImage(downloadB64)
            self.searchImage = self.b64ToImage(searchB64)
            self.settingsImage = self.b64ToImage(settingsB64)
            self.keyboardImage = self.b64ToImage(keyboardB64)
            self.infoImage = self.b64ToImage(infoB64)
            
            self.logoImage = ctk.CTkImage(self.bannerImage, size=(86, 26))
            self.resetImageCTk = ctk.CTkImage(self.resetImage, size=(16, 16))
            self.pianoImageCTk = ctk.CTkImage(self.pianoImage, size=(20, 20))
            self.drumImageCTk = ctk.CTkImage(self.drumImage, size=(20, 20))
            self.downloadImageFile = ctk.CTkImage(self.downloadImage, size=(18, 18))
            self.searchImageFile = ctk.CTkImage(self.searchImage, size=(18, 18))
            self.settingsImageCTk = ctk.CTkImage(self.settingsImage, size=(18, 18))
            self.keyboardImageCTk = ctk.CTkImage(self.keyboardImage, size=(18, 18))
            self.infoImageCTk = ctk.CTkImage(self.infoImage, size=(18, 18))
        except KeyError:
            self.loadFallbackImages()
    
    def loadFallbackImages(self):
        blackImage = Image.new("RGBA", (1, 1), (0, 0, 0, 255))
        self.iconImage = blackImage
        self.bannerImage = blackImage
        self.resetImage = blackImage
        self.pianoImage = blackImage
        self.drumImage = blackImage
        self.downloadImage = blackImage
        self.searchImage = blackImage
        self.settingsImage = blackImage
        self.keyboardImage = blackImage
        self.infoImage = blackImage
        
        self.logoImage = ctk.CTkImage(blackImage, size=(86, 26))
        self.resetImageCTk = ctk.CTkImage(blackImage, size=(16, 16))
        self.pianoImageCTk = ctk.CTkImage(blackImage, size=(20, 20))
        self.drumImageCTk = ctk.CTkImage(blackImage, size=(20, 20))
        self.downloadImageFile = ctk.CTkImage(blackImage, size=(18, 18))
        self.searchImageFile = ctk.CTkImage(blackImage, size=(18, 18))
        self.settingsImageCTk = ctk.CTkImage(blackImage, size=(18, 18))
        self.keyboardImageCTk = ctk.CTkImage(blackImage, size=(18, 18))
        self.infoImageCTk = ctk.CTkImage(blackImage, size=(18, 18))
    
    def updateModuleAttributes(self):
        module = sys.modules[__name__]
        
        module.iconImage = self.iconImage
        module.bannerImage = self.bannerImage
        module.resetImage = self.resetImage
        module.pianoImage = self.pianoImage
        module.drumImage = self.drumImage
        module.downloadImage = self.downloadImage
        module.searchImage = self.searchImage
        module.settingsImage = self.settingsImage
        module.keyboardImage = self.keyboardImage
        module.infoImage = self.infoImage
        
        module.logoImage = self.logoImage
        module.resetImageCTk = self.resetImageCTk
        module.pianoImageCTk = self.pianoImageCTk
        module.drumImageCTk = self.drumImageCTk
        module.downloadImageFile = self.downloadImageFile
        module.searchImageFile = self.searchImageFile
        module.settingsImageCTk = self.settingsImageCTk
        module.keyboardImageCTk = self.keyboardImageCTk
        module.infoImageCTk = self.infoImageCTk
    
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            defaultTheme = self.getDefaultTheme()
            if key in defaultTheme:
                self[key] = defaultTheme[key]
                self.saveTheme()
                return self[key]
            else:
                raise KeyError(f"Theme key '{key}' not found")
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.saveTheme()
    
    def getDefaultTheme(self):
        try:
            response = requests.get(self.remoteUrl, timeout=5)
            if response.status_code == 200:
                themeData = response.json()
                defaultTheme = themeData.get("defaultTheme")
                availableThemes = themeData.get("availableThemes", {})
                defaultThemeUrl = availableThemes.get(str(defaultTheme))
                
                if defaultThemeUrl:
                    themeResponse = requests.get(defaultThemeUrl, timeout=5)
                    if themeResponse.status_code == 200:
                        return json.loads(themeResponse.text)
        except:
            pass
        
        if os.path.exists(self.defaultPath):
            with open(self.defaultPath, "r") as f:
                return json.load(f)
        
        return {}
    
    def saveTheme(self):
        with open(self.filePath, "w") as file:
            json.dump(dict(self), file, indent=2)
    
    def reload(self):
        self.loadTheme()
        self.updateModuleAttributes()

activeThemeData = ThemeDict(activeThemePath, defaultThemePath, remoteThemeUrl)

def initializeFonts():
    global globalFont11, globalFont12, globalFont14, globalFont20, globalFont40
    
    if osName == "Windows":
        family = activeThemeData["Theme"]["GlobalFont"]["Windows"]
    elif osName == "Darwin":
        family = activeThemeData["Theme"]["GlobalFont"]["macOS"]
    elif osName == "Linux":
        family = activeThemeData["Theme"]["GlobalFont"]["Linux"]
    else:
        family = activeThemeData["Theme"]["GlobalFont"]["Windows"]

    globalFont11 = ctk.CTkFont(size=11, weight="bold", family=family)
    globalFont12 = ctk.CTkFont(size=12, weight="bold", family=family)
    globalFont14 = ctk.CTkFont(size=14, weight="bold", family=family)
    globalFont20 = ctk.CTkFont(size=20, weight="bold", family=family)
    globalFont40 = ctk.CTkFont(size=40, weight="bold", family=family)

def fetchThemes(event=None):
    try:
        response = requests.get(remoteThemeUrl, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        themeNames = list(data["availableThemes"].keys())
        return themeNames
    except:
        return []

def loadTheme(event=None):
    try:
        response = requests.get(remoteThemeUrl, timeout=10)
        response.raise_for_status()
        themeData = response.json()
        
        os.makedirs(assetsDirectory, exist_ok=True)
        defaultTheme = themeData.get("defaultTheme")
        availableThemes = themeData.get("availableThemes", {})
        defaultThemeUrl = availableThemes.get(str(defaultTheme))
        
        if defaultThemeUrl:
            themeResponse = requests.get(defaultThemeUrl, timeout=10)
            if themeResponse.status_code == 200:
                with open(activeThemePath, "w") as file:
                    file.write(themeResponse.text)
                activeThemeData.reload()
                return
    except:
        pass

    try:
        shutil.copy(defaultThemePath, activeThemePath)
        activeThemeData.reload()
    except:
        pass

def switchTheme(event=None):
    from ui.settings import SettingsTab
    from modules.functions import mainFunctions
    from main import App

    app = mainFunctions.getApp()
    value = SettingsTab.themeSelector.get()
    configuration.configData['appUI']['forceTheme'] = False
    configuration.configData.save()

    if "(Custom)" not in value:
        response = requests.get(remoteThemeUrl, timeout=5)
        if response.status_code == 200:
            themeData = response.json()
            availableThemes = themeData["availableThemes"]
            if value in availableThemes:
                themeUrl = availableThemes[value]
                themeResponse = requests.get(themeUrl, timeout=5)
                if themeResponse.status_code == 200:
                    with open(activeThemePath, 'w') as activeThemeFile:
                        activeThemeFile.write(themeResponse.text)
                    activeThemeData.reload()
                else:
                    print(f"FAIL > {themeUrl}. Code: ({themeResponse.status_code})")
            else:
                print(f"'{value}' does not exist.")
        else:
            print(f"Failed ({response.status_code})")
    else:
        customThemeName = value.replace(" (Custom)", "")
        customThemePath = os.path.join(customThemesDir, customThemeName)
        if os.path.isfile(customThemePath):
            with open(customThemePath, 'r') as customThemeFile:
                customThemeData = customThemeFile.read()
            with open(activeThemePath, 'w') as activeThemeFile:
                activeThemeFile.write(customThemeData)
            activeThemeData.reload()
        else:
            print(f"'{customThemePath}' does not exist.")

    app.destroy()

    importlib.reload(customTheme)

    newApp = App()
    mainFunctions.registerApp(newApp)
    newApp.mainloop()