import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

from kernel.types import Sale
from kernel.server import Server

from renderizador.renderer import render_ticket

from componentes.largeButton import LargeButton
from componentes.currencyEntry import CurrencyEntry

class Payment(simpledialog.Dialog):
    def __init__(self, owner, total):
        self.total = total
        self.owner = owner
        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("500x260")
        self.title("Generar Pago")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Coins-in-hand.ico")
        self.resizable(False, False)

        frame.pack(expand=True)

        self.priceLabel = tk.Label(frame, text="Por Pagar: $0.00", font=("Helvetica", 14))
        self.priceLabel.pack(side=tk.TOP, pady=10)

        entryBox = tk.Frame(frame)
        entryBox.pack(side=tk.TOP)

        LargeButton(entryBox, "", "./recursos/Fatcow-Farm-Fresh-Coins.32.png", self.focusEEfectivo, False).grid(row=0, column=0)
        self.EEfectivo = CurrencyEntry(entryBox, font=("helvetica", 14))
        self.EEfectivo.grid(row=0, column=1)
        self.EEfectivo.bind("<KeyRelease>", self.valueChange)

        self.EEfectivo.bind("<Return>", self.BEnterEnd)

        LargeButton(entryBox, "", "./recursos/Fatcow-Farm-Fresh-Card-amex-gold.32.png", self.focusETarjeta, False).grid(row=1, column=0)
        self.ETarjeta = CurrencyEntry(entryBox, font=("helvetica", 14))
        self.ETarjeta.grid(row=1, column=1)
        self.ETarjeta.bind("<KeyRelease>", self.valueChange)

        self.changeLabel = tk.Label(frame, text="Cambio: $0.00", font=("Helvetica", 12))
        self.changeLabel.pack(anchor="sw", padx=10, pady=(10, 0))

        self.updateData()

        return self.EEfectivo

    def buttonbox(self):
        LargeButton(self, "Terminar", "./recursos/Fatcow-Farm-Fresh-Company-generosity.32.png", self.Bend).pack(side=tk.RIGHT, padx=10, pady=(0, 10))

    def valueChange(self, event): #sobrecarga la funcion para poder manejar el event
        self.updateData()

    def updateData(self):
        pending = self.total

        cashPayment = float(self.EEfectivo.get()) if self.EEfectivo.get() != "" else 0.00
        cardPayment = float(self.ETarjeta.get()) if self.ETarjeta.get() != "" else 0.00 

        pending = pending - cashPayment - cardPayment
        change = -1*pending
        
        if pending > 0:
            self.priceLabel.config(text=f"Por Pagar: ${pending:.2f}") 
            self.changeLabel.config(text=f"Cambio: -${-1*change:.2f}")
            self.changeLabel.config(fg="red")
        else:
            self.priceLabel.config(text=f"Por Pagar: $0.00")
            self.changeLabel.config(fg="green") 
            self.changeLabel.config(text=f"Cambio: ${change:.2f}")

    def focusEEfectivo(self):
        self.EEfectivo.delete(0, tk.END)
        self.EEfectivo.focus_set()

    def focusETarjeta(self):
        self.ETarjeta.delete(0, tk.END)
        self.ETarjeta.focus_set()

    def BEnterEnd(self, envent):
        # if messagebox.askyesno("Terminar Venta", "Desea realizar la venta?")
        self.Bend()

    def Bend(self):
        cashPayment = float(self.EEfectivo.get()) if self.EEfectivo.get() != "" else 0.00
        cardPayment = float(self.ETarjeta.get()) if self.ETarjeta.get() != "" else 0.00
        change = -self.total + cashPayment + cardPayment
        if change < 0:
            messagebox.showwarning(parent=self, title="Datos Incorrectos", message="El total de la venta es menor al pago recibido\nRevise los datos introducidos.")
            return
        
        if cashPayment != 0:
            cashPayment -= change
        elif cardPayment != 0:
            cardPayment -= change

        today = datetime.now()
        sale = Sale()
        sale.Date = today.date()
        sale.Time = today.time() 
        sale.Total = self.total
        sale.CashPayment = cashPayment
        sale.CardPayment = cardPayment  

        Server().SvcSales.setSale(True, sale)

        self.owner.generateTicket()

        self.owner.clearData()
        self.destroy()
