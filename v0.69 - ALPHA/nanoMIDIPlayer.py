import customtkinter
import os
from PIL import Image
from tkinter import filedialog
import threading
import mido
from mido import MidiFile
import keyboard
import datetime
import time
import requests

class App(customtkinter.CTk):
    def __init__(self):

        self.playback_state = False
        self.playback_start_time = None
        self.last_update_time = None
        self.hotkey = "F1"
        keyboard.on_press_key(self.hotkey, self.toggle_playback)
        self.midi_port_lock = threading.Lock()

        super().__init__()
        themejsurl = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/main/assets/theme.json"
        themejs = os.path.join(os.path.dirname(__file__), "temp_theme.json")
        with open(themejs, 'w') as f:
            f.write(requests.get(themejsurl).text)

        customtkinter.set_default_color_theme(themejs)

        consolas_font = customtkinter.CTkFont(size=14, weight="bold", family="Consolas")

        self.title("nanoMIDIPlayer [BETA]")
        self.geometry("600x450")
        self.resizable(False, False)

        icon_url = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/main/assets/icon.ico"
        bannerimage = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/main/assets/banner.png"
        resetimage = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/main/assets/reset.png"
        pianoimage = "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/main/assets/piano.png"

        icon_path = os.path.join(os.path.dirname(__file__), "temp_icon.ico")
        with open(icon_path, 'wb') as f:
            f.write(requests.get(icon_url).content)

        self.iconbitmap(icon_path)

        self.logo_image = customtkinter.CTkImage(Image.open(requests.get(bannerimage, stream=True).raw), size=(86, 26))
        self.reset_image = customtkinter.CTkImage(Image.open(requests.get(resetimage, stream=True).raw), size=(16, 16))
        self.pianoimage = customtkinter.CTkImage(Image.open(requests.get(pianoimage, stream=True).raw), size=(20, 20))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, text="", image=self.logo_image,
            compound="left", font=customtkinter.CTkFont(size=15, weight="bold", family="Consolas")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="MIDI Player",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray7", "gray7"),
            image=self.pianoimage, anchor="w", font=consolas_font, command=self.home_button_event
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.versionlabel = customtkinter.CTkLabel(
            self.navigation_frame, text="nanoMIDI // v0.69", fg_color="transparent", text_color="#191919", font=consolas_font
        )
        self.versionlabel.grid(row=6, column=0, padx=20, pady=1, sticky="s")

        def combo():
            print("a")

        # MIDI
        self.home_frame = customtkinter.CTkFrame(self.master, corner_radius=0, fg_color="#0A0A0A")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_label_1 = customtkinter.CTkLabel(
            self.home_frame, text="MIDI Output Device", fg_color="transparent", font=consolas_font
        )
        self.home_frame_label_1.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.output_devices = mido.get_output_names()
        loopbe_device = next((device for device in self.output_devices if "LoopBe" in device), None)

        self.home_frame_combobox_1 = customtkinter.CTkOptionMenu(
            self.home_frame, width=350, values=self.output_devices, command=combo, font=consolas_font
        )
        default_device = loopbe_device if loopbe_device else self.output_devices[0]
        self.home_frame_combobox_1.set(default_device)
        self.home_frame_combobox_1.grid(row=1, column=0, padx=0, pady=0)

        self.home_frame_label_2 = customtkinter.CTkLabel(
            self.home_frame, text="MIDI File Path", fg_color="transparent", font=consolas_font
        )
        self.home_frame_label_2.grid(row=2, column=0, padx=(0,200), pady=(10, 0))

        self.home_frame_entry_1 = customtkinter.CTkEntry(self.home_frame, width=350, placeholder_text="/midi.mid")
        self.home_frame_entry_1.grid(row=3, column=0, padx=20, pady=(10, 0))

        self.select_file_button = customtkinter.CTkButton(
            self.home_frame, text="Select File", command=self.open_file_dialog, font=consolas_font
        )
        self.select_file_button.grid(row=2, column=0, padx=(0,55), pady=(10,0), sticky="e")

        self.play_button = customtkinter.CTkButton(
            self.home_frame, text="Play",fg_color="#006900", command=self.toggle_playback, font=consolas_font
        )
        self.play_button.grid(row=9, column=0, padx=(0, 200), pady=(10, 0), sticky="s")

        self.home_frame_label_3 = customtkinter.CTkLabel(
            self.home_frame, text="Hotkey:", fg_color="transparent", font=consolas_font
        )
        self.home_frame_label_3.grid(row=9, column=0, padx=(120,0), pady=(10, 0), sticky="s")

        self.play_hotkey = customtkinter.CTkButton(
            self.home_frame, text="F1", width=70, command=self.get_hotkey, font=consolas_font
        )
        self.play_hotkey.grid(row=9, column=0, padx=(260, 0), pady=(10, 0), sticky="s")

        self.timeline = customtkinter.CTkLabel(
            self.home_frame, text="0:00:00 / 0:00:00", fg_color="transparent", font=consolas_font
        )
        self.timeline.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.speedlabel = customtkinter.CTkLabel(
            self.home_frame, text="Speed", fg_color="transparent", font=consolas_font
        )
        self.speedlabel.grid(row=6, column=0, padx=(0,290), pady=(190, 0))

        self.speed = customtkinter.CTkSlider(self.home_frame, from_=50, to=1000, command=self.sliderupdate)
        self.speed.grid(row=6, column=0, padx=(0,50), pady=(190, 0))
        self.speed.set(100)

        self.resetspeed = customtkinter.CTkButton(
            self.home_frame, image=self.reset_image, text="", width=30, command=self.resetspeedvalue, font=consolas_font
        )
        self.resetspeed.grid(row=6, column=0, padx=(290, 0), pady=(190, 0))

        self.speedtext = customtkinter.CTkEntry(
            self.home_frame, placeholder_text="100", width=50, fg_color="transparent", font=consolas_font
        )
        self.speedtext.grid(row=6, column=0, padx=(200,0), pady=(190, 0))
        self.speedtext.insert(0, "100")

        self.speedtext.bind("<FocusOut>", self.slidertoentry)
        self.speedtext.bind("<KeyRelease>", self.slidertoentry)
        self.speed.bind("<ButtonRelease-1>", self.entrytoslider)

        self.stop_playback_flag = threading.Event()

        self.select_frame_by_name("home")

    def sliderupdate(self, value):
        rounded_value = round(float(value))
        self.speedtext.delete(0, "end")
        self.speedtext.insert(0, str(rounded_value))

    def slidertoentry(self, event=None):
        try:
            value = float(self.speedtext.get())
            if 50 <= value <= 1000:
                self.speed.set(value)
        except ValueError:
            pass

    def entrytoslider(self, event):
        value = self.speed.get()
        self.speedtext.delete(0, "end")
        self.speedtext.insert(0, str(value))

    def resetspeedvalue(self):
        self.speedtext.delete(0, "end")
        self.speedtext.insert(0, 100)
        self.speed.set(100)

    def get_hotkey(self):
        keyboard.unhook_all()
        self.play_hotkey.configure(text="Press Key")
        self.bind("<Key>", self.get_pressed_key)

    def get_pressed_key(self, event):
        new_hotkey = event.keysym
        self.play_hotkey.configure(text=new_hotkey)

        self.hotkey = new_hotkey

        keyboard.unhook_all()
        keyboard.on_press_key(new_hotkey, self.toggle_playback)

        self.unbind("<Key>")

    def toggle_playback(self, e=None):
        if self.playback_state:
            self.stop_playback_flag.set()
            self.playback_state = False
            self.play_button.configure(text="Play", fg_color="#006900")
        else:
            self.stop_playback_flag.clear()
            playback_thread = threading.Thread(target=self.play_midi, daemon=True)
            playback_thread.start()
            self.playback_state = True
            self.play_button.configure(text="Stop", fg_color="#FF1800")
            self.update_timeline()

    def play_midi_threaded(self):
        with self.midi_port_lock:
            playback_thread = threading.Thread(target=self.play_midi, daemon=True)
            playback_thread.start()

    def play_midi(self):
        selected_device = self.home_frame_combobox_1.get()
        midi_file_path = self.home_frame_entry_1.get()

        if selected_device and midi_file_path:
            try:
                with self.midi_port_lock:
                    self.midi_file = MidiFile(midi_file_path)
                    midi_port = mido.open_output(selected_device)

                    ticks_per_beat = self.midi_file.ticks_per_beat

                    speed_factor = self.speed.get() / 100.0

                    self.playback_start_time = time.time()

                    for track in self.midi_file.tracks:
                        for msg in track:
                            if hasattr(msg, 'time'):
                                msg.time = int(msg.time / speed_factor)

                    for msg in self.midi_file.play():
                        if self.stop_playback_flag.is_set():
                            break

                        midi_port.send(msg)

                    midi_port.close()

            except Exception as e:
                print(f"{e}")

            self.playback_state = False
            self.play_button.configure(text="Play", fg_color="#006900")
            self.playback_start_time = None
            total_time = self.midi_file.length
            self.timeline.configure(text=f"0:00:00 / {str(datetime.timedelta(seconds=int(total_time)))}")

    def update_timeline(self):
        if self.playback_start_time is not None and self.playback_state:
            elapsed_time = time.time() - self.playback_start_time
            total_time = self.midi_file.length
            elapsed_time_str = str(datetime.timedelta(seconds=int(elapsed_time)))
            total_time_str = str(datetime.timedelta(seconds=int(total_time)))
            timeline_text = f"{elapsed_time_str} / {total_time_str}"
            self.timeline.configure(text=timeline_text)
            self.after(1000, self.update_timeline)

    def on_close(self):
        self.stop_playback_flag.set()
        keyboard.unhook_all()

    def open_file_dialog(self):
        self.stop_playback_flag.set()
        self.playback_state = False
        self.play_button.configure(text="Play")

        keyboard.unhook_all()

        file_path = filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid;*.midi")])
        if file_path:
            self.home_frame_entry_1.delete(0, "end")
            self.home_frame_entry_1.insert(0, file_path)

            midi_file = MidiFile(file_path)
            self.total_time = midi_file.length
            self.timeline.configure(text=f"0:00:00 / {str(datetime.timedelta(seconds=int(self.total_time)))}")

            keyboard.on_press_key(self.hotkey, self.toggle_playback)

    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray5", "gray5") if name == "home" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")


if __name__ == "__main__":
    app = App()
    app.mainloop()