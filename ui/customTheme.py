import os
import json
import platform
import io
import base64
import shutil
import logging
from PIL import Image
import customtkinter as ctk
import ui.customTheme as customTheme
import importlib
import sys

from modules import configuration
import requests

logger = logging.getLogger(__name__)

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

def validateJsonFile(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read().strip()
            if not content:
                return False, "File is empty"
            json.loads(content)
            return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return False, f"File error: {str(e)}"

def createFallbackTheme():
    try:
        fallbackTheme = {}
        
        if os.path.exists(defaultThemePath):
            isValid, error = validateJsonFile(defaultThemePath)
            if isValid:
                with open(defaultThemePath, "r") as f:
                    fallbackTheme = json.load(f)
                logger.info("Loaded fallback from defaultTheme.json")
            else:
                logger.error(f"defaultTheme.json invalid: {error}")
        else:
            logger.error("defaultTheme.json not found")
            
            fallbackTheme = {
                "Theme": {
                    "Icons": {},
                    "GlobalFont": {
                        "Windows": "Segoe UI",
                        "macOS": "SF Pro",
                        "Linux": "Ubuntu"
                    }
                }
            }
        
        with open(activeThemePath, "w") as file:
            json.dump(fallbackTheme, file, indent=2)
        logger.info("Created fallback theme")
        return fallbackTheme
        
    except Exception as e:
        logger.error(f"Failed to create fallback: {str(e)}")
        
        minimalTheme = {"Theme": {}}
        with open(activeThemePath, "w") as file:
            json.dump(minimalTheme, file, indent=2)
        return minimalTheme

def loadThemeFile():
    global activeThemeData
    
    themeValid = False
    activeThemeData = {}
    
    if not os.path.exists(activeThemePath):
        logger.info("Theme file doesn't exist, creating initial theme")
        activeThemeData = createFallbackTheme()
        return activeThemeData
    
    isValid, error = validateJsonFile(activeThemePath)
    if isValid:
        try:
            with open(activeThemePath, "r") as themeFile:
                activeThemeData = json.load(themeFile)
            if isinstance(activeThemeData, dict) and "Theme" in activeThemeData:
                themeValid = True
                logger.info("Loaded existing theme")
            else:
                logger.error("Theme is missing required 'Theme' key")
        except Exception as e:
            logger.error(f"Error loading theme: {str(e)}")
    else:
        logger.warning(f"Theme validation failed: {error}")
    
    if not themeValid:
        logger.warning("Using fallback theme")
        activeThemeData = createFallbackTheme()
    
    return activeThemeData

def checkThemeUpdates():
    global activeThemeData
    
    loadThemeFile()
    
    remoteThemeData = {}
    url = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/assets/defaultTheme.json"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            try:
                remoteThemeData = response.json()
                logger.info("Successfully fetched remote theme")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in remote theme: {str(e)}")
                remoteThemeData = {}
        else:
            logger.warning(f"Failed to retrieve remote theme. Code: {response.status_code}")
    except requests.exceptions.Timeout:
        logger.warning("Remote theme fetch timeout")
    except requests.exceptions.ConnectionError:
        logger.warning("No internet connection for theme update")
    except Exception as e:
        logger.error(f"Error fetching remote theme: {str(e)}")
    
    if not remoteThemeData and os.path.exists(defaultThemePath):
        isValid, error = validateJsonFile(defaultThemePath)
        if isValid:
            try:
                with open(defaultThemePath, "r") as f:
                    remoteThemeData = json.load(f)
                logger.info("Loaded defaultTheme.json as fallback")
            except Exception as e:
                logger.error(f"Error loading defaultTheme.json: {str(e)}")
        else:
            logger.error(f"defaultTheme.json invalid: {error}")
    
    if not remoteThemeData:
        logger.warning("No valid remote theme source available")
        return
    
    try:
        updated = False
        
        if not isinstance(remoteThemeData, dict) or "Theme" not in remoteThemeData:
            logger.error("Remote theme is missing required structure")
            return
        
        themeUpdated = False
        themeKeysAdded = []
        
        def recursiveUpdate(current, remote, path=""):
            nonlocal themeUpdated
            for key, value in remote.items():
                fullPath = f"{path}.{key}" if path else key
                if key not in current:
                    current[key] = value
                    themeUpdated = True
                    themeKeysAdded.append(fullPath)
                elif isinstance(value, dict) and isinstance(current[key], dict):
                    recursiveUpdate(current[key], value, fullPath)
        
        recursiveUpdate(activeThemeData, remoteThemeData)
        
        if themeUpdated:
            backupPath = activeThemePath + ".backup"
            try:
                shutil.copy2(activeThemePath, backupPath)
                logger.info(f"Created theme backup: {backupPath}")
            except Exception as e:
                logger.error(f"Failed to create backup: {str(e)}")
            
            try:
                with open(activeThemePath, "w") as file:
                    json.dump(activeThemeData, file, indent=2)
                logger.info(f"Updated Theme with keys: {themeKeysAdded}")
            except Exception as e:
                logger.error(f"Failed to write updated theme: {str(e)}")
                
                try:
                    shutil.copy2(backupPath, activeThemePath)
                    logger.info("Restored theme from backup")
                except:
                    createFallbackTheme()
        else:
            logger.info("Theme Up to Date")
            
    except Exception as e:
        logger.error(f"Theme update failed: {str(e)}")
        
        try:
            activeThemeData = createFallbackTheme()
        except Exception as e2:
            logger.critical(f"Failed to create fallback: {str(e2)}")

def safeB64ToImage(b64string, defaultName):
    try:
        if not b64string:
            raise ValueError("Empty base64 string")
        
        data = base64.b64decode(b64string)
        return Image.open(io.BytesIO(data))
    except Exception as e:
        logger.error(f"Failed to decode {defaultName} image: {str(e)}")
        return Image.new('RGBA', (32, 32), (255, 255, 255, 255))

def initializeImages():
    global iconImage, bannerImage, resetImage, pianoImage, drumImage
    global downloadImage, searchImage, settingsImage, keyboardImage, infoImage
    global logoImage, resetImageCTk, pianoImageCTk, drumImageCTk
    global downloadImageFile, searchImageFile, settingsImageCTk, keyboardImageCTk, infoImageCTk
    
    icons = activeThemeData.get("Theme", {}).get("Icons", {})
    
    iconImage = safeB64ToImage(icons.get("icon"), "icon")
    bannerImage = safeB64ToImage(icons.get("banner"), "banner")
    resetImage = safeB64ToImage(icons.get("reset"), "reset")
    pianoImage = safeB64ToImage(icons.get("piano"), "piano")
    drumImage = safeB64ToImage(icons.get("drum"), "drum")
    downloadImage = safeB64ToImage(icons.get("download"), "download")
    searchImage = safeB64ToImage(icons.get("search"), "search")
    settingsImage = safeB64ToImage(icons.get("cogwheel"), "cogwheel")
    keyboardImage = safeB64ToImage(icons.get("keyboard"), "keyboard")
    infoImage = safeB64ToImage(icons.get("info"), "info")
    
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
    
    fontConfig = activeThemeData.get("Theme", {}).get("GlobalFont", {})
    
    if osName == "Windows":
        family = fontConfig.get("Windows", "Segoe UI")
    elif osName == "Darwin":
        family = fontConfig.get("macOS", "SF Pro")
    elif osName == "Linux":
        family = fontConfig.get("Linux", "Ubuntu")
    else:
        family = fontConfig.get("Windows", "Segoe UI")
    
    globalFont11 = ctk.CTkFont(size=11, weight="bold", family=family)
    globalFont12 = ctk.CTkFont(size=12, weight="bold", family=family)
    globalFont14 = ctk.CTkFont(size=14, weight="bold", family=family)
    globalFont20 = ctk.CTkFont(size=20, weight="bold", family=family)
    globalFont40 = ctk.CTkFont(size=40, weight="bold", family=family)

def fetchThemes(event=None):
    try:
        response = requests.get("https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/api/theme.json", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        themeNames = list(data.get("availableThemes", {}).keys())
        return themeNames
    except requests.RequestException as e:
        logger.error(f"Failed to fetch themes: {str(e)}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in theme list: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching themes: {str(e)}")
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
                isValid, error = validateJsonFileFromString(themeResponse.text)
                if isValid:
                    with open(activeThemePath, "w") as file:
                        file.write(themeResponse.text)
                    logger.info("Downloaded Theme")
                    return True
                else:
                    logger.error(f"Downloaded theme invalid: {error}")
    except Exception as e:
        logger.error(f"Failed to fetch online theme: {str(e)}")

    try:
        if os.path.exists(defaultThemePath):
            isValid, error = validateJsonFile(defaultThemePath)
            if isValid:
                shutil.copy(defaultThemePath, activeThemePath)
                logger.info("Loaded fallback defaultTheme.json")
                return True
            else:
                logger.error(f"Fallback theme invalid: {error}")
        else:
            logger.error("Default theme file not found")
    except Exception as e:
        logger.error(f"Fallback failed: {str(e)}")
    
    return False

def validateJsonFileFromString(content):
    try:
        if not content.strip():
            return False, "Content is empty"
        json.loads(content)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def switchTheme(event=None):
    from ui.settings import SettingsTab
    from modules.functions import mainFunctions
    from main import App

    app = mainFunctions.getApp()
    value = SettingsTab.themeSelector.get()
    
    try:
        configuration.configData['appUI']['forceTheme'] = False
        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)
    except Exception as e:
        logger.error(f"Failed to update config: {str(e)}")
    
    themeSwitched = False
    
    if "(Custom)" not in value:
        try:
            response = requests.get("https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/api/theme.json", timeout=10)
            if response.status_code == 200:
                themeData = response.json()
                availableThemes = themeData.get("availableThemes", {})
                if value in availableThemes:
                    themeUrl = availableThemes[value]
                    themeResponse = requests.get(themeUrl, timeout=10)
                    if themeResponse.status_code == 200:
                        isValid, error = validateJsonFileFromString(themeResponse.text)
                        if isValid:
                            with open(activeThemePath, 'w') as activeThemeFile:
                                activeThemeFile.write(themeResponse.text)
                            themeSwitched = True
                            logger.info(f"Switched to theme: {value}")
                        else:
                            logger.error(f"Theme validation failed: {error}")
                    else:
                        logger.error(f"Failed to download theme. Code: {themeResponse.status_code}")
                else:
                    logger.error(f"Theme '{value}' does not exist.")
            else:
                logger.error(f"Failed to fetch theme list. Code: {response.status_code}")
        except Exception as e:
            logger.error(f"Theme switch error: {str(e)}")
    else:
        customThemeName = value.replace(" (Custom)", "")
        customThemePath = os.path.join(customThemesDir, customThemeName)
        if os.path.isfile(customThemePath):
            isValid, error = validateJsonFile(customThemePath)
            if isValid:
                try:
                    with open(customThemePath, 'r') as customThemeFile:
                        customThemeData = customThemeFile.read()
                    with open(activeThemePath, 'w') as activeThemeFile:
                        activeThemeFile.write(customThemeData)
                    themeSwitched = True
                    logger.info(f"Switched to custom theme: {customThemeName}")
                except Exception as e:
                    logger.error(f"Failed to load custom theme: {str(e)}")
            else:
                logger.error(f"Custom theme invalid: {error}")
        else:
            logger.error(f"Custom theme file not found: {customThemePath}")
    
    if not themeSwitched:
        logger.warning("Theme switch failed, using current theme")
        return
    
    try:
        app.destroy()
        importlib.reload(customTheme)
        newApp = App()
        mainFunctions.registerApp(newApp)
        newApp.mainloop()
    except Exception as e:
        logger.critical(f"Failed to restart app after theme switch: {str(e)}")

checkThemeUpdates()
loadThemeFile()
initializeImages()