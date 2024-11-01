#!/bin/bash

rm -r nanoMIDIPlayer.dmg 

create-dmg \
    --volname "nanoMIDIPlayer" \
    --volicon "../../assets/icon.ico" \
    --background "../../assets/background.png" \
    --window-pos 200 120 \
    --window-size 625 400 \
    --icon-size 128 \
    --icon "nanoMIDIPlayer.app" 150 200 \
    --hide-extension "nanoMIDIPlayer.app" \
    --app-drop-link 475 200 \
    "./nanoMIDIPlayer.dmg" \
    "./dmg/nanoMIDIPlayer.app"
