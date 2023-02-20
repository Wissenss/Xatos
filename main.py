import tkinter as tk
from tkinter import ttk
from kernel import init
from WTabGeneral import TabGeneral
from kernel.server import Server

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.minsize(800, 500)
        self.title("Xatos")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Cash-terminal.ico")

        self.style = ttk.Style(self)
        self.style.theme_use("xpnative")

        self.tab_control = ttk.Notebook(self)

        self.tabs = {
            TabGeneral : "General"
        }

        for tab in self.tabs:
            instance = tab(self.tab_control)
            self.tab_control.add(instance, text=self.tabs[tab])
            self.tabs[tab] = instance

        self.tab_control.pack(expand=1, fill=tk.BOTH)

if __name__ == "__main__":
    App().mainloop()