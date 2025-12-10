import mido
import threading
import time
import random

from modules.functions import mainFunctions
from modules import configuration

activeTransposedNotes = {}
activeNotes = set()
stopEvent = threading.Event()
clockThreadRef = None
timerList = []
closeThread = False
paused = False
playThread = None
playbackSpeed = 1.0
sustainActive = False
midiOut = None

log = mainFunctions.log

def noteAllowed(note):
    allow88 = configuration.configData["midiPlayer"]["88Keys"]
    maps = configuration.configData["midiPlayer"]["pianoMap"]
    if not allow88:
        return str(note) in maps["61keyMap"]
    return str(note) in maps["61keyMap"] or str(note) in maps["88keyMap"]["lowNotes"] or str(note) in maps["88keyMap"]["highNotes"]

def parseMidi(message):
    global sustainActive, activeNotes
    log(str(message))

    if message.type == "control_change":
        if message.control == 64:
            if not configuration.configData["midiPlayer"]["sustain"]:
                return
            if message.value > configuration.configData["midiPlayer"]["sustainCutoff"]:
                sustainActive = True
                if midiOut:
                    midiOut.send(message)
            else:
                sustainActive = False
                if midiOut:
                    midiOut.send(message)
            return

    if message.type in ("note_on", "note_off"):
        note = message.note
        if not noteAllowed(note):
            log(f"out of range: {note}")
            return

        if message.type == "note_on":
            if message.velocity == 0:
                msgType = "note_off"
            else:
                msgType = "note_on"
        else:
            msgType = "note_off"

        if msgType == "note_on" and not configuration.configData["midiPlayer"]["velocity"]:
            message.velocity = 78
        elif msgType == "note_off":
            message.velocity = 0

        channel = message.channel if hasattr(message, "channel") else 0
        key = (note, channel)

        if configuration.configData["midiPlayer"]["noDoubles"]:
            if msgType == "note_on" and key in activeNotes:
                log(f"skipped double: note {note} ch {channel}")
                return

        if msgType == "note_on":
            activeNotes.add(key)
        if msgType == "note_off" and key in activeNotes:
            activeNotes.remove(key)

        if midiOut:
            midiOut.send(message)

def playMidiOnce(midiFile):
    global sustainActive
    mid = mido.MidiFile(midiFile, clip=True)
    startTime = time.monotonic()
    currentTime = 0
    for msg in mid:
        if stopEvent.is_set() or closeThread:
            return False

        adjustedDelay = msg.time / playbackSpeed
        if configuration.configData["midiPlayer"]["randomFail"]["enabled"] and not msg.is_meta:
            if random.random() < configuration.configData["midiPlayer"]["randomFail"]["speed"] / 100:
                adjustedDelay *= random.uniform(0.5, 1.5)

        currentTime += adjustedDelay
        targetTime = startTime + currentTime

        while time.monotonic() < targetTime:
            if stopEvent.is_set() or closeThread:
                return False
            while paused and not (stopEvent.is_set() or closeThread):
                pauseStart = time.monotonic()
                time.sleep(0.05)
                delta = time.monotonic() - pauseStart
                startTime += delta
                targetTime += delta
            remaining = targetTime - time.monotonic()
            if remaining > 0:
                time.sleep(min(remaining, 0.005))

        if msg.is_meta:
            continue

        if hasattr(msg, "note"):
            n = msg.note

            if not noteAllowed(n):
                log(f"out of range: {n}")
                continue

            if msg.type == "note_on" and msg.velocity > 0:
                if configuration.configData["midiPlayer"]["randomFail"]["enabled"]:
                    if random.random() < configuration.configData["midiPlayer"]["randomFail"]["transpose"] / 100:
                        delta = random.randint(-12, 12)
                        newNote = n + delta
                        if not noteAllowed(newNote):
                            log(f"out of range: {newNote}")
                            continue
                        if n not in activeTransposedNotes:
                            activeTransposedNotes[n] = []
                        activeTransposedNotes[n].append(newNote)
                        original = msg.note
                        msg.note = newNote
                        parseMidi(msg)
                        msg.note = original
                        continue

            if msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                if n in activeTransposedNotes and activeTransposedNotes[n]:
                    transNote = activeTransposedNotes[n].pop(0)
                    if not activeTransposedNotes[n]:
                        del activeTransposedNotes[n]
                    if noteAllowed(transNote):
                        original = msg.note
                        msg.note = transNote
                        parseMidi(msg)
                        msg.note = original
                    else:
                        log(f"out of range: {transNote}")
                    continue

        parseMidi(msg)

    return True

def playMidiFile(midiFile):
    log("nanoMIDI Direct MIDI Out v1.0")
    log(f"Playing MIDI file: {midiFile}")

    while not (stopEvent.is_set() or closeThread):
        finished = playMidiOnce(midiFile)

        if stopEvent.is_set() or closeThread:
            break

        if not finished:
            break

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

def startPlayback(midiFile, outputDevice, updateCallback=None):
    global playThread, stopEvent, clockThreadRef, closeThread, paused, midiOut
    stopEvent.clear()
    closeThread = False
    paused = False
    if playThread is not None and isinstance(playThread, threading.Thread) and playThread.is_alive():
        return
    midiOut = mido.open_output(outputDevice)
    totalSeconds = mido.MidiFile(midiFile, clip=True).length
    playThread = threading.Thread(target=playMidiFile, args=(midiFile,), daemon=True)
    clockThreadRef = threading.Thread(target=clockThread, args=(totalSeconds, updateCallback), daemon=True)
    clockThreadRef.start()
    playThread.start()

def pausePlayback():
    global paused
    paused = not paused
    log("Playback paused." if paused else "Playback resumed.")

def changeSpeed(amount):
    global playbackSpeed
    playbackSpeed = max(0.1, min(5.0, playbackSpeed + amount))
    log(f"Speed: {playbackSpeed * 100:.0f}%")

def stopPlayback():
    global closeThread, stopEvent, playThread, clockThreadRef, timerList, midiOut, activeNotes
    if stopEvent.is_set():
        return
    stopEvent.set()
    closeThread = True
    for t in list(timerList):
        try:
            t.cancel()
        except:
            pass
    timerList.clear()
    if playThread is not None and isinstance(playThread, threading.Thread):
        try:
            playThread.join(timeout=1.0)
        except:
            pass
    if clockThreadRef is not None and isinstance(clockThreadRef, threading.Thread):
        try:
            clockThreadRef.join(timeout=1.0)
        except:
            pass
    if midiOut:
        try:
            for note, channel in list(activeNotes):
                midiOut.send(mido.Message("note_off", note=note, velocity=0, channel=channel))
            activeNotes.clear()
            midiOut.close()
        except:
            pass
        midiOut = None
    log("Playback fully stopped.")
