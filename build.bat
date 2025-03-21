name: Build Windows Executable

on: [push]

jobs:
  build:
    runs-on: windows-latest  # Use Windows runner

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          architecture: 'x64'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Build executable
        uses: Martin005/pyinstaller-action@v1
        with:
          spec: nanoMIDIPlayer.py
          options: '--onefile, --icon=./assets/icon.png, --hidden-import=mido.backends.rtmidi, --noconsole'
          python_ver: '3.10'
          python_arch: 'x64'
          upload_exe_with_name: 'nanoMIDIPlayer_executable'

      - name: Upload executable
        uses: actions/upload-artifact@v3
        with:
          name: nanoMIDIPlayer.exe
          path: ./dist/nanoMIDIPlayer.exe
