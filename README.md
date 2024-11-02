
# nanoMIDIPlayer

  

**nanoMIDIPlayer** is a MIDI Player that can either simulate QWERTY keys or send MIDI directly to Output MIDI Devices.
  

## Showcase



https://github.com/user-attachments/assets/84e9d8b1-2f60-41e9-8f5c-078aeadd7ecc


# MACOS


https://github.com/user-attachments/assets/7a701085-2c07-479b-92ae-fedcfcabe669




  

## nanoMIDIPlayer Setup // DOWNLOAD

**1.** Download the latest copy of [nanoMIDIPlayer.exe](https://github.com/NotHammer043/nanoMIDIPlayer/releases) from [Releases](https://github.com/NotHammer043/nanoMIDIPlayer/releases)

  

**2.** Run [nanoMIDIPlayer.exe](https://github.com/NotHammer043/nanoMIDIPlayer/releases) and select a **MIDI File** or find one from **MIDI Hub**

  

**6.** Focus on your Virtual Piano game/app and click **PLAY** (Default Hotkey F1 "*modifiable*")


# Why is this program detected as a virus?
- Open source programs such as this program are commonly detected as viruses because actual malware may be using the same libaries as this one. Getting this software to not get detected as a virus will cost us 300$/year. You can freely check if the code contains any malicious stuff.
  

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
