import tkinter as tk
from tkinter import ttk
from generalTab import GeneralTab
from kernel.server import Server

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.title("Xato's")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Cash-terminal.ico")

        self.tab_control = ttk.Notebook(self)

        self.tabs = {
            GeneralTab : "General"
        }

        for tab in self.tabs:
            instance = tab(self.tab_control)
            self.tab_control.add(instance, text=self.tabs[tab])
            self.tabs[tab] = instance

        self.tab_control.pack(expand=1, fill=tk.BOTH)

if __name__ == "__main__":

    App().mainloop()