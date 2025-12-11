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

class SafeDict(dict):
    def __init__(self, manager, data, path=""):
        super().__init__(data)
        self.manager = manager
        self.path = path
        
        for key, value in list(self.items()):
            if isinstance(value, dict):
                self[key] = SafeDict(self.manager, value, f"{self.path}.{key}" if self.path else key)
    
    def __getitem__(self, key):
        try:
            value = super().__getitem__(key)
            if isinstance(value, dict) and not isinstance(value, SafeDict):
                value = SafeDict(self.manager, value, f"{self.path}.{key}" if self.path else key)
                super().__setitem__(key, value)
            return value
        except KeyError:
            defaultConfig = self.manager.getDefaultConfig()
            
            currentDefault = defaultConfig
            if self.path:
                for part in self.path.split("."):
                    if part in currentDefault and isinstance(currentDefault[part], dict):
                        currentDefault = currentDefault[part]
                    else:
                        currentDefault = {}
                        break
            
            if key in currentDefault:
                default_value = currentDefault[key]
            else:
                default_value = None
            
            if isinstance(default_value, dict):
                default_value = SafeDict(self.manager, default_value, f"{self.path}.{key}" if self.path else key)
            
            super().__setitem__(key, default_value)
            
            self.manager.saveConfig()
            
            return default_value
    
    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, SafeDict):
            value = SafeDict(self.manager, value, f"{self.path}.{key}" if self.path else key)
        super().__setitem__(key, value)
        self.manager.saveConfig()
    
    def update(self, other_dict):
        for key, value in other_dict.items():
            self[key] = value
        self.manager.saveConfig()
    
    def to_dict(self):
        result = {}
        for key, value in self.items():
            if isinstance(value, SafeDict):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

class ConfigManager:
    def __init__(self):
        self.configPath = configPath
        self.defaultConfigPath = defaultConfigPath
        self.remoteConfigUrl = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/api/defaultConfig.json"
        
        self._configData = SafeDict(self, {})
        self.loadConfig()
        self.validateConfig()
        self.checkRemoteUpdates()
    
    def loadConfig(self):
        if not os.path.exists(self.configPath):
            self.copyDefaultConfig()
            return
        
        with open(self.configPath, "r") as config:
            try:
                data = json.load(config)
                self._configData.update(data)
            except json.JSONDecodeError:
                self.repairCorruptedConfig()
    
    def copyDefaultConfig(self):
        if os.path.exists(self.defaultConfigPath):
            with open(self.defaultConfigPath, "r") as f:
                data = json.load(f)
                self._configData.update(data)
            self.saveConfig()
        else:
            self._configData = SafeDict(self, {})
            self.saveConfig()
    
    def repairCorruptedConfig(self):
        if os.path.exists(self.defaultConfigPath):
            with open(self.defaultConfigPath, "r") as f:
                data = json.load(f)
                self._configData = SafeDict(self, data)
            self.saveConfig()
        else:
            self._configData = SafeDict(self, {})
            self.saveConfig()
    
    def getDefaultConfig(self):
        localDefault = {}
        if os.path.exists(self.defaultConfigPath):
            with open(self.defaultConfigPath, "r") as f:
                localDefault = json.load(f)
        
        remoteDefault = {}
        try:
            response = requests.get(self.remoteConfigUrl, timeout=5)
            if response.status_code == 200:
                remoteDefault = response.json()
        except:
            pass
        
        return remoteDefault or localDefault
    
    def validateConfig(self):
        defaultConfig = self.getDefaultConfig()
        updated = False
        
        def deepMerge(target, source, path=""):
            nonlocal updated
            for key, value in source.items():
                if key not in target:
                    target[key] = value
                    updated = True
                elif isinstance(value, dict) and isinstance(target.get(key), dict):
                    deepMerge(target[key], value, f"{path}.{key}" if path else key)
        
        deepMerge(self._configData, defaultConfig)
        
        if updated:
            self.saveConfig()
    
    def checkRemoteUpdates(self):
        try:
            response = requests.get(self.remoteConfigUrl, timeout=5)
            if response.status_code == 200:
                remoteConfig = response.json()
                self.validateAgainstRemote(remoteConfig)
        except:
            pass
    
    def validateAgainstRemote(self, remoteConfig):
        updated = False
        
        def deepCheck(target, source, path=""):
            nonlocal updated
            for key, value in source.items():
                if key not in target:
                    target[key] = value
                    updated = True
                elif isinstance(value, dict) and isinstance(target.get(key), dict):
                    deepCheck(target[key], value, f"{path}.{key}" if path else key)
        
        deepCheck(self._configData, remoteConfig)
        
        if updated:
            self.saveConfig()
    
    def saveConfig(self):
        with open(self.configPath, "w") as file:
            json.dump(self._configData.to_dict(), file, indent=2)
    
    def __getitem__(self, key):
        return self._configData[key]
    
    def __setitem__(self, key, value):
        self._configData[key] = value
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    
    def save(self):
        self.saveConfig()

configData = ConfigManager()