import re
import keyboard
import mido
import threading

from pynput import keyboard as pynputKeyboard
from modules.functions import mainFunctions
from modules import configuration

pressedKeys = set()
heldKeys = set()
activeTransposedNotes = {}

log = mainFunctions.log

inPort = None
midiThread = None

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

if configuration.configData["midiToQwerty"]["inputModule"] == "keyboard":
    def press(key):
        keyboard.press(key)
        logKeys("press", key)
    def release(key):
        keyboard.release(key)
        logKeys("release", key)

elif configuration.configData["midiToQwerty"]["inputModule"] == "pynput":
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
            raise ValueError(f"Unsupported key for pynput: {key}")

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
        if isBlockedKey(keyObj):
            return
        pynputController.press(keyObj)
        logKeys("press", keyObj)
        heldKeys.add(keyObj)

    def release(key):
        keyObj = translateKey(key)
        if isBlockedKey(keyObj):
            return
        pynputController.release(keyObj)
        logKeys("release", keyObj)
        if keyObj in heldKeys:
            heldKeys.remove(keyObj)

stopEvent = threading.Event()
keyboardHandlers = []
timerList = []
closeThread = False
sustainActive = False

def findVelocityKey(velocity):
    velocityMap = configuration.configData["midiToQwerty"]["pianoMap"]["velocityMap"]
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
    if configuration.configData["midiToQwerty"]["customHoldLength"]["enabled"]:
        t = threading.Timer(configuration.configData["midiToQwerty"]["customHoldLength"]["noteLength"], lambda: release(key))
        timerList.append(t)
        t.start()

def simulateKey(msgType, note, velocity):
    if not -15 <= note - 36 <= 88:
        log(f"out of range: {note}")
        return

    key = None
    letterNoteMap = configuration.configData["midiToQwerty"]["pianoMap"]["61keyMap"]
    lowNotes = configuration.configData["midiToQwerty"]["pianoMap"]["88keyMap"]["lowNotes"]
    highNotes = configuration.configData["midiToQwerty"]["pianoMap"]["88keyMap"]["highNotes"]

    if str(note) in letterNoteMap:
        key = letterNoteMap[str(note)]
    elif str(note) in lowNotes:
        key = lowNotes[str(note)]
    elif str(note) in highNotes:
        key = highNotes[str(note)]

    if not key:
        log(f"no mapping: {note}")
        return
    
    pianoWidget = mainFunctions.getApp().frames["miditoqwerty"].piano

    if msgType == "note_on":
        pianoWidget.down(note, velocity)

        if configuration.configData["midiToQwerty"]["velocity"]:
            velocityKey = findVelocityKey(velocity)
            press("alt")
            press(velocityKey)
            release(velocityKey)
            release("alt")

        if 36 <= note <= 96:
            if configuration.configData["midiToQwerty"]["noDoubles"]:
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
        pianoWidget.up(note)

        if 36 <= note <= 96:
            if re.search("[!@$%^*(]", key):
                release(letterNoteMap[str(note - 1)])
            else:
                release(key.lower())
        else:
            release(key.lower())

def parseMidi(message):
    global sustainActive
    if message.type == "control_change" and configuration.configData["midiToQwerty"]["sustain"]:
        if not sustainActive and message.value > configuration.configData["midiToQwerty"]["sustainCutoff"]:
            sustainActive = True
            press("space")
        elif sustainActive and message.value < configuration.configData["midiToQwerty"]["sustainCutoff"]:
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

def startMidiInput(portName=None):
    global inPort, midiThread, stopEvent, closeThread
    stopEvent.clear()
    closeThread = False
    log("nanoMIDI Mid2VK Translator v1.0 (Live Input)")
    try:
        if portName:
            inPort = mido.open_input(portName)
        else:
            inPort = mido.open_input()
    except Exception as e:
        log(f"Could not open MIDI input: {e}")
        return

    def midiLoop():
        for msg in inPort:
            if stopEvent.is_set() or closeThread:
                break
            parseMidi(msg)

    midiThread = threading.Thread(target=midiLoop, daemon=True)
    midiThread.start()
    return midiThread


def stopMidiInput():
    global closeThread, stopEvent, keyboardHandlers, timerList, inPort, midiThread
    stopEvent.set()
    closeThread = True

    if inPort:
        try:
            inPort.close()
        except Exception:
            pass
        inPort = None

    if midiThread and midiThread.is_alive():
        try:
            midiThread.join(timeout=1.0)
        except Exception:
            pass
        midiThread = None

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

    try:
        pianoWidget = mainFunctions.getApp().frames["miditoqwerty"].piano
        for note in pianoWidget.currentNotes():
            pianoWidget.up(note)
    except Exception:
        pass

    log("MIDI input stopped.")