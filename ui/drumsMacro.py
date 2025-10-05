import customtkinter as ctk
import tkinter as tk
import json

from modules import configuration
from ui import customTheme
from ui.widget.tooltip import ToolTip

class DrumsMacroTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        customTheme.initializeFonts()
        from modules.functions import drumsMacroFunctions
        from modules.functions import mainFunctions
        from modules.functions import settingsFunctions

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mainFrame = ctk.CTkFrame(self, corner_radius=0, fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["BackgroundColor"])
        self.mainFrame.grid(row=0, column=0, sticky="nsew")
        self.mainFrame.grid_columnconfigure(0, weight=1)

        # MIDI FILE PATH
        self.midiPathLabel = ctk.CTkLabel(
            self.mainFrame, text="MIDI File Path", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.midiPathLabel.grid(row=2, column=0, padx=(0,200), pady=(10, 0))

        self.midiPathDropdown = ctk.CTkOptionMenu(
            self.mainFrame, width=350, values="", command=drumsMacroFunctions.switchMidiEvent, 
            font=customTheme.globalFont14, dropdown_font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["OptionBackColor"], 
            dropdown_fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["OptionDropdownBackground"], 
            button_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["OptionDropdownButtonColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["OptionDropdownButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.midiPathDropdown.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.__class__.midiPathDropdown = self.midiPathDropdown
        ToolTip.CreateToolTip(self.midiPathDropdown, text = 'Selected MIDI File')

        self.selectFileButton = ctk.CTkButton(
            self.mainFrame, text="Select File", command=drumsMacroFunctions.selectFile, 
            font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["ButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.selectFileButton.grid(row=2, column=0, padx=(0,55), pady=(10,0), sticky="e")
        ToolTip.CreateToolTip(self.selectFileButton, text = 'Select MIDI File (.mid | .midi)\nMake sure it has Drums Instrument')

        # CONSOLE
        self.consoleFrame = tk.Frame(
            master=self.mainFrame, width=200, height=285, 
            bg=customTheme.activeThemeData["Theme"]["DrumsMacro"]["ConsoleBackground"]
        )
        self.consoleFrame.grid(row=4, column=0, padx=(0,30), pady=(10,0), sticky="ne")
        self.consoleFrame.pack_propagate(0)
        self.__class__.consoleFrame = self.consoleFrame

        # HOTKEYS
        self.playHotkeyLabel = ctk.CTkLabel(
            self.mainFrame, text=" Play:", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.playHotkeyLabel.grid(row=4, column=0, padx=(0, 250), pady=(50, 0), sticky="n")

        self.playHotkeyButton = ctk.CTkButton(
            self.mainFrame, text=configuration.configData["hotkeys"].get('play', 'f1').upper(), width=70, 
            command=mainFunctions.playHotkeyCommand, font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.playHotkeyButton.grid(row=4, column=0, padx=(0, 120), pady=(50, 0), sticky="n")
        self.__class__.playHotkeyButton = self.playHotkeyButton
        ToolTip.CreateToolTip(self.playHotkeyButton, text = 'Start Playback Hotkey')

        self.pauseHotkeyLabel = ctk.CTkLabel(
            self.mainFrame, text="Pause:", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.pauseHotkeyLabel.grid(row=4, column=0, padx=(0, 250), pady=(80, 0), sticky="n")

        self.pauseHotkeyButton = ctk.CTkButton(
            self.mainFrame, text=configuration.configData["hotkeys"].get('pause', 'f2').upper(), width=70, 
            command=mainFunctions.pauseHotkeyCommand, font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.pauseHotkeyButton.grid(row=4, column=0, padx=(0, 120), pady=(80, 0), sticky="n")
        self.__class__.pauseHotkeyButton = self.pauseHotkeyButton
        ToolTip.CreateToolTip(self.pauseHotkeyButton, text = 'Pause Playback Hotkey')

        self.stopHotkeyLabel = ctk.CTkLabel(
            self.mainFrame, text=" Stop:", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.stopHotkeyLabel.grid(row=4, column=0, padx=(0, 250), pady=(110, 0), sticky="n")

        self.stopHotkeyButton = ctk.CTkButton(
            self.mainFrame, text=configuration.configData["hotkeys"].get('stop', 'f3').upper(), width=70, 
            command=mainFunctions.stopHotkeyCommand, font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.stopHotkeyButton.grid(row=4, column=0, padx=(0, 120), pady=(110, 0), sticky="n")
        self.__class__.stopHotkeyButton = self.stopHotkeyButton
        ToolTip.CreateToolTip(self.stopHotkeyButton, text = 'Stop Playback Hotkey')

        self.slowDownHotkeyLabel = ctk.CTkLabel(
            self.mainFrame, text="Slow Down:", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        ) 
        self.slowDownHotkeyLabel.grid(row=4, column=0, padx=(0, 280), pady=(140, 0), sticky="n")

        self.speedUpHotkeyButton = ctk.CTkButton(
            self.mainFrame, text=configuration.configData["hotkeys"].get('speedup', 'f4').upper(), width=70, 
            command=mainFunctions.speedUpHotkeyCommand, font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.speedUpHotkeyButton.grid(row=4, column=0, padx=(0, 120), pady=(140, 0), sticky="n")
        self.__class__.speedUpHotkeyButton = self.speedUpHotkeyButton
        ToolTip.CreateToolTip(self.speedUpHotkeyButton, text = 'Speed-up Playback Hotkey')

        self.speedUpHotkeyLabel = ctk.CTkLabel(
            self.mainFrame, text=" Speed Up:", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.speedUpHotkeyLabel.grid(row=4, column=0, padx=(0, 280), pady=(170, 0), sticky="n")

        self.slowHotkeyButton = ctk.CTkButton(
            self.mainFrame, text=configuration.configData["hotkeys"].get('slowdown', 'f5').upper(), width=70, 
            command=mainFunctions.slowHotkeyCommand, font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.slowHotkeyButton.grid(row=4, column=0, padx=(0, 120), pady=(170, 0), sticky="n")
        self.__class__.slowHotkeyButton = self.slowHotkeyButton
        ToolTip.CreateToolTip(self.slowHotkeyButton, text = 'Slow-down Playback Hotkey')

        # CREDITS
        self.creditsLabel = ctk.CTkLabel(
            self.mainFrame, text="♡\n- Drums Macro -\n- created by -\n>> fearsomeorc1406 <<", 
            fg_color="transparent", 
            text_color=customTheme.activeThemeData["Theme"]["Navigation"]["WatermarkColor"], 
            font=customTheme.globalFont14
        )
        self.creditsLabel.grid(row=4, column=0, padx=(0, 235), pady=(220, 0), sticky="n")

        # PLAYBACK CONTROLS
        self.playButton = ctk.CTkButton(
            self.mainFrame, text="Play", 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PlayColor"], 
            width=80, command=drumsMacroFunctions.startPlayback, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"], 
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["PlayColorHover"]
        )
        self.playButton.grid(row=10, column=0, padx=45, pady=(0, 0), sticky="w")
        self.__class__.playButton = self.playButton
        ToolTip.CreateToolTip(self.playButton, text = 'Start Playback')

        self.stopButton = ctk.CTkButton(
            self.mainFrame, text="Stop",
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["StopColorDisabled"], 
            width=80, state="disabled", command=drumsMacroFunctions.stopPlayback, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"], 
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["StopColorHover"]
        )
        self.stopButton.grid(row=10, column=0, padx=130, pady=(0, 0), sticky="w")
        self.__class__.stopButton = self.stopButton

        # TIMESTAMP
        self.timelineText = "0:00:00 / 0:00:00" if configuration.configData['appUI']['timestamp'] else "X:XX:XX / 0:00:00"
        self.timelineIndicator = ctk.CTkLabel(
            self.mainFrame, text=self.timelineText, fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.timelineIndicator.grid(row=10, column=0, padx=(0, 50), pady=(0, 0), sticky="e")
        self.__class__.timelineIndicator = self.timelineIndicator

        # SPEED CONTROL
        self.speedLabel = ctk.CTkLabel(
            self.mainFrame, text="Speed", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.speedLabel.grid(row=9, column=0, padx=(0,290), pady=(15, 0))

        self.speedSlider = ctk.CTkSlider(
            self.mainFrame, from_=1, to=500, command=lambda value: settingsFunctions.updateFromSlider("drumsSpeedController", value), 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["SpeedSliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["SpeedSliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["SpeedSliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["SpeedSliderCircleHoverColor"]
        )
        self.speedSlider.grid(row=9, column=0, padx=(0,50), pady=(15, 0))
        self.__class__.speedSlider = self.speedSlider
        self.speedSlider.set(100)
        ToolTip.CreateToolTip(self.speedSlider, text = 'Playback Speed')

        self.resetSpeedButton = ctk.CTkButton(
            self.mainFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("drumsSpeedController"), font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["ButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColorDisabled"]
        )
        self.resetSpeedButton.grid(row=9, column=0, padx=(290, 0), pady=(15, 0))
        ToolTip.CreateToolTip(self.resetSpeedButton, text = 'Reset Speed')

        self.speedValueEntry = ctk.CTkEntry(
            self.mainFrame, placeholder_text="100", width=50, 
            fg_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["SpeedValueBoxBackColor"], 
            font=customTheme.globalFont14, 
            border_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["SpeedValueBoxBorderColor"], 
            text_color=customTheme.activeThemeData["Theme"]["DrumsMacro"]["TextColor"]
        )
        self.speedValueEntry.grid(row=9, column=0, padx=(200,0), pady=(15, 0))
        self.__class__.speedValueEntry = self.speedValueEntry
        self.speedValueEntry.insert(0, "100")
        ToolTip.CreateToolTip(self.speedValueEntry, text = 'Speed Value')

        self.speedValueEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("drumsSpeedController", value))
        self.speedValueEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("drumsSpeedController", value))
        self.speedSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("drumsSpeedController", value))