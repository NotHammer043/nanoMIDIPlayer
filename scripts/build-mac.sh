#!/bin/bash
set -e

ARCH="arm"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --arch)
            ARCH="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 --arch [intel|arm]"
            exit 1
            ;;
    esac
done

if [[ "$ARCH" != "intel" && "$ARCH" != "arm" ]]; then
    echo "Invalid architecture: $ARCH"
    exit 1
fi

echo "Building nanoMIDIPlayer for macOS ($ARCH)"

rm -rf ./build ./dist ./venv-mac
mkdir -p build dist

python3 -m venv venv-mac
source ./venv-mac/bin/activate
pip install --upgrade pip setuptools wheel pyinstaller
pip install -r requirements.txt

if [[ "$ARCH" == "intel" ]]; then
    TARGET_ARCH="x86_64"
    APP_NAME="nanoMIDIPlayer-Intel"
    DMG_NAME="nanoMIDIPlayer-Intel.dmg"
else
    TARGET_ARCH="arm64"
    APP_NAME="nanoMIDIPlayer-ARM"
    DMG_NAME="nanoMIDIPlayer-ARM.dmg"
fi

pyinstaller --onefile --noconsole --noconfirm \
    --target-architecture "$TARGET_ARCH" \
    --hidden-import=mido.backends.rtmidi \
    --hidden-import=tkinter \
    --hidden-import=_tkinter \
    --add-data="assets:assets" \
    --paths="." \
    --name="$APP_NAME" \
    --icon="assets/icons/integrated/icon.ico" \
    main.py

chmod +x dist/$APP_NAME.app
mkdir -p dist/macOS-$ARCH
mv dist/$APP_NAME.app dist/macOS-$ARCH/
ln -s /Applications dist/macOS-$ARCH || true

if ! command -v create-dmg &> /dev/null; then
    brew install create-dmg
fi

rm -f dist/$DMG_NAME

create-dmg \
    --volname "$APP_NAME" \
    --volicon "assets/icons/integrated/icon.ico" \
    --background "assets/icons/integrated/dmgbackground.png" \
    --window-pos 200 120 \
    --window-size 625 400 \
    --icon-size 128 \
    --icon "$APP_NAME.app" 150 200 \
    --hide-extension "$APP_NAME.app" \
    --app-drop-link 475 200 \
    "dist/$DMG_NAME" \
    "dist/macOS-$ARCH/$APP_NAME.app"

rm -rf __pycache__ build venv-mac *.spec
echo "Build complete: dist/$DMG_NAME"
