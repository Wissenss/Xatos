import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkcalendar import DateEntry

from kernel.server import Server

from datetime import datetime

class SalesReport(simpledialog.Dialog):
    def __init__(self, owner, mode):
        self.selectedDate = datetime.today()
        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("450x490")
        self.title("Reporte de Ventas")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Document-index.ico")
        self.resizable(False, False)

        frame.pack(side=tk.TOP)
        
        tk.Label(frame, text="Fecha").grid(row=0, column=0, pady=20)
        self.Edate = DateEntry(frame, localestr="es_ES")
        self.Edate.grid(row=0, column=1, pady=20)
        ttk.Button(frame, text="Generar Reporte", command=self.generateReport).grid(row=0, column=2, pady=20)

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=4, sticky="nswe")

        tk.Label(frame, text="Ventas").grid(row=2, column=0, columnspan=2, sticky="sw", pady=5)

        self.salesList = ttk.Treeview(frame, columns=("Hora", "MontoTotal", "PagoEnEfectivo", "PagoEnTarjeta"), show="headings")
        self.salesList.column("Hora", width=80, anchor=tk.CENTER)
        self.salesList.column("MontoTotal", width=80, anchor=tk.CENTER)
        self.salesList.column("PagoEnEfectivo", width=100, anchor=tk.CENTER)
        self.salesList.column("PagoEnTarjeta", width=100, anchor=tk.CENTER)
        self.salesList.heading("Hora", text="Hora")
        self.salesList.heading("MontoTotal", text="Monto")
        self.salesList.heading("PagoEnEfectivo", text="Pago en efectivo")
        self.salesList.heading("PagoEnTarjeta", text="Pago en tarjeta")
        self.salesList.grid(row=3, column=0, columnspan=4, sticky="nswe", pady=5)

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=4, sticky="nswe", pady=(10, 5))

        tk.Label(frame, text="Ingresos").grid(row=5, column=0, columnspan=2, sticky="sw", pady=5)

        tk.Label(frame, text="Total").grid(row=6, column=0, pady=5, padx=5, sticky="sw")
        self.salesTotal = ttk.Entry(frame, state='disabled', justify=tk.RIGHT)
        self.salesTotal.grid(row=6, column=1, pady=5, sticky="sw")

        tk.Label(frame, text="Efectivo").grid(row=7, column=0, pady=5, padx=5, sticky="sw")
        self.cashTotal = ttk.Entry(frame, state='disabled', justify=tk.RIGHT)
        self.cashTotal.grid(row=7, column=1, pady=5, sticky="sw")
        tk.Label(frame, text="Tarjeta").grid(row=7, column=2, pady=5, padx=5, sticky="se")
        self.cardTotal = ttk.Entry(frame, state='disabled', justify=tk.RIGHT)
        self.cardTotal.grid(row=7, column=3, pady=5, sticky="sw")

    def buttonbox(self):
        pass

    def generateReport(self):
        date = self.Edate.get_date()
        sales = Server().SvcSales.getSalesFrom(date)
        cashTotal = 0.00
        cardTotal = 0.00

        if len(sales) == 0:
            messagebox.showerror(parent=self, title="Error", message=f"No se encontraron ventas registradas en este periodo.\nRevise la fecha seleccionada.\n  Fecha: {date}")
            return

        for item in self.salesList.get_children():
            self.salesList.delete(item)

        for sale in sales:
            self.salesList.insert("", tk.END, sale.SaleId, values=(
                sale.Time,
                f"${sale.Total:.2f}",
                f"${sale.CashPayment:.2f}" if sale.CashPayment != 0 else "",
                f"${sale.CardPayment:.2f}" if sale.CardPayment != 0 else "",
            ))
            cashTotal += sale.CashPayment
            cardTotal += sale.CardPayment

        self.salesTotal.config(state="normal")
        self.salesTotal.delete(0, tk.END)
        self.salesTotal.insert(0, f"${cashTotal+cardTotal:.2f}")
        self.salesTotal.config(state="disabled")

        self.cashTotal.config(state="normal")
        self.cashTotal.delete(0, tk.END)
        self.cashTotal.insert(0, f"${cashTotal:.2f}")
        self.cashTotal.config(state="disabled")

        self.cardTotal.config(state="normal")
        self.cardTotal.delete(0, tk.END)
        self.cardTotal.insert(0, f"${cardTotal:.2f}")
        self.cardTotal.config(state="disabled")