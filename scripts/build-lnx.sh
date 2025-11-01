#!/bin/bash

echo "=> Cleaning up previous builds..."
rm -rf ./build/
rm -rf ./dist/
mkdir build
mkdir dist

echo "=> Creating virtual environment..."
python3 -m venv venv-lnx

echo "=> Activating virtual environment..."
source ./venv-lnx/bin/activate

echo "=> Installing dependencies via pip..."
venv-lnx/bin/pip install --upgrade pip pyinstaller
venv-lnx/bin/pip install -r requirements.txt

echo "=> Running PyInstaller to create binary..."
pyinstaller --onefile --noconsole --noconfirm \
    --hidden-import=mido.backends.rtmidi \
    --add-data="assets/:assets" \
    --paths="." \
    --name=nanoMIDIPlayer \
    --icon="assets/icons/integrated/icon.ico" \
    main.py

echo " => Packaging executable as tar.gz archive..."
cd dist
tar -czvf nanoMIDIPlayer.tar.gz nanoMIDIPlayer
cd ..

echo " => Cleaning up temporary files..."
rm -rf __pycache__ build venv-lnx *.spec

echo " => Done! Packaged tar.gz is available in 'dist/OnTheSpot.tar.gz'."
