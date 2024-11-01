#!/bin/bash

/Users/nothammer/Desktop/nanoMIDIPlayer/venv2/bin/python -m PyInstaller --onefile --icon="./assets/icon.png" --hidden-import=mido.backends.rtmidi --noconsole --noconfirm ./nanoMIDIPlayer.py