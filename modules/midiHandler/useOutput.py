import mido
import threading
import time
import random

from modules.functions import mainFunctions
from modules import configuration

activeTransposedNotes = {}
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

def parseMidi(message):
    global sustainActive
    log(str(message))

    if message.type == "control_change" and configuration.configData["midiPlayer"]["sustain"]:
        if not sustainActive and message.value > configuration.configData["midiPlayer"]["sustainCutoff"]:
            sustainActive = True
            if midiOut:
                midiOut.send(message)
        elif sustainActive and message.value < configuration.configData["midiPlayer"]["sustainCutoff"]:
            sustainActive = False
            if midiOut:
                midiOut.send(message)
    elif message.type in ("note_on", "note_off"):
        if midiOut:
            midiOut.send(message)

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
            if remaining > 0.002:
                time.sleep(max(0, remaining - 0.001))
            else:
                time.sleep(0.0005)
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
    log("nanoMIDI Direct MIDI Out v1.0")
    log(f"Playing MIDI file: {midiFile}")
    while not (stopEvent.is_set() or closeThread):
        finished = playMidiOnce(midiFile)
        if not configuration.configData["midiPlayer"]["loopSong"] or not finished or stopEvent.is_set() or closeThread:
            break

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
    totalSeconds = mido.MidiFile(midiFile).length
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
    global closeThread, stopEvent, playThread, clockThreadRef, timerList, midiOut
    stopEvent.set()
    closeThread = True
    for t in list(timerList):
        try:
            t.cancel()
        except Exception:
            pass
    timerList.clear()
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

    if midiOut:
        try:
            for channel in range(16):
                for note in range(128):
                    midiOut.send(mido.Message("note_off", note=note, velocity=0, channel=channel))
            midiOut.close()
        except Exception:
            pass
        midiOut = None

    log("Playback fully stopped.")