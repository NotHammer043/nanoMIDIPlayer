import os
import json
import logging
import shutil
import requests
import sys

logger = logging.getLogger(__name__)

documentsDir = os.path.join(os.path.expanduser("~"), "Documents")
baseDirectory = os.path.join(documentsDir, "nanoMIDIPlayer")
os.makedirs(baseDirectory, exist_ok=True)

configFile = "config.json"
configPath = os.path.join(baseDirectory, configFile)

def resourcePath(relativePath):
    if hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS
    else:
        basePath = os.path.abspath(".")
    return os.path.join(basePath, relativePath)

defaultConfigPath = resourcePath("assets/defaultConfig.json")

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

def createFallbackConfig():
    try:
        if os.path.exists(defaultConfigPath):
            isValid, error = validateJsonFile(defaultConfigPath)
            if isValid:
                with open(defaultConfigPath, "r") as f:
                    fallbackConfig = json.load(f)
                logger.info("Loaded fallback from defaultConfig.json")
            else:
                logger.error(f"defaultConfig.json invalid: {error}")
                fallbackConfig = {}
        else:
            logger.error("defaultConfig.json not found")
            fallbackConfig = {}
        
        with open(configPath, "w") as file:
            json.dump(fallbackConfig, file, indent=2)
        logger.info("Created fallback config")
        return fallbackConfig
        
    except Exception as e:
        logger.error(f"Failed to create fallback: {str(e)}")
        
        minimalConfig = {}
        with open(configPath, "w") as file:
            json.dump(minimalConfig, file, indent=2)
        return minimalConfig

def checkConfig():
    global configData
    
    configValid = False
    configData = {}
    
    if os.path.exists(configPath):
        isValid, error = validateJsonFile(configPath)
        if isValid:
            try:
                with open(configPath, "r") as config:
                    configData = json.load(config)
                if isinstance(configData, dict):
                    configValid = True
                    logger.info("Loaded existing config")
                else:
                    logger.error("Config is not a dictionary")
            except Exception as e:
                logger.error(f"Error loading config: {str(e)}")
        else:
            logger.warning(f"Config validation failed: {error}")
    
    if not configValid:
        logger.warning("Using fallback config")
        configData = createFallbackConfig()
        return
    
    remoteConfigs = []
    
    url = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/api/defaultConfig.json"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            try:
                apiConfig = response.json()
                remoteConfigs.append(("api", apiConfig))
                logger.info("Successfully fetched remote config")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in remote config: {str(e)}")
        else:
            logger.warning(f"Failed to retrieve remote configuration. Code: {response.status_code}")
    except requests.exceptions.Timeout:
        logger.warning("Remote config fetch timeout")
    except requests.exceptions.ConnectionError:
        logger.warning("No internet connection for config update")
    except Exception as e:
        logger.error(f"Error fetching remote configuration: {str(e)}")
    
    if os.path.exists(defaultConfigPath):
        isValid, error = validateJsonFile(defaultConfigPath)
        if isValid:
            try:
                with open(defaultConfigPath, "r") as f:
                    localDefaultConfig = json.load(f)
                remoteConfigs.append(("local_default", localDefaultConfig))
                logger.info("Loaded defaultConfig.json")
            except Exception as e:
                logger.error(f"Error loading defaultConfig.json: {str(e)}")
        else:
            logger.error(f"defaultConfig.json invalid: {error}")
    
    if not remoteConfigs:
        logger.warning("No valid config sources available")
        return
    
    try:
        updated = False
        addedKeys = []
        
        allKeys = set()
        for sourceName, sourceConfig in remoteConfigs:
            if isinstance(sourceConfig, dict):
                for key in sourceConfig.keys():
                    allKeys.add(key)
        
        backupMade = False
        backupPath = configPath + ".backup"
        
        for key in allKeys:
            if key not in configData:
                for sourceName, sourceConfig in remoteConfigs:
                    if key in sourceConfig and isinstance(sourceConfig, dict):
                        if not backupMade:
                            try:
                                shutil.copy2(configPath, backupPath)
                                logger.info(f"Created config backup: {backupPath}")
                                backupMade = True
                            except Exception as e:
                                logger.error(f"Failed to create backup: {str(e)}")
                        
                        configData[key] = sourceConfig[key]
                        updated = True
                        addedKeys.append((key, sourceName))
                        logger.info(f"Added missing key '{key}' from {sourceName}")
                        break
        
        if updated:
            try:
                with open(configPath, "w") as file:
                    json.dump(configData, file, indent=2)
                logger.info(f"Updated Config with missing keys")
                if addedKeys:
                    logger.info(f"Added new keys: {addedKeys}")
            except Exception as e:
                logger.error(f"Failed to write updated config: {str(e)}")
                
                if backupMade:
                    try:
                        shutil.copy2(backupPath, configPath)
                        logger.info("Restored config from backup")
                    except Exception as e2:
                        logger.error(f"Failed to restore from backup: {e2}")
        else:
            logger.info("Config Up to Date - No missing keys found")
            
    except Exception as e:
        logger.error(f"Config update failed: {str(e)}")