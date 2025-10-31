@echo off

set FOLDER_NAME=%cd%
for %%F in ("%cd%") do set FOLDER_NAME=%%~nxF
if /i "%FOLDER_NAME%"=="scripts" (
    cd ..
)

echo =^> Cleaning up previous builds...
del /F /Q /A dist\bootstrapper.exe

echo =^> Creating virtual environment...
python -m venv venv-win

echo =^> Activating virtual environment...
call venv-win\Scripts\activate.bat

echo =^> Installing dependencies via pip...
python -m pip install --upgrade pip pyinstaller
pip install -r requirements.txt

echo =^> Running PyInstaller to create .exe package...
pyinstaller --onefile --noconsole --noconfirm ^
    --add-data="assets;assets" ^
    --paths="." ^
    --name="bootstrapper" ^
    --icon=assets\icons\integrated\icon.ico ^
    main.py

echo =^> Cleaning up temporary files...
del /F /Q *.spec
rmdir /s /q build __pycache__ venv-win

echo =^> Done! Executable available as 'dist/bootstrapper.exe'.