from ui import customTheme
from modules import configuration
from tkinter import Toplevel, LEFT, SOLID, Label

class ToolTip(object):
    def __init__(self, widget):
        customTheme.initializeFonts()
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showTip(self, text):
        if configuration.configData["appUI"]["tooltip"]:
            self.text = text
            if self.tipwindow or not self.text:
                return
            x, y, cx, cy = self.widget.bbox("insert")
            x = x + self.widget.winfo_rootx() + 57
            y = y + cy + self.widget.winfo_rooty() +27
            self.tipwindow = tw = Toplevel(self.widget)
            tw.wm_overrideredirect(1)
            tw.wm_attributes("-topmost", True)
            tw.wm_geometry("+%d+%d" % (x, y))
            label = Label(tw, text=self.text, justify=LEFT, fg="#ffffff",
                        background="#151515", relief=SOLID, borderwidth=1,
                        font=customTheme.globalFont14)
            label.pack(ipadx=1)

    def hideTip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def CreateToolTip(widget, text):
        toolTip = ToolTip(widget)
        def enter(event):
            toolTip.showTip(text)
        def leave(event):
            toolTip.hideTip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)