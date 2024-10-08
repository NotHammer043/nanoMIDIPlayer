
# nanoMIDIPlayer

  

**nanoMIDIPlayer** is a MIDI Player that can either simulate QWERTY keys or send MIDI directly to Output MIDI Devices.
  

## Showcase

  


https://github.com/NotHammer043/nanoMIDIPlayer/assets/107131733/1b12c130-8a94-40d5-863a-61961f70fa5f


https://github.com/user-attachments/assets/84e9d8b1-2f60-41e9-8f5c-078aeadd7ecc




  

## nanoMIDIPlayer Setup // DOWNLOAD

**1.** Download the latest copy of [nanoMIDIPlayer.exe](https://github.com/NotHammer043/nanoMIDIPlayer/releases) from [Releases](https://github.com/NotHammer043/nanoMIDIPlayer/releases)

  

**2.** Run [nanoMIDIPlayer.exe](https://github.com/NotHammer043/nanoMIDIPlayer/releases) and select a **MIDI File** or find one from **MIDI Hub**

  

**6.** Focus on your Virtual Piano game/app and click **PLAY** (Default Hotkey F1 "*modifiable*")

  

# Building

**REQUIREMENTS**

  

* [VS BuildTools C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

* [Python 3.11.4](https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe)

* requirements.txt

```
customtkinter
Pillow
mido
pynput
requests
python-rtmidi
```

* PyInstaller (Compiler)

```
pip install pyinstaller
```

  

**BUILD**

```
pyinstaller --onefile --icon="./assets/icon.ico" --hidden-import=mido.backends.rtmidi --noconsole nanoMIDIPlayer.py
```

**Debugging**

```
nanoMIDIPlayer.exe --debug
```

**Beta Testers**
- **redxyzxd**
- **sherben10**
- **nictiser**
- **somecoolname2**
- **obanaiserpenthashira**
- **x.bunn**
- **10cryptic**
- **xaydd**
- **somecoolname2**
- **obanaiserpenthashira**


[![Star History Chart](https://api.star-history.com/svg?repos=NotHammer043/nanoMIDIPlayer&type=Date)](https://star-history.com/#NotHammer043/nanoMIDIPlayer&Date)
