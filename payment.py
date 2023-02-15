import tkinter as tk
from tkinter import simpledialog

from kernel.types import Sell

from componentes.largeButton import LargeButton

class Payment(simpledialog.Dialog):
    def __init__(self, owner, data:Sell):
        self.data = data
        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("500x250")
        self.title("Generar Pago")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Coins-in-hand.ico")
        self.resizable(False, False)

        frame.pack(expand=True)

        self.priceLabel = tk.Label(frame, text="Por Pagar: $0.00", font=("Helvetica", 14))
        self.priceLabel.pack(side=tk.TOP, pady=10)

        entryBox = tk.Frame(frame)
        entryBox.pack(side=tk.TOP)

        LargeButton(entryBox, "", "./recursos/Fatcow-Farm-Fresh-Coins.32.png", lambda:None).grid(row=0, column=0)
        self.EEfectivo = tk.Entry(entryBox)
        self.EEfectivo.grid(row=0, column=1)

        LargeButton(entryBox, "", "./recursos/Fatcow-Farm-Fresh-Card-amex-gold.32.png", lambda:None).grid(row=0, column=2)
        self.ETarjeta = tk.Entry(entryBox)
        self.ETarjeta.grid(row=0, column=3)

        self.changeLabel = tk.Label(frame, text="Cambio: $0.00", font=("Helvetica", 12))
        self.changeLabel.pack(anchor="sw", padx=10, pady=10)

        self.updateData()

    def buttonbox(self):
        LargeButton(self, "Terminar", "./recursos/Fatcow-Farm-Fresh-Company-generosity.32.png", lambda:self.Bend).pack(side=tk.RIGHT, padx=10, pady=(0, 10))

    def filterNumericInput(self, event): 
        pass

    def updateData(self):
        pending = self.data.Total

        cashPayment = float(self.EEfectivo.get()) if self.EEfectivo.get() != "" else 0.00
        cardPayment = float(self.ETarjeta.get()) if self.ETarjeta.get() != "" else 0.00 

        pending = pending - cashPayment - cardPayment
        change = -1*pending
        
        if pending >=0:
            self.priceLabel.config(text=f"Por Pagar: ${pending:.2f}") 
            self.changeLabel.config(text=f"Cambio: ${change:.2f}")
            self.changeLabel.config(fg="red")
        else:
            self.priceLabel.config(text=f"Por Pagar: ${pending:.2f}")
            self.changeLabel.config(fg="green") 
            self.changeLabel.config(text=f"Cambio: -${-1*change:.2f}")

    def Bend(self):
        # print ticket
        pass