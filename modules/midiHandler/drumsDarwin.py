import mido
import time
import random
import threading
import keyboard
from pynput import keyboard as pynputKeyboard

from modules import configuration
from modules.functions import mainFunctions

pressedKeys = set()
heldKeys = set()

log = mainFunctions.log
pynputController = pynputKeyboard.Controller()
blockedKeys = {f"f{i}" for i in range(1, 13)} | {"tab", "backspace", "esc"}

def logKeys(action, key):
    keyName = key.name if isinstance(key, pynputKeyboard.Key) and key.name else str(key)
    if action == "press":
        pressedKeys.add(keyName)
    elif action == "release" and keyName in pressedKeys:
        pressedKeys.remove(keyName)
    if pressedKeys:
        log(f"{action}: {'+'.join(sorted(pressedKeys))}")
    else:
        log(f"{action}: {keyName}")

def isBlockedKey(keyObj):
    if isinstance(keyObj, str):
        return keyObj.lower() in blockedKeys
    if isinstance(keyObj, pynputKeyboard.Key):
        name = getattr(keyObj, "name", None)
        if isinstance(name, str) and name.lower() in blockedKeys:
            return True
        s = str(keyObj).lower()
        if s.startswith("key.f") and any(s.startswith(f"key.f{i}") for i in range(1, 13)):
            return True
        return False
    return False

def press(key):
    if isinstance(key, str) and (key.isdigit() or key.lower() in ["shift", "ctrl"]):
        keyboard.press(key)
        logKeys("press", key)
    else:
        if isBlockedKey(key):
            return
        pynputController.press(key)
        logKeys("press", key)
        heldKeys.add(key)

def release(key):
    if isinstance(key, str) and (key.isdigit() or key.lower() in ["shift", "ctrl"]):
        keyboard.release(key)
        logKeys("release", key)
    else:
        if isBlockedKey(key):
            return
        pynputController.release(key)
        logKeys("release", key)
        if key in heldKeys:
            heldKeys.remove(key)

drumsMap = {
    42: configuration.configData['drumsMacro']['drumsMap']['closed_Hi-Hat'],
    44: configuration.configData['drumsMacro']['drumsMap']['closed_Hi-Hat2'],
    46: configuration.configData['drumsMacro']['drumsMap']['open_Hi-Hat'],
    48: configuration.configData['drumsMacro']['drumsMap']['tom1'],
    50: configuration.configData['drumsMacro']['drumsMap']['tom1_2'],
    60: configuration.configData['drumsMacro']['drumsMap']['tom'],
    62: configuration.configData['drumsMacro']['drumsMap']['tom2_2'],
    49: configuration.configData['drumsMacro']['drumsMap']['rightCrash'],
    55: configuration.configData['drumsMacro']['drumsMap']['leftCrash'],
    38: configuration.configData['drumsMacro']['drumsMap']['snare'],
    40: configuration.configData['drumsMacro']['drumsMap']['snare2'],
    37: configuration.configData['drumsMacro']['drumsMap']['snareSide'],
    35: configuration.configData['drumsMacro']['drumsMap']['kick'],
    36: configuration.configData['drumsMacro']['drumsMap']['kick2'],
    51: configuration.configData['drumsMacro']['drumsMap']['ride'],
    53: configuration.configData['drumsMacro']['drumsMap']['rideBell'],
    39: configuration.configData['drumsMacro']['drumsMap']['cowbell'],
    52: configuration.configData['drumsMacro']['drumsMap']['crashChina'],
    57: configuration.configData['drumsMacro']['drumsMap']['splashCrash'],
    45: configuration.configData['drumsMacro']['drumsMap']['lowTom'],
    47: configuration.configData['drumsMacro']['drumsMap']['lowMidTom'],
}

stopEvent = threading.Event()
clockThreadRef = None
playThread = None
timerList = []
paused = False
closeThread = False
playbackSpeed = 1.0
keyboardHandlers = []

def pressAndMaybeRelease(key):
    press(key)
    if configuration.configData["drumsMacro"]["customHoldLength"]["enabled"]:
        t = threading.Timer(configuration.configData["drumsMacro"]["customHoldLength"]["noteLength"], lambda: release(key))
        timerList.append(t)
        t.start()

def parseMidi(message):
    if message.type == 'note_on' and message.velocity > 0:
        key = drumsMap.get(message.note)
        if key is not None:
            pressAndMaybeRelease(key)
    elif message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):
        key = drumsMap.get(message.note)
        if key is not None:
            release(key)

def playMidiOnce(filePath):
    mid = mido.MidiFile(filePath, clip=True)
    startTime = time.monotonic()
    currentTime = 0
    for msg in mid:
        if stopEvent.is_set() or closeThread:
            return False
        adjustedDelay = msg.time / playbackSpeed
        if configuration.configData["drumsMacro"]["randomFail"]["enabled"] and not msg.is_meta:
            if random.random() < configuration.configData["drumsMacro"]["randomFail"]["speed"] / 100:
                speedFactor = random.uniform(0.5, 1.5)
                adjustedDelay *= speedFactor
        currentTime += adjustedDelay
        targetTime = startTime + currentTime
        while time.monotonic() < targetTime:
            if stopEvent.is_set() or closeThread:
                return False
            while paused and not (stopEvent.is_set() or closeThread):
                pauseStart = time.monotonic()
                time.sleep(0.05)
                pauseDuration = time.monotonic() - pauseStart
                startTime += pauseDuration
                targetTime += pauseDuration
            remaining = targetTime - time.monotonic()
            if remaining > 0:
                sleepChunk = min(remaining, 0.005)
                time.sleep(sleepChunk)
        if msg.is_meta:
            continue
        parseMidi(msg)
    return True

def playMidiFile(filePath):
    while not (stopEvent.is_set() or closeThread):
        finished = playMidiOnce(filePath)
        if not configuration.configData["drumsMacro"]["loopSong"] or not finished or stopEvent.is_set() or closeThread:
            break
        for key in list(heldKeys):
            release(key)

    if not configuration.configData["drumsMacro"]["loopSong"]:
        from modules.functions.drumsMacroFunctions import stopPlayback
        stopPlayback()

def formatTime(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:0}:{minutes:02}:{secs:02}"

def clockThread(totalSeconds, updateCallback=None):
    global closeThread, playbackSpeed, paused
    currentSeconds = 0
    while not (stopEvent.is_set() or closeThread):
        if not paused:
            shown = currentSeconds % max(1, int(totalSeconds))
            formattedTime = f"{formatTime(shown)} / {formatTime(totalSeconds)}"
            if configuration.configData['appUI']['timestamp']:
                if updateCallback:
                    updateCallback(formattedTime)
                else:
                    log(formattedTime)
            currentSeconds += 1
            for _ in range(10):
                if stopEvent.is_set() or closeThread:
                    break
                time.sleep(0.1 / playbackSpeed)
        else:
            time.sleep(0.1)

def startPlayback(filePath, updateCallback=None):
    global playThread, stopEvent, clockThreadRef, closeThread, paused
    stopEvent.clear()
    closeThread = False
    paused = False
    if playThread is not None and isinstance(playThread, threading.Thread) and playThread.is_alive():
        return
    totalSeconds = mido.MidiFile(filePath, clip=True).length
    playThread = threading.Thread(target=playMidiFile, args=(filePath,), daemon=True)
    clockThreadRef = threading.Thread(target=clockThread, args=(totalSeconds, updateCallback), daemon=True)
    clockThreadRef.start()
    playThread.start()

def pausePlayback():
    global paused
    paused = not paused
    if paused and configuration.configData["drumsMacro"]["releaseOnPause"]:
        for key in list(heldKeys):
            release(key)

def changeSpeed(amount):
    global playbackSpeed
    playbackSpeed = max(0.1, min(5.0, playbackSpeed + amount))
    log(f"Speed: {playbackSpeed * 100:.0f}%")

def stopPlayback():
    global closeThread, stopEvent, playThread, clockThreadRef, timerList, keyboardHandlers
    stopEvent.set()
    closeThread = True
    for key in list(heldKeys):
        try:
            release(key)
        except Exception:
            pass
    for t in list(timerList):
        try:
            t.cancel()
        except Exception:
            pass
    timerList.clear()
    try:
        for h in list(keyboardHandlers):
            try:
                keyboard.unhook(h)
            except Exception:
                pass
        keyboardHandlers.clear()
    except Exception:
        pass
    if playThread is not None and isinstance(playThread, threading.Thread):
        try:
            playThread.join(timeout=1.0)
        except Exception:
            pass
    if clockThreadRef is not None and isinstance(clockThreadRef, threading.Thread):
        try:
            clockThreadRef.join(timeout=1.0)
        except Exception:
            pass