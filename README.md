# nanoMIDIPlayer

**nanoMIDIPlayer** is a lightweight application designed to play MIDI files directly to a MIDI Output. Mainly designed for "[LoopBe1](https://nerds.de/data/setuploopbe1.exe)" and "[MIDI to QWERTY](https://github.com/ArijanJ/miditoqwerty/releases/)".

# ⚠️ nanoMIDIPlayer is highly flagged by [Windows Defender][Windows Defender](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and scanning tools like [VirusTotal](https://www.virustotal.com/) due to the way the Executable is Compiled! (Nuitka Obfuscator makes it worst, i only used it because it could compile with the packages)

## Showcase

https://github.com/NotHammer043/nanoMIDIPlayer/assets/107131733/a970179f-d417-4e1c-9ee8-bb3545a42313

## Prerequisites

- [LoopBe1](https://nerds.de/data/setuploopbe1.exe)
- [MIDI to QWERTY](https://github.com/ArijanJ/miditoqwerty/releases/)

## AutoPiano Setup

**1.** Download and install [LoopBe1](https://nerds.de/data/setuploopbe1.exe)

**2.** Download and extract [MIDI to QWERTY](https://github.com/ArijanJ/miditoqwerty/releases/)

**3.** Run [MIDI to QWERTY](https://github.com/ArijanJ/miditoqwerty/releases/) and set the **MIDI Input** to **LoopBe Internal MIDI**

**4.** Download the latest copy of [nanoMIDIPlayer.exe](https://github.com/NotHammer043/nanoMIDIPlayer/releases) from [Releases](https://github.com/NotHammer043/nanoMIDIPlayer/releases)

**5.** Run [nanoMIDIPlayer.exe](https://github.com/NotHammer043/nanoMIDIPlayer/releases) and select [LoopBe1](https://nerds.de/data/setuploopbe1.exe) **from MIDI Output** (if its not selected already)

**6.** Select a MIDI File and click **PLAY** (Default Hotkey F1 "*modifiable*")

**VIDEO TUTORIAL**

https://www.youtube.com/watch?v=coS4-w0SScE

# Contribution

contribute plz im bad at coding

- [ ]  Pause/Resume
- [ ]  MIDI Files Hub
- [ ]  Multiple MIDI selection (for mixing 2 or more songs like F1 for song1 and F2 for song2)
- [ ]  idk

# Building
**REQUIREMENTS**

* [VS BuildTools C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
* [Python 3.11.4](https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe)
* requirements.txt
```
customtkinter==5.2.2
keyboard==0.13.5
mido==1.3.2
Pillow==9.4.0
Pillow==10.2.0
```
* Nuitka (Compiler)
```
pip install nuitka
```

**BUILD**
```
nuitka --onefile --windows-icon-from-ico="./icon.ico" --enable-plugin=tk-inter --include-module=mido.backends.rtmidi --windows-disable-console nanoMIDIPlayer.py
```
