import customtkinter as ctk
import tkinter as tk
import platform

from modules import configuration
from ui import customTheme
from ui.widget.piano import Piano
from ui.widget.tooltip import ToolTip

osName = platform.system()

class MidiToQwertyTab(ctk.CTkFrame):
    def __init__(self, master):
        from modules.functions import midiToQWERTYFunctions
        from modules.functions import settingsFunctions
        from modules.functions import mainFunctions
        super().__init__(master)
        customTheme.initializeFonts()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.midiFrame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["BackgroundColor"]
        )
        self.midiFrame.grid(row=0, column=0, sticky="nsew")
        self.midiFrame.grid_columnconfigure(0, weight=1)

        self.inputDeviceLabel = ctk.CTkLabel(
            self.midiFrame, text="MIDI Input Device", fg_color="transparent", font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColorDisabled"]
        )
        self.inputDeviceLabel.grid(row=0, column=0, padx=(0, 220), pady=(10, 0), sticky="s")

        self.inputDeviceDropdown = ctk.CTkOptionMenu(
            self.midiFrame, width=330, values=["Loading..."], font=customTheme.globalFont14, 
            dropdown_font=customTheme.globalFont14, command=None, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["OptionBackColor"], 
            dropdown_fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["OptionDropdownBackground"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["OptionDropdownButtonColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["OptionDropdownButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColorDisabled"]
        )
        self.inputDeviceDropdown.grid(row=1, column=0, padx=(0,40), pady=0)
        self.__class__.inputDeviceDropdown = self.inputDeviceDropdown
        ToolTip.CreateToolTip(self.inputDeviceDropdown, text = 'Selected MIDI Input Device')

        self.refreshInputDevices = ctk.CTkButton(
            self.midiFrame, image=customTheme.resetImageCTk, text="", width=30, command=mainFunctions.refreshInputDevices, 
            font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["ButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiPlayer"]["TextColorDisabled"]
        )
        self.refreshInputDevices.grid(row=1, column=0, padx=(330, 0), pady=(0, 0))
        ToolTip.CreateToolTip(self.refreshInputDevices, text = 'Refresh MIDI Input Device List')

        self.consoleFrame = tk.Frame(
            master=self.midiFrame, width=200, height=265, 
            bg=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["ConsoleBackground"]
        )
        self.consoleFrame.grid(row=4, column=0, padx=(0,40), pady=(10,5), sticky="ne")
        self.consoleFrame.pack_propagate(0)
        self.__class__.consoleFrame = self.consoleFrame

        self.sustainToggle = ctk.CTkSwitch(
            self.midiFrame, text="Sustain   ", command=midiToQWERTYFunctions.switchSustain, variable=midiToQWERTYFunctions.switchSustainvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColorDisabled"]
        )
        self.sustainToggle.grid(row=4, column=0, padx=(40, 0), pady=(5, 0), sticky="nw")
        self.__class__.sustainToggle = self.sustainToggle
        ToolTip.CreateToolTip(self.sustainToggle, text = 'Simulates Pedal by "Spacebar"\nOnly works on supported games.')

        self.noDoublesToggle = ctk.CTkSwitch(
            self.midiFrame, text="No Doubles", command=midiToQWERTYFunctions.switchNoDoubles, variable=midiToQWERTYFunctions.switchNoDoublesvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColorDisabled"]
        )
        self.noDoublesToggle.grid(row=4, column=0, padx=(40, 0), pady=(30, 0), sticky="nw")
        self.__class__.noDoublesToggle = self.noDoublesToggle
        ToolTip.CreateToolTip(self.noDoublesToggle, text = 'Prevents double-triggering of keys')

        self.velocityToggle = ctk.CTkSwitch(
            self.midiFrame, text="Velocity  ", command=midiToQWERTYFunctions.switchVelocity, variable=midiToQWERTYFunctions.switchVelocityvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColorDisabled"]
        )
        self.velocityToggle.grid(row=4, column=0, padx=(40, 0), pady=(55, 0), sticky="nw")
        self.__class__.velocityToggle = self.velocityToggle
        ToolTip.CreateToolTip(self.velocityToggle, text = 'Simulates how hard a key is pressed by "CTRL"\nwhich affects the loudness of that note\nOnly works on supported games.')

        self.use88KeysToggle = ctk.CTkSwitch(
            self.midiFrame, text="88 Keys   ", command=midiToQWERTYFunctions.switch88Keys, variable=midiToQWERTYFunctions.switch88Keysvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColorDisabled"]
        )
        self.use88KeysToggle.grid(row=4, column=0, padx=(40, 0), pady=(80, 10), sticky="nw")
        self.__class__.use88KeysToggle = self.use88KeysToggle
        ToolTip.CreateToolTip(self.use88KeysToggle, text = 'Simulate LowNote and HighNote by "CTRL"\nOnly works on supported games.')

        self.sustainCutoffLabel = ctk.CTkLabel(
            self.midiFrame, text="Sustain\nCutoff", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.sustainCutoffLabel.grid(row=4, column=0, padx=(40,0), pady=(110, 0), sticky="nw")

        self.sustainCutoffSlider = ctk.CTkSlider(
            self.midiFrame, from_=0, to=127, width=127, command=lambda value: settingsFunctions.updateFromSlider("midiToQWERTYSustainCutoff", value), 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleHoverColor"]
        )
        self.sustainCutoffSlider.grid(row=4, column=0, padx=(35,0), pady=(145, 0), sticky="nw")
        self.sustainCutoffSlider.set(configuration.configData['midiToQwerty']['sustainCutoff'])
        self.__class__.sustainCutoffSlider = self.sustainCutoffSlider
        ToolTip.CreateToolTip(self.sustainCutoffSlider, text = 'Controls sustain pedal\nDefault: 63')

        self.resetSustainCutoff = ctk.CTkButton(
            self.midiFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("midiToQWERTYSustainCutoff"), font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.resetSustainCutoff.grid(row=4, column=0, padx=(143,0), pady=(110, 0), sticky="nw")
        ToolTip.CreateToolTip(self.resetSustainCutoff, text = 'Reset Sustain Cutoff')

        self.sustainCutoffEntry = ctk.CTkEntry(
            self.midiFrame, placeholder_text="63", width=40, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            border_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBorderColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBackColor"]
        )
        self.sustainCutoffEntry.grid(row=4, column=0, padx=(100,0), pady=(110, 0), sticky="nw")
        self.sustainCutoffEntry.insert(0, configuration.configData['midiToQwerty']['sustainCutoff'])
        self.__class__.sustainCutoffEntry = self.sustainCutoffEntry
        ToolTip.CreateToolTip(self.sustainCutoffEntry, text = 'Sustain Cutoff Value\nDefault: 63')

        self.sustainCutoffEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("midiToQWERTYSustainCutoff", value))
        self.sustainCutoffEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("midiToQWERTYSustainCutoff", value))
        self.sustainCutoffSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("midiToQWERTYSustainCutoff", value))

        self.customHoldLengthToggle = ctk.CTkSwitch(
            self.midiFrame, text="Custom Hold\nLength", command=midiToQWERTYFunctions.switchCustomHoldLength, variable=midiToQWERTYFunctions.switchCustomHoldLengthvar, font=customTheme.globalFont14, 
            onvalue="on", offvalue="off", fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchDisabled"], 
            progress_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchEnabled"], 
            button_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircle"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["SwitchCircleHovered"], 
            text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColorDisabled"]
        )
        self.customHoldLengthToggle.grid(row=4, column=0, padx=(40,0), pady=(165, 0), sticky="nw")
        ToolTip.CreateToolTip(self.customHoldLengthToggle, text = 'Custom Note Hold Length')

        self.customHoldLengthSlider = ctk.CTkSlider(
            self.midiFrame, from_=0, to=10, width=140, command=lambda value: settingsFunctions.updateFromSlider("midiToQWERTYNoteLength", value), 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderBackColor"], 
            progress_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderFillColor"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["SliderCircleHoverColor"]
        )
        self.customHoldLengthSlider.grid(row=4, column=0, padx=(35,0), pady=(200, 0), sticky="nw")
        self.customHoldLengthSlider.set(configuration.configData['midiToQwerty']['customHoldLength']['noteLength'])
        self.__class__.customHoldLengthSlider = self.customHoldLengthSlider
        ToolTip.CreateToolTip(self.customHoldLengthSlider, text = 'Custom Note Hold Length')

        self.resetCustomHoldLength = ctk.CTkButton(
            self.midiFrame, image=customTheme.resetImageCTk, text="", width=30, 
            command=lambda: settingsFunctions.resetControl("midiToQWERTYNoteLength"), font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonColor"], 
            hover_color=customTheme.activeThemeData["Theme"]["Settings"]["ButtonHoverColor"]
        )
        self.resetCustomHoldLength.grid(row=4, column=0, padx=(143,0), pady=(220, 0), sticky="nw")
        self.__class__.resetCustomHoldLength = self.resetCustomHoldLength
        ToolTip.CreateToolTip(self.resetCustomHoldLength, text = 'Reset Note Hold Length')

        self.customHoldLengthEntry = ctk.CTkEntry(
            self.midiFrame, placeholder_text="0.1", width=95, 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            border_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBorderColor"], 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["ValueBoxBackColor"]
        )
        self.customHoldLengthEntry.grid(row=4, column=0, padx=(45,0), pady=(220, 0), sticky="nw")
        self.customHoldLengthEntry.insert(0, configuration.configData['midiToQwerty']['customHoldLength']['noteLength'])
        self.__class__.customHoldLengthEntry = self.customHoldLengthEntry
        ToolTip.CreateToolTip(self.customHoldLengthEntry, text = 'Custom Note Hold Length Value')

        self.customHoldLengthEntry.bind("<FocusOut>", lambda value: settingsFunctions.updateFromEntry("midiToQWERTYNoteLength", value))
        self.customHoldLengthEntry.bind("<KeyRelease>", lambda value: settingsFunctions.updateFromEntry("midiToQWERTYNoteLength", value))
        self.customHoldLengthSlider.bind("<ButtonRelease-1>", lambda value: settingsFunctions.updateFromEntry("midiToQWERTYNoteLength", value))

        self.moduleSelectorText = ctk.CTkLabel(
            self.midiFrame, text="Keyboard Module", fg_color="transparent", 
            font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"]
        )
        self.moduleSelectorText.grid(row=4, column=0, padx=(0, 270), pady=(20, 0), sticky="es")

        self.moduleSelector = ctk.CTkOptionMenu(
            self.midiFrame, width=130, command=midiToQWERTYFunctions.onModuleSelect, values=["pynput", "keyboard"], 
            font=customTheme.globalFont14, dropdown_font=customTheme.globalFont14, 
            fg_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionBackColor"], 
            dropdown_fg_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownBackground"], 
            button_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownButtonColor"], 
            button_hover_color=customTheme.activeThemeData["Theme"]["Settings"]["OptionDropdownButtonHoverColor"], 
            text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            dropdown_text_color=customTheme.activeThemeData["Theme"]["Settings"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["Settings"]["TextColorDisabled"]
        )

        self.moduleSelector.grid(row=5, column=0, padx=(0, 265), pady=(0, 0), sticky="es")
        
        if osName != "Windows":
            self.moduleSelector.set("Unavailable")
            self.moduleSelector.configure(state="disabled")
        else:
            self.moduleSelector.set(configuration.configData.get("midiToQwerty", {}).get("inputModule", "pynput"))
        
        ToolTip.CreateToolTip(self.moduleSelector, text = 'Module for simulating keypresses')

        self.toggleListener = ctk.CTkButton(
            self.midiFrame, text="Enable", fg_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["PlayColor"], 
            width=200, command=midiToQWERTYFunctions.playButton, font=customTheme.globalFont14, 
            text_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColor"], 
            text_color_disabled=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["TextColorDisabled"], 
            hover_color=customTheme.activeThemeData["Theme"]["MidiToQWERTY"]["PlayColorHover"]
        )
        self.toggleListener.grid(row=5, column=0, padx=(0,40), pady=(0,0), sticky="ne")
        self.__class__.toggleListener = self.toggleListener
        ToolTip.CreateToolTip(self.toggleListener, text = 'Start Listening to MIDI Input Device')

        self.midiFrame.grid_rowconfigure(20, weight=1)
        self.piano = Piano(self.midiFrame)
        self.piano.grid(row=21, column=0, sticky="sew", padx=10, pady=(5, 10))
