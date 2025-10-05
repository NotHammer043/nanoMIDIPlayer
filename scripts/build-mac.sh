#!/bin/bash
set -e

ARCH="arm64"
if [[ "$1" == "--arch" && -n "$2" ]]; then
  ARCH="$2"
fi

echo "=> Building for architecture: $ARCH"

echo "=> Cleaning up previous builds..."
rm -rf ./build/ ./dist/ ./__pycache__ *.spec
mkdir -p build dist

if [ ! -d "venv-mac" ]; then
  echo "=> Creating virtual environment..."
  python3 -m venv venv-mac
fi

echo "=> Activating virtual environment..."
source ./venv-mac/bin/activate

echo "=> Installing dependencies via pip..."
pip install --upgrade pip setuptools wheel pyinstaller
pip install -r requirements.txt customtkinter

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
chmod +x dist/nanoMIDIPlayer || true

echo "=> Preparing DMG staging directory..."
mkdir -p dist/macOS-dmg
mv dist/nanoMIDIPlayer dist/macOS-dmg/nanoMIDIPlayer.app
ln -sf /Applications dist/macOS-dmg/

if ! command -v create-dmg &> /dev/null; then
  echo "=> create-dmg not found in PATH. Please ensure it is installed by CI."
  exit 1
fi

DMG_PATH="dist/nanoMIDIPlayer-${ARCH}.dmg"
rm -f "$DMG_PATH"

echo "=> Creating DMG at $DMG_PATH..."
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
  "$DMG_PATH" \
  "dist/macOS-dmg"

echo "=> Cleaning up temporary files..."
rm -rf build __pycache__ *.spec venv-mac

echo "=> Done! DMG available at $DMG_PATH"
