import os
import json
import threading
import platform
import datetime
import requests
import concurrent.futures
import customtkinter as ctk
import textwrap
import logging
from PIL import Image
from mido import MidiFile
from modules import configuration
from ui import customTheme
from modules.functions import mainFunctions

logger = logging.getLogger(__name__)

osName = platform.system()

documentsDir = os.path.join(os.path.expanduser("~"), "Documents")
baseDirectory = os.path.join(documentsDir, "nanoMIDIPlayer")
os.makedirs(baseDirectory, exist_ok=True)

midiDataUrl = "https://api.nanomidi.net/api/midiData"
pageSize = 10
currentPage = 1
downloadFolder = os.path.join(baseDirectory, "Midis")
allMidiData = None
totalPages = None
filteredData = None

os.makedirs(downloadFolder, exist_ok=True)

def searchBar(event=None):
    logger.info("searchBar called")
    try:
        threading.Thread(target=filteredMidiData).start()
    except Exception as e:
        logger.exception(f"searchBar error: {e}")

def sortComboCommand(value):
    logger.info(f"sortComboCommand called with value: {value}")
    try:
        threading.Thread(target=sortMidiData, args=(value,)).start()
    except Exception as e:
        logger.exception(f"sortComboCommand error: {e}")

def loadMidiData():
    logger.info("loadMidiData called")
    clearList()
    def worker():
        global allMidiData, totalPages, filteredData
        from ui.midiHub import MidiHubTab
        try:
            logger.debug(f"Requesting {midiDataUrl}")
            response = requests.get(midiDataUrl, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to load MIDI data: {e}")
            def errorUi(err=e):
                for widget in MidiHubTab.mainScrollFrame.winfo_children():
                    info = widget.grid_info()
                    if info and int(info.get("row", 1)) > 0:
                        try:
                            widget.destroy()
                        except Exception as ex:
                            logger.debug(f"Widget destroy failed: {ex}")

                pleaseWait = ctk.CTkLabel(
                    MidiHubTab.mainScrollFrame, text="Couldn't reach\nnanomidi.net!",
                    text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
                    compound="left", font=customTheme.globalFont40
                )
                pleaseWait.grid(row=1, column=0, padx=10, pady=(30,0), sticky="new")

                pleaseWait2 = ctk.CTkLabel(
                    MidiHubTab.mainScrollFrame, 
                    text=f"Error: {err.__class__.__name__}\n\nThis may have happened for one of the\nfollowing reasons:\n\n1. You are offline.\n2. Something is blocking your connection\nto https://nanomidi.net\n3. The server is currently offline or encountered\nan issue — please try again later.\n\nIf nanoMIDI is Offline, please report it to the\ndeveloper or check server status here\nhttps://status.nanomidi.net",
                    text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
                    compound="left", font=customTheme.globalFont14
                )
                pleaseWait2.grid(row=2, column=0, padx=10, pady=(0,0), sticky="new")
            MidiHubTab.mainScrollFrame.after(0, errorUi)
            return

        try:
            allMidiData = response.json()
            logger.debug(f"Fetched {len(allMidiData)} MIDI entries")
            allMidiData.reverse()
            filteredData = allMidiData
            totalPages = (len(filteredData) + pageSize - 1) // pageSize
            showPage(currentPage)
        except Exception as e:
            logger.exception(f"Parsing response error: {e}")

    threading.Thread(target=worker, daemon=True).start()

def fetchImage(midi):
    try:
        imageUrl = f"https://api.nanomidi.net/api/v2/images/{midi['imageFilename']}?size=100x100"
        logger.debug(f"Fetching image {imageUrl}")
        response = requests.get(imageUrl, stream=True)
        return ctk.CTkImage(Image.open(response.raw), size=(100, 100))
    except Exception as e:
        logger.exception(f"fetchImage error for {midi.get('imageFilename')}: {e}")
        return None

def sortMidiData(selectedValue):
    logger.info(f"sortMidiData called with {selectedValue}")
    global totalPages, filteredData
    try:
        clearList()
        if selectedValue == "Newest":
            filteredData = sorted(allMidiData, key=lambda x: x["id"], reverse=True)
        elif selectedValue == "Oldest":
            filteredData = sorted(allMidiData, key=lambda x: x["id"])
        elif selectedValue == "Downloads":
            filteredData = sorted(allMidiData, key=lambda m: m.get("downloads", 0), reverse=True)
        elif selectedValue == "Views":
            filteredData = sorted(allMidiData, key=lambda m: m.get("views", 0), reverse=True)
        else:
            filteredData = allMidiData

        totalPages = (len(filteredData) + pageSize - 1) // pageSize
        showPage(currentPage)
    except Exception as e:
        logger.exception(f"sortMidiData error: {e}")

def showPage(page):
    logger.info(f"showPage called with page {page}")
    clearList()
    def worker():
        global filteredData
        from ui.midiHub import MidiHubTab
        try:
            startIndex = (page - 1) * pageSize
            endIndex = min(startIndex + pageSize, len(filteredData))
            logger.debug(f"Rendering entries {startIndex} to {endIndex}")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [(midi, executor.submit(fetchImage, midi)) for midi in filteredData[startIndex:endIndex]]
            def render():
                if hasattr(MidiHubTab, "loadingFrame"):
                    MidiHubTab.loadingFrame.destroy()
                for index, (midi, future) in enumerate(results, start=1):
                    try:
                        midiImage = future.result()
                    except Exception as e:
                        logger.debug(f"Image fetch failed for {midi.get('name')}: {e}")
                        midiImage = None
                    createMidiFrame(index, midi, midiImage)
                midiHubFooter()
            MidiHubTab.mainScrollFrame.after(0, render)
        except Exception as e:
            logger.exception(f"showPage worker error: {e}")
    threading.Thread(target=worker, daemon=True).start()

def createMidiFrame(row, midi, midiImage):
    from ui.midiHub import MidiHubTab
    logger.debug(f"Creating frame for {midi.get('name')} at row {row}")
    try:
        def wrapText(text, width):
            return "\n".join(textwrap.wrap(text, width=width, break_long_words=True))

        nameText = wrapText(midi["name"], 28)
        artistText = wrapText(midi["artists"], 36)
        arrText = "Arr: " + (wrapText(midi["arranger"], 36) if midi["arranger"] else "N/A")
        uploaderText = "Uploader: " + wrapText(midi["uploader"], 36)

        nameLines = nameText.count("\n") + 1
        artistLines = artistText.count("\n") + 1
        arrLines = arrText.count("\n") + 1
        uploaderLines = uploaderText.count("\n") + 1
        totalLines = nameLines + artistLines + arrLines + uploaderLines
        frameHeight = max(100, 40 + totalLines * 18)

        midiFrame = ctk.CTkFrame(
            master=MidiHubTab.mainScrollFrame,
            height=frameHeight,
            fg_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["MidiCardBackColor"]
        )
        midiFrame.grid(row=row, column=0, padx=20, pady=5, sticky="nsew")

        midiImageButton = ctk.CTkButton(
            master=midiFrame, text="", fg_color="transparent", width=100, height=100,
            state="disabled", image=midiImage
        )
        midiImageButton.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            midiFrame, text=nameText,
            font=customTheme.globalFont14, text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            anchor="w", justify="left"
        ).grid(row=0, column=0, padx=120, pady=(0, 80 + (nameLines - 1) * 18), sticky="w")

        ctk.CTkLabel(
            midiFrame, text=artistText,
            font=customTheme.globalFont12, text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            anchor="w", justify="left"
        ).grid(row=0, column=0, padx=120, pady=(0, 35 + (artistLines - 1) * 18), sticky="w")

        ctk.CTkLabel(
            midiFrame, text=arrText,
            font=customTheme.globalFont11, text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            anchor="w", justify="left"
        ).grid(row=0, column=0, padx=120, pady=(40 + (arrLines - 1) * 18, 0), sticky="w")

        ctk.CTkLabel(
            midiFrame, text=uploaderText,
            font=customTheme.globalFont11, text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            anchor="w", justify="left"
        ).grid(row=0, column=0, padx=120, pady=(80 + (uploaderLines - 1) * 18, 0), sticky="w")

        midiFilename = midi["midiFilename"]
        if midiFilename:
            downloadUrl = "https://api.nanomidi.net/api/midis/" + midiFilename
            ctk.CTkButton(
                master=midiFrame, text="", width=24, height=24,
                fg_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["DownloadButtonColor"],
                hover_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["DownloadButtonHoverColor"],
                image=customTheme.downloadImageFile,
                command=lambda url=downloadUrl: downloadMidi(url)
            ).grid(row=0, column=0, padx=345, pady=(75 + (totalLines - 4) * 18, 0), sticky="e")
    except Exception as e:
        logger.exception(f"createMidiFrame error: {e}")

def downloadMidi(url):
    logger.info(f"downloadMidi called with url {url}")
    try:
        from ui.midiPlayer import MidiPlayerTab
        app = mainFunctions.getApp()
        response = requests.get(url)
        filename = url.split("/")[-1]
        filepath = os.path.join(downloadFolder, filename)

        configuration.configData['midiPlayer']['currentFile'] = filepath
        midi_list = configuration.configData['midiPlayer'].get('midiList', [])
        if filepath not in midi_list:
            midi_list.append(filepath)
        configuration.configData['midiPlayer']['midiList'] = midi_list

        with open(configuration.configPath, 'w') as configFile:
            json.dump(configuration.configData, configFile, indent=2)

        with open(filepath, "wb") as f:
            f.write(response.content)

        currentValues = list(MidiPlayerTab.filePathEntry.cget("values"))
        if filepath not in currentValues:
            currentValues.append(filepath)
            MidiPlayerTab.filePathEntry.configure(values=currentValues)
        MidiPlayerTab.filePathEntry.set(filepath)
        
        app.showFrame("midi")
        midiFile = MidiFile(filepath)
        totalTime = midiFile.length
        timelineText = (
            f"0:00:00 / {str(datetime.timedelta(seconds=int(totalTime)))}"
            if configuration.configData['appUI']['timestamp']
            else f"X:XX:XX / {str(datetime.timedelta(seconds=int(totalTime)))}"
        )
        MidiPlayerTab.timelineIndicator.configure(text=timelineText)

        threading.Thread(target=mainFunctions.log, args=("Downloaded MIDI File:",)).start()
        threading.Thread(target=mainFunctions.log, args=(filepath,)).start()
        logger.debug(f"Downloaded and saved to {filepath}")
    except Exception as e:
        logger.exception(f"downloadMidi error: {e}")

def midiHubFooter():
    logger.debug("midiHubFooter called")
    try:
        from ui.midiHub import MidiHubTab
        paginationFrame = ctk.CTkFrame(master=MidiHubTab.mainScrollFrame, fg_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["PageControlFrameBackground"])
        paginationFrame.grid(row=pageSize + 1, column=0, padx=20, pady=5, sticky="nsew")
        ctk.CTkButton(master=paginationFrame, text="Previous", width=118, font=customTheme.globalFont14,
            command=prevPage, text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            fg_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["PreviousButtonColor"],
            hover_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["PreviousButtonHoverColor"]).grid(row=0, column=0, padx=9, pady=10)
        ctk.CTkLabel(master=paginationFrame, text=f"Page {currentPage}/{totalPages}", font=customTheme.globalFont14,
            text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"]).grid(row=0, column=1, padx=(13, 0), pady=10)
        ctk.CTkButton(master=paginationFrame, text="Next", font=customTheme.globalFont14, width=118,
            command=nextPage, text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            fg_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["NextButtonColor"],
            hover_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["NextButtonHoverColor"]).grid(row=0, column=2, padx=18, pady=10)
    except Exception as e:
        logger.exception(f"midiHubFooter error: {e}")

def prevPage():
    global currentPage
    logger.info("prevPage called")
    try:
        if currentPage > 1:
            currentPage -= 1
            showPage(currentPage)
    except Exception as e:
        logger.exception(f"prevPage error: {e}")

def nextPage():
    global currentPage
    logger.info("nextPage called")
    try:
        if currentPage < totalPages:
            currentPage += 1
            showPage(currentPage)
    except Exception as e:
        logger.exception(f"nextPage error: {e}")

def filteredMidiData():
    global totalPages, filteredData, currentPage
    logger.info("filteredMidiData called")
    try:
        from ui.midiHub import MidiHubTab
        for widget in MidiHubTab.mainScrollFrame.winfo_children():
            if widget not in (MidiHubTab.searchEntry, MidiHubTab.searchButton, MidiHubTab.sortComboBox):
                widget.destroy()

        pleaseWait = ctk.CTkLabel(
            MidiHubTab.mainScrollFrame, text="Please Wait...", text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            compound="left", font=customTheme.globalFont40
        )
        pleaseWait.grid(row=1, column=0, padx=10, pady=(150,0), sticky="nsew")
        pleaseWait2 = ctk.CTkLabel(
            MidiHubTab.mainScrollFrame, text="Fetching from nanomidi.net...", text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            compound="left", font=customTheme.globalFont14
        )
        pleaseWait2.grid(row=2, column=0, padx=10, pady=(100,0), sticky="nsew")
        MidiHubTab.mainScrollFrame.update()

        searchQuery = MidiHubTab.searchEntry.get().lower()
        logger.debug(f"searchQuery: {searchQuery}")
        filteredData = [
            midi for midi in allMidiData
            if searchQuery in midi["name"].lower() or searchQuery in midi["artists"].lower()
        ]
        totalPages = (len(filteredData) + pageSize - 1) // pageSize
        currentPage = 1
        showPage(currentPage)
    except Exception as e:
        logger.exception(f"filteredMidiData error: {e}")

def clearList():
    logger.debug("clearList called")
    try:
        from ui.midiHub import MidiHubTab
        MidiHubTab.mainScrollFrame._parent_canvas.yview_moveto(0)
        for widget in MidiHubTab.mainScrollFrame.winfo_children():
            if widget not in (MidiHubTab.searchEntry, MidiHubTab.searchButton, MidiHubTab.sortComboBox):
                widget.destroy()
        loadingFrame = ctk.CTkFrame(MidiHubTab.mainScrollFrame, fg_color="transparent")
        loadingFrame.grid(row=1, column=0, padx=10, pady=(150,0), sticky="nsew")
        pleaseWaitText = ctk.CTkLabel(
            loadingFrame, text="Please Wait...", 
            text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            compound="left", font=customTheme.globalFont40
        )
        pleaseWaitText.pack()
        pleaseWaitText2 = ctk.CTkLabel(
            loadingFrame, text="Fetching from nanomidi.net...", 
            text_color=customTheme.activeThemeData["Theme"]["MIDIHub"]["TextColor"],
            compound="left", font=customTheme.globalFont14
        )
        pleaseWaitText2.pack(pady=10)
        MidiHubTab.loadingFrame = loadingFrame
    except Exception as e:
        logger.exception(f"clearList error: {e}")
