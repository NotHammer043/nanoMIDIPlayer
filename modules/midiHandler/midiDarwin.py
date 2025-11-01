import re
import keyboard
import mido
import os
import threading
import time
import random

from pynput import keyboard as pynputKeyboard
from modules.functions import mainFunctions
from modules import configuration

pressedKeys = set()
heldKeys = set()
activeTransposedNotes = {}

log = mainFunctions.log

def logKeys(action, key):
    if isinstance(key, pynputKeyboard.Key):
        keyName = key.name if key.name else str(key)
    else:
        keyName = str(key)
    if action == "press":
        pressedKeys.add(keyName)
    elif action == "release" and keyName in pressedKeys:
        pressedKeys.remove(keyName)
    if pressedKeys:
        log(f"{action}: {'+'.join(sorted(pressedKeys))}")
    else:
        log(f"{action}: {keyName}")

specialKeyMap = {
    "shift": pynputKeyboard.Key.shift,
    "ctrl": pynputKeyboard.Key.ctrl,
    "alt": pynputKeyboard.Key.alt,
    "space": pynputKeyboard.Key.space
}

pynputController = pynputKeyboard.Controller()
blockedKeys = {f"f{i}" for i in range(1, 13)} | {"tab", "backspace", "esc"}

def translateKey(key):
    keyLower = key.lower() if isinstance(key, str) else key
    if isinstance(keyLower, str) and keyLower in specialKeyMap:
        return specialKeyMap[keyLower]
    elif isinstance(keyLower, str) and len(keyLower) == 1:
        return keyLower
    elif isinstance(key, pynputKeyboard.Key):
        return key
    else:
        raise ValueError(f"Unsupported key: {key}")

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
    keyObj = translateKey(key)
    if isinstance(keyObj, str) and (keyObj.isdigit() or keyObj in ["ctrl", "shift"]):
        keyboard.press(keyObj)
        logKeys("press", keyObj)
    else:
        if isBlockedKey(keyObj):
            return
        pynputController.press(keyObj)
        logKeys("press", keyObj)
        heldKeys.add(keyObj)

def release(key):
    keyObj = translateKey(key)
    if isinstance(keyObj, str) and (keyObj.isdigit() or keyObj in ["ctrl", "shift"]):
        keyboard.release(keyObj)
        logKeys("release", keyObj)
    else:
        if isBlockedKey(keyObj):
            return
        pynputController.release(keyObj)
        logKeys("release", keyObj)
        if keyObj in heldKeys:
            heldKeys.remove(keyObj)

stopEvent = threading.Event()
clockThreadRef = None
keyboardHandlers = []
timerList = []

closeThread = False
paused = False
playThread = None
playbackSpeed = 1.0
sustainActive = False

def findVelocityKey(velocity):
    velocityMap = configuration.configData["midiPlayer"]["pianoMap"]["velocityMap"]
    thresholds = sorted(int(k) for k in velocityMap.keys())
    minimum = 0
    maximum = len(thresholds) - 1
    index = 0
    while minimum <= maximum:
        index = (minimum + maximum) // 2
        if index == 0 or index == len(thresholds) - 1:
            break
        if thresholds[index] < velocity:
            minimum = index + 1
        else:
            maximum = index - 1
    return velocityMap[str(thresholds[index])]

def pressAndMaybeRelease(key):
    press(key)
    if configuration.configData["midiPlayer"]["customHoldLength"]["enabled"]:
        t = threading.Timer(configuration.configData["midiPlayer"]["customHoldLength"]["noteLength"], lambda: release(key))
        timerList.append(t)
        t.start()

def simulateKey(msgType, note, velocity):
    if not -15 <= note - 36 <= 88:
        log(f"out of range: {note}")
        return
    key = None
    letterNoteMap = configuration.configData["midiPlayer"]["pianoMap"]["61keyMap"]
    lowNotes = configuration.configData["midiPlayer"]["pianoMap"]["88keyMap"]["lowNotes"]
    highNotes = configuration.configData["midiPlayer"]["pianoMap"]["88keyMap"]["highNotes"]
    if str(note) in letterNoteMap:
        key = letterNoteMap[str(note)]
    elif str(note) in lowNotes:
        key = lowNotes[str(note)]
    elif str(note) in highNotes:
        key = highNotes[str(note)]
    if not key:
        log(f"no mapping: {note}")
        return
    if msgType == "note_on":
        if configuration.configData["midiPlayer"]["velocity"]:
            velocityKey = findVelocityKey(velocity)
            press("alt")
            press(velocityKey)
            release(velocityKey)
            release("alt")
        if 36 <= note <= 96:
            if configuration.configData["midiPlayer"]["noDoubles"]:
                if re.search("[!@$%^*(]", key):
                    release(letterNoteMap[str(note - 1)])
                else:
                    release(key.lower())
            if re.search("[!@$%^*(]", key):
                press("shift")
                pressAndMaybeRelease(letterNoteMap[str(note - 1)])
                release("shift")
            elif key.isupper():
                press("shift")
                pressAndMaybeRelease(key.lower())
                release("shift")
            else:
                pressAndMaybeRelease(key)
        else:
            release(key.lower())
            press("ctrl")
            pressAndMaybeRelease(key.lower())
            release("ctrl")
    elif msgType == "note_off":
        if 36 <= note <= 96:
            if re.search("[!@$%^*(]", key):
                release(letterNoteMap[str(note - 1)])
            else:
                release(key.lower())
        else:
            release(key.lower())

def parseMidi(message):
    global sustainActive
    if message.type == "control_change" and configuration.configData["midiPlayer"]["sustain"]:
        if not sustainActive and message.value > configuration.configData["midiPlayer"]["sustainCutoff"]:
            sustainActive = True
            press("space")
        elif sustainActive and message.value < configuration.configData["midiPlayer"]["sustainCutoff"]:
            sustainActive = False
            release("space")
    elif message.type in ("note_on", "note_off"):
        try:
            if message.velocity == 0:
                simulateKey("note_off", message.note, message.velocity)
            else:
                simulateKey(message.type, message.note, message.velocity)
        except IndexError:
            pass

def playMidiOnce(midiFile):
    global sustainActive
    mid = mido.MidiFile(midiFile)
    startTime = time.monotonic()
    currentTime = 0
    for msg in mid:
        if stopEvent.is_set() or closeThread:
            return False
        adjustedDelay = msg.time / playbackSpeed
        if configuration.configData["midiPlayer"]["randomFail"]["enabled"] and not msg.is_meta:
            if random.random() < configuration.configData["midiPlayer"]["randomFail"]["speed"] / 100:
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
        if hasattr(msg, "note"):
            if msg.type == "note_on" and msg.velocity > 0:
                if configuration.configData["midiPlayer"]["randomFail"]["enabled"] and random.random() < configuration.configData["midiPlayer"]["randomFail"]["transpose"] / 100:
                    delta = random.randint(-12, 12)
                    newNote = msg.note + delta
                    if msg.note not in activeTransposedNotes:
                        activeTransposedNotes[msg.note] = []
                    activeTransposedNotes[msg.note].append(newNote)
                    original = msg.note
                    msg.note = newNote
                    parseMidi(msg)
                    msg.note = original
                    continue
            if msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                if msg.note in activeTransposedNotes and activeTransposedNotes[msg.note]:
                    transNote = activeTransposedNotes[msg.note].pop(0)
                    if not activeTransposedNotes[msg.note]:
                        del activeTransposedNotes[msg.note]
                    original = msg.note
                    msg.note = transNote
                    parseMidi(msg)
                    msg.note = original
                    continue
        parseMidi(msg)
    return True

def playMidiFile(midiFile):
    log("nanoMIDI Mid2VK Translator v3.0")
    log(f"Playing MIDI file: {midiFile}")
    while not (stopEvent.is_set() or closeThread):
        finished = playMidiOnce(midiFile)
        if not configuration.configData["midiPlayer"]["loopSong"] or not finished or stopEvent.is_set() or closeThread:
            break
        for key in list(heldKeys):
            release(key)

    if not configuration.configData["midiPlayer"]["loopSong"]:
        from modules.functions.midiPlayerFunctions import stopPlayback
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

def startPlayback(midiFile, updateCallback=None):
    global playThread, stopEvent, clockThreadRef, closeThread, paused
    stopEvent.clear()
    closeThread = False
    paused = False
    if playThread is not None and isinstance(playThread, threading.Thread) and playThread.is_alive():
        return
    totalSeconds = mido.MidiFile(midiFile).length
    playThread = threading.Thread(target=playMidiFile, args=(midiFile,), daemon=True)
    clockThreadRef = threading.Thread(target=clockThread, args=(totalSeconds, updateCallback), daemon=True)
    clockThreadRef.start()
    playThread.start()

def pausePlayback():
    global paused
    paused = not paused
    if paused and configuration.configData["midiPlayer"]["releaseOnPause"]:
        for key in list(heldKeys):
            release(key)
    log("Playback paused." if paused else "Playback resumed.")

def changeSpeed(amount):
    global playbackSpeed
    playbackSpeed = max(0.1, min(5.0, playbackSpeed + amount))
    log(f"Speed: {playbackSpeed * 100:.0f}%")

def stopPlayback():
    global closeThread, stopEvent, playThread, clockThreadRef, keyboardHandlers, timerList
    if closeThread or stopEvent.is_set():
        return
    
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
    log("Playback fully stopped.")