import customtkinter as ctk
import tkinter as tk
import json
import mido

from modules import configuration
from ui import customTheme
from ui.widget.tooltip import ToolTip

class MidiPlayerTab(ctk.CTkFrame):
    def __init__(self, master):
        from modules.functions import midiPlayerFunctions
        from modules.functions import mainFunctions
        from modules.functions import settingsFunctions
        super().__init__(master)
        customTheme.initializeFonts()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.midiFrame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["BackgroundColor"]
        )

        self.midiFrame.grid(row=0, column=0, sticky="nsew")
        self.midiFrame.grid_columnconfigure(0, weight=1)

        self.outputDeviceLabel = ctk.CTkLabel(
            self.midiFrame, text="MIDI Output Device", fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.outputDeviceLabel.grid(row=0, column=0, padx=(0, 200), pady=(10, 0), sticky="s")

        self.midiToggleSwitch = ctk.CTkSwitch(
            self.midiFrame, text="Use MIDI Output", command=midiPlayerFunctions.switchUseMIDI, variable=midiPlayerFunctions.switchUseMIDIvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.midiToggleSwitch.grid(row=0, column=0, padx=(0, 40), pady=(10, 0), sticky="e")
        ToolTip.CreateToolTip(self.midiToggleSwitch, text = 'Simulates MIDI signals to the\nselected MIDI Output Device\n\nNOTE: Having this enabled won\'t simulate\nQWERTY Keys for you if you\'re looking to macro.')

        self.outputDeviceDropdown = ctk.CTkOptionMenu(
            self.midiFrame, width=315, values=["Loading..."], font=customTheme.globalFont14, 
            dropdown_font=customTheme.globalFont14, command=None, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["OptionBackColor"], 
            dropdown_fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["OptionDropdownBackground"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["OptionDropdownButtonColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["OptionDropdownButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.outputDeviceDropdown.grid(row=1, column=0, padx=(0,35), pady=0)
        self.__class__.outputDeviceDropdown = self.outputDeviceDropdown
        self.__class__.midiToggleSwitch = self.midiToggleSwitch
        ToolTip.CreateToolTip(self.outputDeviceDropdown, text = 'Selected MIDI Output Device')

        self.refreshOutputDevices = ctk.CTkButton(
            self.midiFrame, image=customTheme.resetImageCTk, text="", width=30, command=mainFunctions.refreshOutputDevices, 
            font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.refreshOutputDevices.grid(row=1, column=0, padx=(320, 0), pady=(0, 0))
        ToolTip.CreateToolTip(self.refreshOutputDevices, text = 'Refresh MIDI Output Devices List')

        # MIDI FILE SELECTION
        self.filePathLabel = ctk.CTkLabel(
            self.midiFrame, text="MIDI File Path", fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.filePathLabel.grid(row=2, column=0, padx=(0,200), pady=(10, 0))

        self.filePathEntry = ctk.CTkOptionMenu(
            self.midiFrame, width=350, values="", command=midiPlayerFunctions.switchMidiEvent, font=customTheme.globalFont14, 
            dropdown_font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["OptionBackColor"], 
            dropdown_fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["OptionDropdownBackground"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["OptionDropdownButtonColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["OptionDropdownButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.filePathEntry.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.__class__.filePathEntry = self.filePathEntry
        ToolTip.CreateToolTip(self.filePathEntry, text = 'Selected MIDI File')

        self.selectFileButton = ctk.CTkButton(
            self.midiFrame, text="Select File", command=midiPlayerFunctions.selectFile, font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.selectFileButton.grid(row=2, column=0, padx=(0,55), pady=(10,0), sticky="e")
        ToolTip.CreateToolTip(self.selectFileButton, text = 'Select MIDI File (.mid | .midi)')

        # CONSOLE
        self.consoleFrame = tk.Frame(
            master=self.midiFrame, width=200, height=155, 
            bg=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ConsoleBackground"]
        )
        self.consoleFrame.grid(row=4, column=0, padx=(0,40), pady=(10,5), sticky="ne")
        self.consoleFrame.pack_propagate(0)
        self.__class__.consoleFrame = self.consoleFrame

        # HOTKEYS
        self.playHotkeyLabel = ctk.CTkLabel(
            self.midiFrame, text=" Play:", fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.playHotkeyLabel.grid(row=4, column=0, padx=(0, 300), pady=(0, 0), sticky="s")

        self.playHotkeyButton = ctk.CTkButton(
            self.midiFrame, text=configuration.configData["hotkeys"].get('play', 'f1').upper(), width=70, command=mainFunctions.playHotkeyCommand, 
            font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.playHotkeyButton.grid(row=4, column=0, padx=(0, 165), pady=(0, 0), sticky="s")
        self.__class__.playHotkeyButton = self.playHotkeyButton
        ToolTip.CreateToolTip(self.playHotkeyButton, text = 'Start Playback Hotkey')

        self.pauseHotkeyLabel = ctk.CTkLabel(
            self.midiFrame, text="Pause:", fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.pauseHotkeyLabel.grid(row=5, column=0, padx=(0, 300), pady=(2, 30), sticky="s")

        self.pauseHotkeyButton = ctk.CTkButton(
            self.midiFrame, text=configuration.configData["hotkeys"].get('pause', 'f2').upper(), width=70, command=mainFunctions.pauseHotkeyCommand, 
            font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.pauseHotkeyButton.grid(row=5, column=0, padx=(0, 165), pady=(0, 30), sticky="s")
        self.__class__.pauseHotkeyButton = self.pauseHotkeyButton
        ToolTip.CreateToolTip(self.pauseHotkeyButton, text = 'Pause Playback Hotkey')

        self.stopHotkeyLabel = ctk.CTkLabel(
            self.midiFrame, text=" Stop:", fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.stopHotkeyLabel.grid(row=5, column=0, padx=(0, 300), pady=(0, 0), sticky="s")

        self.stopHotkeyButton = ctk.CTkButton(
            self.midiFrame, text=configuration.configData["hotkeys"].get('stop', 'f3').upper(), width=70, command=mainFunctions.stopHotkeyCommand, 
            font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.stopHotkeyButton.grid(row=5, column=0, padx=(0, 165), pady=(0, 0), sticky="s")
        self.__class__.stopHotkeyButton = self.stopHotkeyButton
        ToolTip.CreateToolTip(self.stopHotkeyButton, text = 'Stop Playback Hotkey')

        self.slowDownHotkeyLabel = ctk.CTkLabel(
            self.midiFrame, text="Slow Down:", fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.slowDownHotkeyLabel.grid(row=5, column=0, padx=(80, 0), pady=(0, 30), sticky="s")

        self.speedUpHotkeyButton = ctk.CTkButton(
            self.midiFrame, text=configuration.configData["hotkeys"].get('speedup', 'f4').upper(), width=70, command=mainFunctions.speedUpHotkeyCommand, 
            font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.speedUpHotkeyButton.grid(row=5, column=0, padx=(250, 0), pady=(0, 30), sticky="s")
        self.__class__.speedUpHotkeyButton = self.speedUpHotkeyButton
        ToolTip.CreateToolTip(self.speedUpHotkeyButton, text = 'Speed-up Playback Hotkey')

        self.speedUpHotkeyLabel = ctk.CTkLabel(
            self.midiFrame, text=" Speed Up:", fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.speedUpHotkeyLabel.grid(row=5, column=0, padx=(80, 0), pady=(0, 0), sticky="s")

        self.slowHotkeyButton = ctk.CTkButton(
            self.midiFrame, text=configuration.configData["hotkeys"].get('slowdown', 'f5').upper(), width=70, command=mainFunctions.slowHotkeyCommand, 
            font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["HotkeySelectorHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.slowHotkeyButton.grid(row=5, column=0, padx=(250, 0), pady=(0, 0), sticky="s")
        self.__class__.slowHotkeyButton = self.slowHotkeyButton
        ToolTip.CreateToolTip(self.slowHotkeyButton, text = 'Slow-down Playback Hotkey')
        
        # TOGGLES
        """
        self.consoleToggle = ctk.CTkSwitch(
            self.midiFrame, text="Console", command=None, variable=None, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.consoleToggle.grid(row=4, column=0, padx=(184, 0), pady=(10, 10), sticky="nw")
        """
        
        self.sustainToggle = ctk.CTkSwitch(
            self.midiFrame, text="Sustain   ", command=midiPlayerFunctions.switchSustain, variable=midiPlayerFunctions.switchSustainvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.sustainToggle.grid(row=4, column=0, padx=(40, 0), pady=(10, 0), sticky="nw")
        self.__class__.sustainToggle = self.sustainToggle
        ToolTip.CreateToolTip(self.sustainToggle, text = 'Simulates Pedal by "Spacebar"\nOnly works on supported games.')

        self.noDoublesToggle = ctk.CTkSwitch(
            self.midiFrame, text="No Doubles", command=midiPlayerFunctions.switchNoDoubles, variable=midiPlayerFunctions.switchNoDoublesvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.noDoublesToggle.grid(row=4, column=0, padx=(40, 0), pady=(40, 0), sticky="nw")
        self.__class__.noDoublesToggle = self.noDoublesToggle
        ToolTip.CreateToolTip(self.noDoublesToggle, text = 'Prevents double-triggering of keys')

        self.velocityToggle = ctk.CTkSwitch(
            self.midiFrame, text="Velocity  ", command=midiPlayerFunctions.switchVelocity, variable=midiPlayerFunctions.switchVelocityvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.velocityToggle.grid(row=4, column=0, padx=(40, 0), pady=(70, 0), sticky="nw")
        self.__class__.velocityToggle = self.velocityToggle
        ToolTip.CreateToolTip(self.velocityToggle, text = 'Simulates how hard a key is pressed by "CTRL"\nwhich affects the loudness of that note\nOnly works on supported games.')

        self.use88KeysToggle = ctk.CTkSwitch(
            self.midiFrame, text="88 Keys   ", command=midiPlayerFunctions.switch88Keys, variable=midiPlayerFunctions.switch88Keysvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.use88KeysToggle.grid(row=4, column=0, padx=(40, 0), pady=(100, 10), sticky="nw")
        self.__class__.use88KeysToggle = self.use88KeysToggle
        ToolTip.CreateToolTip(self.use88KeysToggle, text = 'Simulate LowNote and HighNote by "CTRL"\nOnly works on supported games.')

        # PLAYBACK BUTTONS
        self.playButton = ctk.CTkButton(
            self.midiFrame, text="Play", fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["PlayColor"], 
            width=80, command=midiPlayerFunctions.playButton, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["PlayColorHover"]
        )
        self.playButton.grid(row=10, column=0, padx=45, pady=(0, 0), sticky="w")
        self.__class__.playButton = self.playButton
        ToolTip.CreateToolTip(self.playButton, text = 'Start Playback')

        self.stopButton = ctk.CTkButton(
            self.midiFrame, text="Stop", fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["StopColorDisabled"], 
            width=80, state="disabled", command=midiPlayerFunctions.stopPlayback, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["StopColorHover"]
        )
        self.stopButton.grid(row=10, column=0, padx=130, pady=(0, 0), sticky="w")
        self.__class__.stopButton = self.stopButton

        # TIMER
        self.timelineText = "0:00:00 / 0:00:00" if configuration.configData['appUI']['timestamp'] else "X:XX:XX / 0:00:00"

        self.timelineIndicator = ctk.CTkLabel(
            self.midiFrame, text=self.timelineText, fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.timelineIndicator.grid(row=10, column=0, padx=(0, 50), pady=(0, 0), sticky="e")
        self.__class__.timelineIndicator = self.timelineIndicator

        # SPEED CONTROL
        self.speedTextTitle = ctk.CTkLabel(
            self.midiFrame, text="Speed", fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.speedTextTitle.grid(row=9, column=0, padx=(0,290), pady=(5, 0))

        self.speedSlider = ctk.CTkSlider(
            self.midiFrame, from_=1, to=500, command=lambda value: settingsFunctions.updateFromSlider("midiSpeedController", value), 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SpeedSliderBackColor"], width=190,
            progress_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SpeedSliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SpeedSliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SpeedSliderCircleHoverColor"]
        )
        self.speedSlider.grid(row=9, column=0, padx=(0,50), pady=(5, 0))
        self.__class__.speedSlider = self.speedSlider
        self.speedSlider.set(100)
        ToolTip.CreateToolTip(self.speedSlider, text = 'Playback Speed')

        self.resetSpeedButton = ctk.CTkButton(
            self.midiFrame, image=customTheme.resetImageCTk, text="", width=30, command=lambda: settingsFunctions.resetControl("midiSpeedController"), 
            font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.resetSpeedButton.grid(row=9, column=0, padx=(290, 0), pady=(5, 0))
        ToolTip.CreateToolTip(self.resetSpeedButton, text = 'Reset Speed')

        self.speedValueEntry = ctk.CTkEntry(
            self.midiFrame, placeholder_text="100", width=50, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SpeedValueBoxBackColor"], 
            font=customTheme.globalFont14, 
            border_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["SpeedValueBoxBorderColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"]
        )
        self.speedValueEntry.grid(row=9, column=0, padx=(200,0), pady=(5, 0))
        self.__class__.speedValueEntry = self.speedValueEntry
        self.speedValueEntry.insert(0, "100")
        ToolTip.CreateToolTip(self.speedValueEntry, text = 'Speed Value')

        self.speedValueEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("midiSpeedController", value))
        self.speedValueEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("midiSpeedController", value))
        self.speedSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("midiSpeedController", value))

        mainFunctions.insertConsoleText("Hello! :)", ignoreConsoleCheck=False)