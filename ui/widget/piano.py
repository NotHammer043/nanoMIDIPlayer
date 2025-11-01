import customtkinter as ctk
from ui import customTheme

class Piano(ctk.CTkFrame):
    def __init__(self, master=None, keyWidth=8.01, blackKeyWidth=5.5, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.keyWidth = keyWidth
        self.blackKeyWidth = blackKeyWidth
        self.whiteKeyHeight = 60
        self.blackKeyHeight = 40

        theme = customTheme.activeThemeData["Theme"]["MidiToQWERTY"]
        self.whiteColor = theme["WhiteNoteColor"]
        self.whiteHeldColor = theme["WhiteNoteColorHeld"]
        self.blackColor = theme["BlackNoteColor"]
        self.blackHeldColor = theme["BlackNoteColorHeld"]

        self.canvas = ctk.CTkCanvas(
            self,
            width=52 * self.keyWidth,
            height=self.whiteKeyHeight,
            bg="gray20",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.keyStates = [0] * 256
        self.keyMap = {}
        self.heldKey = None

        self.drawKeys()

        self.canvas.bind("<Button-1>", self.onClick)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)

    def hasBlack(self, key):
        return not ((key - 1) % 7 == 0 or (key - 1) % 7 == 3) and key != 51

    def drawKeys(self):
        curKey = 21
        for i in range(52):
            x1 = i * self.keyWidth
            x2 = x1 + self.keyWidth
            rect = self.canvas.create_rectangle(
                x1, 0, x2, self.whiteKeyHeight,
                fill=self.whiteColor, outline="black"
            )
            self.keyMap[rect] = (curKey, "white")
            curKey += 1
            if self.hasBlack(i):
                curKey += 1

        curKey = 22
        for i in range(52):
            if self.hasBlack(i):
                xCenter = i * self.keyWidth + self.keyWidth
                x1 = xCenter - self.blackKeyWidth // 2
                x2 = xCenter + self.blackKeyWidth // 2
                rect = self.canvas.create_rectangle(
                    x1, 0, x2, self.blackKeyHeight,
                    fill=self.blackColor, outline="black"
                )
                self.keyMap[rect] = (curKey, "black")
                curKey += 2
            else:
                curKey += 1

    def onClick(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            keyInfo = self.keyMap.get(item[0])
            if keyInfo:
                key, _ = keyInfo
                self.down(key, velocity=127)
                self.heldKey = key

    def onRelease(self, event):
        if self.heldKey is not None:
            self.up(self.heldKey)
            self.heldKey = None

    def down(self, key, velocity):
        self.keyStates[key] = velocity
        for rect, (k, kind) in self.keyMap.items():
            if k == key:
                if kind == "white":
                    self.canvas.itemconfig(rect, fill=self.whiteHeldColor)
                else:
                    self.canvas.itemconfig(rect, fill=self.blackHeldColor)

    def up(self, key):
        self.keyStates[key] = 0
        for rect, (k, kind) in self.keyMap.items():
            if k == key:
                if kind == "white":
                    self.canvas.itemconfig(rect, fill=self.whiteColor)
                else:
                    self.canvas.itemconfig(rect, fill=self.blackColor)

    def currentNotes(self):
        return [i for i, v in enumerate(self.keyStates) if v > 0]
