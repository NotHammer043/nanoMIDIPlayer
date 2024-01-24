@ECHO OFF
nuitka --onefile --windows-icon-from-ico="./icon.ico" --enable-plugin=tk-inter --include-module=mido.backends.rtmidi --windows-disable-console nanoMIDIPlayer.py
PAUSE
