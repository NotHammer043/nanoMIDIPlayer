@ECHO OFF
:MENU
ECHO.
ECHO Select an option:
ECHO 1 - nanoMIDIPlayer
ECHO 2 - Bootstrapper
SET /P option=Which to build: 

IF "%option%"=="1" (
    ECHO building nanoMIDIPlayer...
    pyinstaller --onefile --icon="./assets/icon.png" --hidden-import=mido.backends.rtmidi --noconsole nanoMIDIPlayer.py
    GOTO END
) ELSE IF "%option%"=="2" (
    ECHO building Bootstrapper...
    pyinstaller --onefile --icon="./assets/icon.png" --noconsole bootstrapper.py
    GOTO END
) ELSE (
    ECHO Invalid option. Please select 1 or 2.
    GOTO MENU
)

:END
PAUSE
