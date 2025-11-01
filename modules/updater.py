import requests
import threading
import webbrowser
import os
import subprocess
import tempfile
import tkinter.messagebox as messagebox

def checkForUpdates(appVersion):
    try:
        response = requests.get("https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/version")
        response.raise_for_status()
        versionInfo = response.json()

        latestVersions = versionInfo.get("latest", [])
        avoidVersions = versionInfo.get("avoid", [])
        alertMessage = versionInfo.get("alertMessage", "")

        if appVersion in avoidVersions:
            return "urgent", alertMessage
        elif appVersion not in latestVersions:
            return "update", ""
    except requests.RequestException as e:
        print(e)

    return "none", ""


def downloadBootstrapper():
    url = "https://github.com/NotHammer043/nanoMIDIPlayer/raw/main/dist/bootstrapper.exe"

    folderPath = tempfile.gettempdir()
    filePath = os.path.join(folderPath, "bootstrapper.exe")

    threading.Thread(
        target=messagebox.showinfo,
        args=("Downloading Bootstrapper", "If there's an issue downloading, try disabling your antivirus.")
    ).start()

    def download(url, filePath):
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filePath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    try:
        download(url, filePath)
        print(f"Downloaded {filePath}")
        messagebox.showinfo("Download Complete", "Click OK to start updater.")
        subprocess.Popen(filePath, creationflags=subprocess.CREATE_NEW_CONSOLE)
        os._exit(1)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while downloading:\n{e}")


def runUpdater(appVersion):
    updateStatus, urgentMessage = checkForUpdates(appVersion)

    if updateStatus == "urgent":
        messagebox.showwarning("Critical Update Required", urgentMessage)
        webbrowser.open("https://github.com/NotHammer043/nanoMIDIPlayer/releases/latest")

    elif updateStatus == "update":
        result = messagebox.askyesno(
            "Update Available",
            "A new version of nanoMIDIPlayer is available.\n\nWould you like to update now?"
        )
        if result:
            threading.Thread(target=downloadBootstrapper).start()