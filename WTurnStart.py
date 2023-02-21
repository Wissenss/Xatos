import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from datetime import datetime

from kernel.server import Server

from componentes.currencyEntry import CurrencyEntry

class TurnStart(simpledialog.Dialog):
    def __init__(self, owner):
        self.owner = owner
        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("250x100")
        self.title("Iniciar Turno")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Clock-play.ico")
        self.resizable(False, False)

        frame.pack(expand=True)

        tk.Label(frame, text="Efectivo en caja").grid(row=0, column=0, padx=5)
        self.cashOnBox = CurrencyEntry(frame)
        self.cashOnBox.grid(row=0, column=1)

    def buttonbox(self):
        buttonBox = tk.Frame(self)
        buttonBox.pack(side=tk.BOTTOM, anchor="e", padx=5, pady=5)
        
        ttk.Button(buttonBox, text="cancelar", command=self.BCancel).pack(side=tk.RIGHT)
        ttk.Button(buttonBox, text="Iniciar", command=self.BStart).pack(side=tk.RIGHT)
        
    def BStart(self):
        efectivo = float(self.cashOnBox.get())

        if (messagebox.askokcancel(parent=self, title="Confirmación", message=f"Esta por iniciar un turno. Desea continuar?\n  Efectivo en caja: ${efectivo:.2f}")):
            Server().SvcTurns.openTurn(efectivo)

        self.destroy()

    def BCancel(self):
        self.destroy()