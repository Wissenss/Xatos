import tkinter as tk

class SellReport(tk.Toplevel):
    def __init__(self, owner, mode):
        super().__init__(owner)
        self.geometry("400x400")
        self.title("Reporte de Ventas")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Document-index.ico")