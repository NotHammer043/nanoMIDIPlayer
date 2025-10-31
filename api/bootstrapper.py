import requests
import threading
import customtkinter
import subprocess
import tkinter as tk
import time
import os
import sys
from PIL import Image

url = "https://github.com/NotHammer043/nanoMIDIPlayer/releases/latest/download/nanoMIDIPlayer.exe"
outputPath = "./nanoMIDIPlayer.exe"

def downloadFile(downloadUrl, outputPath, progressCallback):
    response = requests.get(downloadUrl, stream=True)
    size = int(response.headers.get('content-length', 0))
    downloadedSize = 0
    startTime = time.time()

    with open(outputPath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloadedSize += len(chunk)
            elapsedTime = time.time() - startTime
            speed = (downloadedSize / 1024) / elapsedTime if elapsedTime > 0 else 0
            progress = (downloadedSize / size) * 100
            progressCallback(progress, speed)
    return outputPath

def updateProgress(progress, speed):
    progressBar.update()
    status.configure(text=f"Downloading... ({int(progress)}%)\nSpeed: {speed:.2f} KBps")
    progressVar.set(int(progress) / 100)

def progressThread():
    progressVar.set(0)
    progressBar.update()
    downloadFile(url, outputPath, updateProgress)
    progressBar.update()
    status.configure(text="Download Complete\nStarting in 2.. 1")
    for i in range(2, 0, -1):
        status.configure(text=f"Download Complete\nStarting in {i}..")
        time.sleep(1)
    subprocess.Popen("./nanoMIDIPlayer.exe", creationflags=subprocess.CREATE_NEW_CONSOLE)
    os._exit(0)

def resourcePath(relativePath):
    if hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS
    else:
        basePath = os.path.abspath(".")
    return os.path.join(basePath, relativePath)

iconPath = resourcePath("assets/icons/integrated/icon.png")
bannerPath = resourcePath("assets/icons/integrated/banner.png")

bannerImage = Image.open(bannerPath)
iconImage = Image.open(iconPath)

logoImage = customtkinter.CTkImage(bannerImage, size=(134, 41.5))

tempIconPath = os.path.join(os.path.dirname(__file__), "temp_icon.ico")
iconImage.save(tempIconPath)

root = customtkinter.CTk()
root.title("nanoMIDIPlayer - Bootstrapper")
root.configure(bg="#0A0A0A")
root.geometry("400x200")
root.resizable(False, False)
root.iconbitmap(tempIconPath)

logo = customtkinter.CTkLabel(
    root, text="", image=logoImage,
    compound="left", font=customtkinter.CTkFont(size=15, weight="bold", family="Consolas")
)
logo.pack(pady=20)

progressVar = tk.DoubleVar()
progressBar = customtkinter.CTkProgressBar(root, variable=progressVar, width=300, progress_color="#ffffff")
progressBar.pack(pady=20)

status = customtkinter.CTkLabel(root, text="Downloading...\nPlease wait", font=("Consolas", 14))
status.pack(pady=10)

thread = threading.Thread(target=progressThread)
thread.start()

root.mainloop()
