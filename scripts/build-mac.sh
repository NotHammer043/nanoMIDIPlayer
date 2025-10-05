#!/bin/bash

echo "=> Cleaning up previous builds..."
rm -rf ./build/
rm -rf ./dist/
mkdir build
mkdir dist

echo "=> Creating virtual environment..."
python3 -m venv venv-mac

echo "=> Activating virtual environment..."
source ./venv-mac/bin/activate

echo "=> Installing dependencies via pip..."
venv-mac/bin/pip install --upgrade pip pyinstaller
venv-mac/bin/pip install -r requirements.txt

echo "=> Running PyInstaller to create .app package..."
pyinstaller --onefile --noconsole --noconfirm \
    --hidden-import=mido.backends.rtmidi \
    --hidden-import=tkinter \
    --hidden-import=_tkinter \
    --add-data="assets:assets" \
    --paths="." \
    --name="nanoMIDIPlayer" \
    --icon="assets/icons/integrated/icon.ico" \
    main.py

echo "=> Setting executable permissions..."
chmod +x dist/nanoMIDIPlayer.app

echo " => Creating dmg..."
mkdir -p dist/macOS-dmg
mv dist/nanoMIDIPlayer.app dist/macOS-dmg/nanoMIDIPlayer.app
ln -s /Applications dist/macOS-dmg

if ! command -v create-dmg &> /dev/null; then
    echo "=> Installing create-dmg..."
    brew install create-dmg
fi

rm -f dist/nanoMIDIPlayer.dmg

create-dmg \
    --volname "nanoMIDIPlayer" \
    --volicon "assets/icons/integrated/icon.ico" \
    --background "assets/icons/integrated/dmgbackground.png" \
    --window-pos 200 120 \
    --window-size 625 400 \
    --icon-size 128 \
    --icon "nanoMIDIPlayer.app" 150 200 \
    --hide-extension "nanoMIDIPlayer.app" \
    --app-drop-link 475 200 \
    "dist/nanoMIDIPlayer.dmg" \
    "dist/macOS-dmg/nanoMIDIPlayer.app"

echo " => Cleaning up temporary files..."
rm -rf __pycache__ build venv-mac *.spec

echo " => Done! .dmg available in 'dist/nanoMIDIPlayer.dmg'."
