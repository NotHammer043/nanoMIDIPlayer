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

if not os.path.exists(activeThemePath):
    shutil.copy(defaultThemePath, activeThemePath)

def b64ToImage(b64string):
    data = base64.b64decode(b64string)
    return Image.open(io.BytesIO(data))

with open(activeThemePath, "r") as themeFile:
    activeThemeData = json.load(themeFile)

iconImage = b64ToImage(activeThemeData["Theme"]["Icons"]["icon"])
bannerImage = b64ToImage(activeThemeData["Theme"]["Icons"]["banner"])
resetImage = b64ToImage(activeThemeData["Theme"]["Icons"]["reset"])
pianoImage = b64ToImage(activeThemeData["Theme"]["Icons"]["piano"])
drumImage = b64ToImage(activeThemeData["Theme"]["Icons"]["drum"])
downloadImage = b64ToImage(activeThemeData["Theme"]["Icons"]["download"])
searchImage = b64ToImage(activeThemeData["Theme"]["Icons"]["search"])
settingsImage = b64ToImage(activeThemeData["Theme"]["Icons"]["cogwheel"])
keyboardImage = b64ToImage(activeThemeData["Theme"]["Icons"]["keyboard"])
infoImage = b64ToImage(activeThemeData["Theme"]["Icons"]["info"])

logoImage = ctk.CTkImage(bannerImage, size=(86, 26))
resetImageCTk = ctk.CTkImage(resetImage, size=(16, 16))
pianoImageCTk = ctk.CTkImage(pianoImage, size=(20, 20))
drumImageCTk = ctk.CTkImage(drumImage, size=(20, 20))
downloadImageFile = ctk.CTkImage(downloadImage, size=(18, 18))
searchImageFile = ctk.CTkImage(searchImage, size=(18, 18))
settingsImageCTk = ctk.CTkImage(settingsImage, size=(18, 18))
keyboardImageCTk = ctk.CTkImage(keyboardImage, size=(18, 18))
infoImageCTk = ctk.CTkImage(infoImage, size=(18, 18))

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
        response = requests.get("https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/api/theme.json")
        response.raise_for_status()
        data = response.json()
        
        themeNames = list(data["availableThemes"].keys())
        return themeNames
    except requests.RequestException as e:
        print(e)
        return []

def loadTheme(event=None):
    try:
        response = requests.get("https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/api/theme.json", timeout=10)
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
                print("Downloaded Theme")
                return
    except Exception as e:
        print(f"Failed to fetch online theme: {e}")

    try:
        shutil.copy(defaultThemePath, activeThemePath)
        print("Loaded fallback defaultTheme.json")
    except Exception as e:
        print(f"Fallback failed: {e}")

def switchTheme(event=None):
    from ui.settings import SettingsTab
    from modules.functions import mainFunctions
    from main import App

    app = mainFunctions.getApp()
    value = SettingsTab.themeSelector.get()
    configuration.configData['appUI']['forceTheme'] = False
    with open(configuration.configPath, 'w') as configFile:
        json.dump(configuration.configData, configFile, indent=2)

    if "(Custom)" not in value:
        response = requests.get("https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/api/theme.json")
        if response.status_code == 200:
            themeData = response.json()
            availableThemes = themeData["availableThemes"]
            if value in availableThemes:
                themeUrl = availableThemes[value]
                themeResponse = requests.get(themeUrl)
                if themeResponse.status_code == 200:
                    with open(activeThemePath, 'w') as activeThemeFile:
                        activeThemeFile.write(themeResponse.text)
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
        else:
            print(f"'{customThemePath}' does not exist.")

    app.destroy()

    importlib.reload(customTheme)

    newApp = App()
    mainFunctions.registerApp(newApp)
    newApp.mainloop()