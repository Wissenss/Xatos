import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from datetime import datetime

from kernel.server import Server

from componentes.currencyEntry import CurrencyEntry

class TurnEnd(simpledialog.Dialog):
    def __init__(self, owner):
        self.owner = owner
        self.efectivoEsperado = 0.00
        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("250x100")
        self.title("Iniciar Turno")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Clock-play.ico")
        self.resizable(False, False)

        frame.pack(expand=True)

        self.cashExpected = tk.Label(frame, text=f"Efectivo Esperado: {0.00:.2f}", font=(None, 12))
        self.cashExpected.grid(row=0, column=0, columnspan=2, sticky="nswe")

        tk.Label(frame, text="En caja").grid(row=1, column=0, pady=(10, 0), padx=5)
        self.cashOnBox = CurrencyEntry(frame)
        self.cashOnBox.grid(row=1, column=1, pady=(10, 0))

        self.load()

    def buttonbox(self):
        buttonBox = tk.Frame(self)
        buttonBox.pack(side=tk.BOTTOM, anchor="e", padx=5, pady=5)
        
        ttk.Button(buttonBox, text="cancelar", command=self.BCancel).pack(side=tk.RIGHT)
        ttk.Button(buttonBox, text="Terminar", command=self.BEnd).pack(side=tk.RIGHT)
        
    def load(self):
        self.efectivoEsperado = Server().SvcTurns.getCashCount()
        self.cashExpected.config(text=f"Efectivo Esperado: {self.efectivoEsperado:.2f}")

    def BEnd(self):
        efectivo = 0.00
        if self.cashOnBox != "":
            efectivo = float(self.cashOnBox.get()) 
        
        if efectivo != self.efectivoEsperado:
            messagebox.showerror(parent=self, title="Error", message=f"El efectivo en caja es distinto al esperado. Revise el conteo\n  Efectivo espreado: ${self.efectivoEsperado:.2f}\n  En caja: ${efectivo:.2f}")
            self.cashOnBox.focus()
            return

        if (messagebox.askokcancel(parent=self, title="Confirmación", message=f"Esta por cerrar el turno. Desea continuar?\n  Efectivo en caja: ${efectivo:.2f}")):
            Server().SvcTurns.closeTurn(efectivo)
            return self.destroy()

    def BCancel(self):
        self.destroy()