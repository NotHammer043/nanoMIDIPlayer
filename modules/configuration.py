import os
import json
import platform
import shutil
import requests
import sys

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

if not os.path.exists(configPath):
    shutil.copy(defaultConfigPath, configPath)

with open(configPath, "r") as config:
    configData = json.load(config)

def checkConfig():
    global configData
    url = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/beta/api/defaultConfig.json"
    remoteConfig = None

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            remoteConfig = response.json()
        else:
            print(f"Failed to retrieve remote configuration. Code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching remote configuration: {e}")

    if remoteConfig is None:
        if os.path.exists(defaultConfigPath):
            with open(defaultConfigPath, "r") as f:
                remoteConfig = json.load(f)
            print("Loaded defaultConfig.json as fallback")
        else:
            print("No remote config and no defaultConfig.json found")
            remoteConfig = {}

    updated = False
    for key, value in remoteConfig.items():
        if key not in configData:
            configData[key] = value
            updated = True

    if updated:
        with open(configPath, "w") as file:
            json.dump(configData, file, indent=2)
        print("Updated Config")
    else:
        print("Config Up to Date")
