import tkinter as tk
from tkinter import simpledialog

class SellReport(simpledialog.Dialog):
    def __init__(self, owner, mode):
        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("400x400")
        self.title("Reporte de Ventas")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Document-index.ico")

    def buttonbox(self):
        pass