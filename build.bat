@ECHO OFF
pyinstaller --onefile --icon="./assets/icon.ico" --hidden-import=mido.backends.rtmidi --noconsole nanoMIDIPlayer.py
PAUSE
