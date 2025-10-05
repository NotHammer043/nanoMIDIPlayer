import customtkinter as ctk
import platform
import os
import json
import requests

from ui import customTheme
from modules import configuration
from modules.functions import mainFunctions

osName = platform.system()

if osName == "Darwin":
    baseDirectory = os.path.join(os.path.expanduser("~"), 'nanoMIDIPlayer')
else:
    baseDirectory = os.getcwd()

class SettingsTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        customTheme.initializeFonts()
        from modules.functions import midiPlayerFunctions
        from modules.functions import settingsFunctions

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mainScrollFrame = mainFunctions.ScrollableFrame(
            self, corner_radius=0, 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["BackgroundColor"]
        )
        self.mainScrollFrame.grid(row=0, column=0, sticky="nsew")
        self.mainScrollFrame.grid_rowconfigure(0, weight=1)
        self.__class__.mainScrollFrame = self.mainScrollFrame

        if osName == "Linux":
            self.mainScrollFrame.bind_all("<Button-4>", lambda e: self.mainScrollFrame._parent_canvas.yview("scroll", -1, "units"))
            self.mainScrollFrame.bind_all("<Button-5>", lambda e: self.mainScrollFrame._parent_canvas.yview("scroll", 1, "units"))

        # QWERTY SECTION
        self.qwertySettingsLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="MIDI Player Settings", fg_color="transparent", 
            font=customTheme.globalFont20, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.qwertySettingsLabel.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

        self.sustainToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Sustain", command=midiPlayerFunctions.switchSustain, variable=midiPlayerFunctions.switchSustainvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.sustainToggle.grid(row=1, column=0, padx=(20, 0), pady=(5, 0), sticky="w")
        self.__class__.sustainToggle = self.sustainToggle

        self.noDoublesToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="No Doubles", command=midiPlayerFunctions.switchNoDoubles, variable=midiPlayerFunctions.switchNoDoublesvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.noDoublesToggle.grid(row=2, column=0, padx=(20, 0), pady=(5, 0), sticky="w")
        self.__class__.noDoublesToggle = self.noDoublesToggle

        self.velocityToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Velocity", command=midiPlayerFunctions.switchVelocity, variable=midiPlayerFunctions.switchVelocityvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.velocityToggle.grid(row=3, column=0, padx=(20, 0), pady=(5, 0), sticky="nw")
        self.__class__.velocityToggle = self.velocityToggle

        self.use88KeysToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="88 Keys", command=midiPlayerFunctions.switch88Keys, variable=midiPlayerFunctions.switch88Keysvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.use88KeysToggle.grid(row=3, column=0, padx=(20, 0), pady=(35, 0), sticky="nw")
        self.__class__.use88KeysToggle = self.use88KeysToggle

        self.midiLoopSongToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Loop Song", command=settingsFunctions.switchMidiLoopSong, variable=settingsFunctions.switchMidiLoopSongvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.midiLoopSongToggle.grid(row=4, column=0, padx=(20, 0), pady=(20, 0), sticky="nw")
        self.__class__.midiLoopSongToggle = self.midiLoopSongToggle

        self.midiReleaseOnPauseToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Release\nkeys on Pause", command=settingsFunctions.switchMidiReleaseOnPause, variable=settingsFunctions.switchMidiReleaseOnPausevar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.midiReleaseOnPauseToggle.grid(row=5, column=0, padx=(20, 0), pady=(10, 10), sticky="nw")
        self.__class__.midiReleaseOnPauseToggle = self.midiReleaseOnPauseToggle

        self.midiClearMidiListButton = ctk.CTkButton(
            self.mainScrollFrame, text="Clear MIDI List", width=159, command=settingsFunctions.midiClearMidiList, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.midiClearMidiListButton.grid(row=0, column=0, padx=(0, 170), pady=(10, 0), sticky="e")

        self.midiCustomHoldLengthToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Custom Hold Length", command=settingsFunctions.switchMidiCustomHoldLength, variable=settingsFunctions.switchMidiCustomHoldLengthvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.midiCustomHoldLengthToggle.grid(row=1, column=0, padx=(40,0), pady=(5, 0), sticky="s")

        self.midiNoteLengthLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Note Length", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.midiNoteLengthLabel.grid(row=2, column=0, padx=(212, 0), pady=(0, 0), sticky="nw")
        self.__class__.midiNoteLengthLabel = self.midiNoteLengthLabel

        self.midiNoteLengthSlider = ctk.CTkSlider(
            self.mainScrollFrame, from_=0, to=10, width=200, command=lambda value: settingsFunctions.updateFromSlider("midiNoteLength", value), 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleHoverColor"]
        )
        self.midiNoteLengthSlider.grid(row=3, column=0, padx=(207,0), pady=(0, 0), sticky="nw")
        self.midiNoteLengthSlider.set(configuration.configData['midiPlayer']['randomFail']['speed'])
        self.__class__.midiNoteLengthSlider = self.midiNoteLengthSlider

        self.midiResetNoteLength = ctk.CTkButton(
            self.mainScrollFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("midiNoteLength"), font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.midiResetNoteLength.grid(row=2, column=0, padx=(370, 0), pady=(0, 0), sticky="nw")
        self.__class__.midiResetNoteLength = self.midiResetNoteLength

        self.midiNoteLengthEntry = ctk.CTkEntry(
            self.mainScrollFrame, placeholder_text="10", width=60,
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            border_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBorderColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBackColor"]
        )
        self.midiNoteLengthEntry.grid(row=2, column=0, padx=(307, 0), pady=(0, 0), sticky="nw")
        self.midiNoteLengthEntry.insert(0, configuration.configData['midiPlayer']['customHoldLength']['noteLength'])
        self.__class__.midiNoteLengthEntry = self.midiNoteLengthEntry

        self.midiNoteLengthEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("midiNoteLength", value))
        self.midiNoteLengthEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("midiNoteLength", value))
        self.midiNoteLengthSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("midiNoteLength", value))
        
        self.midiRandomFailToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Random Fail", command=settingsFunctions.switchMidiRandomFail, variable=settingsFunctions.switchMidiRandomFailvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.midiRandomFailToggle.grid(row=3, column=0, padx=(85,0), pady=(0, 0), sticky="s")

        self.midiSpeedFailLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Speed Fail %", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.midiSpeedFailLabel.grid(row=4, column=0, padx=(150,0), pady=(0, 0), sticky="nw")
        self.__class__.midiSpeedFailLabel = self.midiSpeedFailLabel

        self.midiSpeedFailSlider = ctk.CTkSlider(
            self.mainScrollFrame, from_=0, to=100, width=125, command=lambda value: settingsFunctions.updateFromSlider("midiSpeedFail", value), 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleHoverColor"]
        )
        self.midiSpeedFailSlider.grid(row=5, column=0, padx=(140,0), pady=(5, 0), sticky="nw")
        self.midiSpeedFailSlider.set(configuration.configData['midiPlayer']['randomFail']['speed'])
        self.__class__.midiSpeedFailSlider = self.midiSpeedFailSlider

        self.midiResetSpeedFailButton = ctk.CTkButton(
            self.mainScrollFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("midiSpeedFail"), font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.midiResetSpeedFailButton.grid(row=4, column=0, padx=(210, 0), pady=(25, 0), sticky="nw")
        self.__class__.midiResetSpeedFailButton = self.midiResetSpeedFailButton

        self.midiSpeedFailEntry = ctk.CTkEntry(
            self.mainScrollFrame, placeholder_text="10", width=50, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            border_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBorderColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBackColor"]
        )
        self.midiSpeedFailEntry.grid(row=4, column=0, padx=(155,0), pady=(25, 0), sticky="nw")
        self.midiSpeedFailEntry.insert(0, configuration.configData['midiPlayer']['randomFail']['speed'])
        self.__class__.midiSpeedFailEntry = self.midiSpeedFailEntry

        self.midiSpeedFailEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("midiSpeedFail", value))
        self.midiSpeedFailEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("midiSpeedFail", value))
        self.midiSpeedFailSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("midiSpeedFail", value))

        self.midiTransposeFailLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Transpose Fail %", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.midiTransposeFailLabel.grid(row=4, column=0, padx=(85,0), pady=(0, 0), sticky="n")
        self.__class__.midiTransposeFailLabel = self.midiTransposeFailLabel

        self.midiTransposeFailSlider = ctk.CTkSlider(
            self.mainScrollFrame, from_=0, to=100, width=125, command=lambda value: settingsFunctions.updateFromSlider("midiTransposeFail", value), 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleHoverColor"]
        )
        self.midiTransposeFailSlider.grid(row=5, column=0, padx=(85,0), pady=(5, 0), sticky="n")
        self.midiTransposeFailSlider.set(configuration.configData['midiPlayer']['randomFail']['transpose'])
        self.__class__.midiTransposeFailSlider = self.midiTransposeFailSlider

        self.midiResetTransposeFailButton = ctk.CTkButton(
            self.mainScrollFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("midiTransposeFail"), font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.midiResetTransposeFailButton.grid(row=4, column=0, padx=(140, 0), pady=(25, 0))
        self.__class__.midiResetTransposeFailButton = self.midiResetTransposeFailButton

        self.midiTransposeFailEntry = ctk.CTkEntry(
            self.mainScrollFrame, placeholder_text="10", width=50, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            border_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBorderColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBackColor"]
        )
        self.midiTransposeFailEntry.grid(row=4, column=0, padx=(50,0), pady=(25, 0))
        self.midiTransposeFailEntry.insert(0, configuration.configData['midiPlayer']['randomFail']['transpose'])
        self.__class__.midiTransposeFailEntry = self.midiTransposeFailEntry

        self.midiTransposeFailEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("midiTransposeFail", value))
        self.midiTransposeFailEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("midiTransposeFail", value))
        self.midiTransposeFailSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("midiTransposeFail", value))

        self.midiDecreaseSizeLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Speed Hotkey\nDecrease Size", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.midiDecreaseSizeLabel.grid(row=6, column=0, padx=(25, 0), pady=(0, 0), sticky="nw")

        self.midiDecreaseSizeSlider = ctk.CTkSlider(
            self.mainScrollFrame, from_=0, to=100, width=190, command=lambda value: settingsFunctions.updateFromSlider("midiDecreaseSize", value), 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleHoverColor"]
        )
        self.midiDecreaseSizeSlider.grid(row=6, column=0, padx=(20,0), pady=(37, 0), sticky="nw")
        self.midiDecreaseSizeSlider.set(configuration.configData['midiPlayer']['decreaseSize'])
        self.__class__.midiDecreaseSizeSlider = self.midiDecreaseSizeSlider

        self.midiResetDecreaseSize = ctk.CTkButton(
            self.mainScrollFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("midiDecreaseSize"), font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.midiResetDecreaseSize.grid(row=6, column=0, padx=(173, 0), pady=(5, 0), sticky="nw")

        self.midiDecreaseSizeEntry = ctk.CTkEntry(
            self.mainScrollFrame, placeholder_text="10", width=35, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            border_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBorderColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBackColor"]
        )
        self.midiDecreaseSizeEntry.grid(row=6, column=0, padx=(135, 0), pady=(5, 0), sticky="nw")
        self.midiDecreaseSizeEntry.insert(0, configuration.configData['midiPlayer']['decreaseSize'])
        self.__class__.midiDecreaseSizeEntry = self.midiDecreaseSizeEntry

        self.midiDecreaseSizeEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("midiDecreaseSize", value))
        self.midiDecreaseSizeEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("midiDecreaseSize", value))
        self.midiDecreaseSizeSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("midiDecreaseSize", value))

        self.midiModuleSelectorText = ctk.CTkLabel(
            self.mainScrollFrame, text="Keyboard Module", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.midiModuleSelectorText.grid(row=6, column=0, padx=(0, 205), pady=(0, 35), sticky="es")

        self.midiModuleSelector = ctk.CTkOptionMenu(
            self.mainScrollFrame, width=170, command=settingsFunctions.midiModuleSelect, values=["pynput", "keyboard"], 
            font=customTheme.globalFont14, dropdown_font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionBackColor"], 
            dropdown_fg_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownBackground"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownButtonColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            dropdown_text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )

        self.midiModuleSelector.grid(row=6, column=0, padx=(0, 180), pady=(0, 10), sticky="es")
        
        if osName != "Windows":
            self.midiModuleSelector.set("Unavailable")
            self.midiModuleSelector.configure(state="disabled")
        else:
            self.midiModuleSelector.set(configuration.configData.get("midiPlayer", {}).get("inputModule", "pynput"))

        # DRUMS MACRO SECTION
        self.drumsSettingsLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Drums Macro Settings", fg_color="transparent", 
            font=customTheme.globalFont20, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.drumsSettingsLabel.grid(row=7, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

        self.drumsLoopSongToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Loop Song", command=settingsFunctions.switchDrumsLoopSong, variable=settingsFunctions.switchDrumsLoopSongvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.drumsLoopSongToggle.grid(row=8, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.__class__.drumsLoopSongToggle = self.drumsLoopSongToggle

        self.drumsReleaseOnPauseToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Release\nkeys on Pause", command=settingsFunctions.switchDrumsReleaseOnPause, variable=settingsFunctions.switchDrumsReleaseOnPausevar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.drumsReleaseOnPauseToggle.grid(row=9, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.__class__.drumsReleaseOnPauseToggle = self.drumsReleaseOnPauseToggle

        self.drumsClearMidiListButton = ctk.CTkButton(
            self.mainScrollFrame, text="Clear MIDI List", width=159, command=settingsFunctions.drumsClearMidiList, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.drumsClearMidiListButton.grid(row=7, column=0, padx=(0, 170), pady=(10, 0), sticky="e")

        self.drumsCustomHoldLengthToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Custom Hold Length", command=settingsFunctions.switchDrumsCustomHoldLength, variable=settingsFunctions.switchDrumsCustomHoldLengthvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.drumsCustomHoldLengthToggle.grid(row=8, column=0, padx=(40,0), pady=(5, 0), sticky="s")

        self.drumsNoteLengthLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Note Length", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.drumsNoteLengthLabel.grid(row=9, column=0, padx=(212, 0), pady=(0, 0), sticky="nw")
        self.__class__.drumsNoteLengthLabel = self.drumsNoteLengthLabel

        self.drumsNoteLengthSlider = ctk.CTkSlider(
            self.mainScrollFrame, from_=0, to=10, width=200, command=lambda value: settingsFunctions.updateFromSlider("drumsNoteLength", value), 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleHoverColor"]
        )
        self.drumsNoteLengthSlider.grid(row=10, column=0, padx=(207,0), pady=(0, 0), sticky="nw")
        self.drumsNoteLengthSlider.set(configuration.configData['midiPlayer']['customHoldLength']['noteLength'])
        self.__class__.drumsNoteLengthSlider = self.drumsNoteLengthSlider

        self.drumsResetNoteLength = ctk.CTkButton(
            self.mainScrollFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("drumsNoteLength"), font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.drumsResetNoteLength.grid(row=9, column=0, padx=(370, 0), pady=(0, 0), sticky="nw")
        self.__class__.drumsResetNoteLength = self.drumsResetNoteLength

        self.drumsNoteLengthEntry = ctk.CTkEntry(
            self.mainScrollFrame, placeholder_text="10", width=60, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            border_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBorderColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBackColor"]
        )
        self.drumsNoteLengthEntry.grid(row=9, column=0, padx=(307, 0), pady=(0, 0), sticky="nw")
        self.drumsNoteLengthEntry.insert(0, configuration.configData['midiPlayer']['customHoldLength']['noteLength'])
        self.__class__.drumsNoteLengthEntry = self.drumsNoteLengthEntry

        self.drumsNoteLengthEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("drumsNoteLength", value))
        self.drumsNoteLengthEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("drumsNoteLength", value))
        self.drumsNoteLengthSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("drumsNoteLength", value))

        self.drumsRandomFailToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Random Fail", command=settingsFunctions.switchDrumsRandomFail, variable=settingsFunctions.switchDrumsRandomFailvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.drumsRandomFailToggle.grid(row=10, column=0, padx=(100,0), pady=(20, 0), sticky="s")



        self.drumsSpeedFailLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Speed Fail %", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.drumsSpeedFailLabel.grid(row=11, column=0, padx=(0,50), pady=(0, 15))
        self.__class__.drumsSpeedFailLabel = self.drumsSpeedFailLabel

        self.drumsSpeedFailSlider = ctk.CTkSlider(
            self.mainScrollFrame, from_=0, to=100, width=200, command=lambda value: settingsFunctions.updateFromSlider("drumsSpeedFail", value), 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleHoverColor"]
        )
        self.drumsSpeedFailSlider.grid(row=11, column=0, padx=(207,0), pady=(37, 0), sticky="nw")
        self.drumsSpeedFailSlider.set(configuration.configData['drumsMacro']['randomFail']['speed'])
        self.__class__.drumsSpeedFailSlider = self.drumsSpeedFailSlider

        self.drumsResetSpeedFailButton = ctk.CTkButton(
            self.mainScrollFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("drumsSpeedFail"), font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.drumsResetSpeedFailButton.grid(row=11, column=0, padx=(370, 0), pady=(5, 0), sticky="nw")
        self.__class__.drumsResetSpeedFailButton = self.drumsResetSpeedFailButton

        self.drumsSpeedFailEntry = ctk.CTkEntry(
            self.mainScrollFrame, placeholder_text="10", width=50, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            border_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBorderColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBackColor"]
        )
        self.drumsSpeedFailEntry.grid(row=11, column=0, padx=(0, 205), pady=(5, 0), sticky="ne")
        self.drumsSpeedFailEntry.insert(0, configuration.configData['drumsMacro']['randomFail']['speed'])
        self.__class__.drumsSpeedFailEntry = self.drumsSpeedFailEntry

        self.drumsSpeedFailEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("drumsSpeedFail", value))
        self.drumsSpeedFailEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("drumsSpeedFail", value))
        self.drumsSpeedFailSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("drumsSpeedFail", value))



        self.drumsDecreaseSizeLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Speed Hotkey\nDecrease Size", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.drumsDecreaseSizeLabel.grid(row=11, column=0, padx=(25, 0), pady=(0, 0), sticky="nw")

        self.drumsDecreaseSizeSlider = ctk.CTkSlider(
            self.mainScrollFrame, from_=0, to=100, width=190, command=lambda value: settingsFunctions.updateFromSlider("drumsDecreaseSize", value), 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleHoverColor"]
        )
        self.drumsDecreaseSizeSlider.grid(row=11, column=0, padx=(20,0), pady=(37, 0), sticky="nw")
        self.drumsDecreaseSizeSlider.set(configuration.configData['midiPlayer']['decreaseSize'])
        self.__class__.drumsDecreaseSizeSlider = self.drumsDecreaseSizeSlider

        self.drumsResetDecreaseSize = ctk.CTkButton(
            self.mainScrollFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("drumsDecreaseSize"), font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.drumsResetDecreaseSize.grid(row=11, column=0, padx=(173, 0), pady=(5, 0), sticky="nw")

        self.drumsDecreaseSizeEntry = ctk.CTkEntry(
            self.mainScrollFrame, placeholder_text="10", width=35, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            border_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBorderColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBackColor"]
        )
        self.drumsDecreaseSizeEntry.grid(row=11, column=0, padx=(135, 0), pady=(5, 0), sticky="nw")
        self.drumsDecreaseSizeEntry.insert(0, configuration.configData['midiPlayer']['decreaseSize'])
        self.__class__.drumsDecreaseSizeEntry = self.drumsDecreaseSizeEntry

        self.drumsDecreaseSizeEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("drumsDecreaseSize", value))
        self.drumsDecreaseSizeEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("drumsDecreaseSize", value))
        self.drumsDecreaseSizeSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("drumsDecreaseSize", value))

        self.drumsModuleSelectorText = ctk.CTkLabel(
            self.mainScrollFrame, text="Keyboard Module", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.drumsModuleSelectorText.grid(row=10, column=0, padx=(25, 0), pady=(0, 35), sticky="sw")

        self.drumsModuleSelector = ctk.CTkOptionMenu(
            self.mainScrollFrame, width=200, command=settingsFunctions.drumsModuleSelect, values=["pynput", "keyboard"], 
            font=customTheme.globalFont14, dropdown_font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionBackColor"], 
            dropdown_fg_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownBackground"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownButtonColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            dropdown_text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.drumsModuleSelector.grid(row=10, column=0, padx=(20, 0), pady=(30, 10), sticky="sw")

        if osName != "Windows":
            self.drumsModuleSelector.set("Unavailable")
            self.drumsModuleSelector.configure(state="disabled")
        else:
            self.drumsModuleSelector.set(configuration.configData.get("drumsMacro", {}).get("inputModule", "pynput"))



        # APPEARANCE SETTINGS

        self.appUISettingsLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Appearance Settings", fg_color="transparent", 
            font=customTheme.globalFont20, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.appUISettingsLabel.grid(row=12, column=0, padx=(10, 0), pady=(10, 0), sticky="w")



        self.topMostToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Always on top", command=settingsFunctions.switchTopMost, variable=settingsFunctions.switchTopMostvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.topMostToggle.grid(row=13, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.consoleToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Console", command=settingsFunctions.switchConsole, variable=settingsFunctions.switchConsolevar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.consoleToggle.grid(row=13, column=0, padx=(20, 0), pady=(25, 0), sticky="nw")

        self.tooltipToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Tool Tip", command=settingsFunctions.switchToolTip, variable=settingsFunctions.switchToolTipvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.tooltipToggle.grid(row=13, column=0, padx=(20, 0), pady=(50, 0), sticky="nw")

        self.timestampToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Timestamp", command=settingsFunctions.switchTimestamp, variable=settingsFunctions.switchTimestampvar, 
            font=customTheme.globalFont14, onvalue="on", offvalue="off", 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.timestampToggle.grid(row=13, column=0, padx=(20, 0), pady=(75, 0), sticky="nw")


        # DEBUG
        self.openConsoleButton = ctk.CTkButton(
            self.mainScrollFrame, text="Open Debug\nConsole", width=120, command=settingsFunctions.openConsole, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.openConsoleButton.grid(row=13, column=0, padx=(280, 0), pady=(0, 0), sticky="nw")

        self.closeConsoleButton = ctk.CTkButton(
            self.mainScrollFrame, text="Close Debug\nConsole", width=120, command=settingsFunctions.closeConsole, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.closeConsoleButton.grid(row=13, column=0, padx=(280, 0), pady=(50, 0), sticky="nw")

        if osName != 'Windows':
            self.openConsoleButton.configure(state='disabled')
            self.closeConsoleButton.configure(state='disabled')


        





        app = mainFunctions.getApp()

        self.themeSelectorLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="App Theme", fg_color="transparent", 
            font=customTheme.globalFont20, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.themeSelectorLabel.grid(row=14, column=0, padx=(20, 0), pady=(10, 0), sticky="w")

        self.forceThemeToggle = ctk.CTkSwitch(
            self.mainScrollFrame, text="Force API Theme", command=settingsFunctions.switchForceTheme, variable=settingsFunctions.switchForceThemevar,
            font=customTheme.globalFont14, onvalue="on", offvalue="off",
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchDisabled"],
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchEnabled"],
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircle"],
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SwitchCircleHovered"],
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"],
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.forceThemeToggle.grid(row=14, column=0, padx=(65, 0), pady=(0, 0), sticky="s")

        activeThemeName = customTheme.activeThemeData["Name"]
        documentsDir = os.path.join(os.path.expanduser("~"), "Documents")
        baseDirectory = os.path.join(documentsDir, "nanoMIDIPlayer")
        customThemesDir = os.path.join(baseDirectory, "assets", "customThemes")
        os.makedirs(customThemesDir, exist_ok=True)

        if activeThemeName not in app.themeNames:
            app.themeNames.append(activeThemeName)

        for filename in os.listdir(customThemesDir):
            if filename.endswith('.json'):
                customThemeName = filename + " (Custom)"
                if customThemeName and customThemeName not in app.themeNames:
                    app.themeNames.append(customThemeName)

        self.themeSelector = ctk.CTkOptionMenu(
            self.mainScrollFrame, width=380, command=customTheme.switchTheme, values=app.themeNames, 
            font=customTheme.globalFont14, dropdown_font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionBackColor"], 
            dropdown_fg_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownBackground"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownButtonColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            dropdown_text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )
        self.themeSelector.grid(row=15, column=0, padx=(0, 150), pady=(5, 15))
        self.__class__.themeSelector = self.themeSelector
        self.themeSelector.set(activeThemeName)

        # HOTKEY SECTION
        self.hotkeySettingsLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Hotkey Settings", fg_color="transparent", 
            font=customTheme.globalFont20, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.hotkeySettingsLabel.grid(row=20, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

        # HOTKEY LABELS
        self.playHotkeyLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Play", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.playHotkeyLabel.grid(row=21, column=0, padx=(33, 0), pady=(0, 0), sticky="w")

        self.pauseHotkeyLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Pause", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.pauseHotkeyLabel.grid(row=21, column=0, padx=(110, 0), pady=(0, 0), sticky="w")

        self.stopHotkeyLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Stop", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.stopHotkeyLabel.grid(row=21, column=0, padx=(193, 0), pady=(0, 0), sticky="w")

        self.slowDownHotkeyLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Slow Down", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.slowDownHotkeyLabel.grid(row=21, column=0, padx=(254, 0), pady=(0, 0), sticky="w")

        self.speedUpHotkeyLabel = ctk.CTkLabel(
            self.mainScrollFrame, text="Speed Up", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.speedUpHotkeyLabel.grid(row=21, column=0, padx=(340, 0), pady=(0, 0), sticky="w")

        # HOTKEYS
        self.playHotkeyButton = ctk.CTkButton(
            self.mainScrollFrame, text=configuration.configData["hotkeys"].get('play', 'f1').upper(), width=70, 
            command=mainFunctions.playHotkeyCommand, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorHoverColor"]
        )
        self.playHotkeyButton.grid(row=22, column=0, padx=(15, 165), pady=(0, 5), sticky="w")
        self.__class__.playHotkeyButton = self.playHotkeyButton

        self.pauseHotkeyButton = ctk.CTkButton(
            self.mainScrollFrame, text=configuration.configData["hotkeys"].get('pause', 'f2').upper(), width=70, 
            command=mainFunctions.pauseHotkeyCommand, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorHoverColor"]
        )
        self.pauseHotkeyButton.grid(row=22, column=0, padx=(95, 165), pady=(0, 5), sticky="w")
        self.__class__.pauseHotkeyButton = self.pauseHotkeyButton

        self.stopHotkeyButton = ctk.CTkButton(
            self.mainScrollFrame, text=configuration.configData["hotkeys"].get('stop', 'f3').upper(), width=70, 
            command=mainFunctions.stopHotkeyCommand, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorHoverColor"]
        )
        self.stopHotkeyButton.grid(row=22, column=0, padx=(175, 165), pady=(0, 5), sticky="w")
        self.__class__.stopHotkeyButton = self.stopHotkeyButton

        self.speedUpHotkeyButton = ctk.CTkButton(
            self.mainScrollFrame, text=configuration.configData["hotkeys"].get('speedup', 'f4').upper(), width=70, 
            command=mainFunctions.speedUpHotkeyCommand, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorHoverColor"]
        )
        self.speedUpHotkeyButton.grid(row=22, column=0, padx=(255, 165), pady=(0, 5), sticky="w")
        self.__class__.speedUpHotkeyButton = self.speedUpHotkeyButton

        self.slowHotkeyButton = ctk.CTkButton(
            self.mainScrollFrame, text=configuration.configData["hotkeys"].get('slowdown', 'f5').upper(), width=70, 
            command=mainFunctions.slowHotkeyCommand, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["HotkeySelectorHoverColor"]
        )
        self.slowHotkeyButton.grid(row=22, column=0, padx=(337, 165), pady=(0, 5), sticky="w")
        self.__class__.slowHotkeyButton = self.slowHotkeyButton

        settingsFunctions.midiCustomHoldLengthStatus()
        settingsFunctions.midiRandomFailStatus()

        settingsFunctions.drumsCustomHoldLengthStatus()
        settingsFunctions.drumsRandomFailStatus()