@ECHO OFF
nuitka --onefile --windows-icon-from-ico="./assets/icon.ico" --windows-disable-console --enable-plugin=tk-inter nanoMIDIPlayer.py
PAUSE