import tkinter as tk
from tkinter import ttk, simpledialog

from kernel.server import Server

from datetime import datetime

class SalesReport(simpledialog.Dialog):
    def __init__(self, owner, mode):
        self.selectedDate = datetime.today()
        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("550x400")
        self.title("Reporte de Ventas")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Document-index.ico")

        frame.pack(expand=True, fill=tk.BOTH)

        leftPane = tk.Frame(frame)
        leftPane.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.datesList = ttk.Treeview(leftPane, columns=("Fecha"), show="headings", selectmode=tk.BROWSE)  
        self.datesList.heading("Fecha", text="Fecha")
        self.datesList.column("Fecha", anchor=tk.CENTER, width=100, stretch=False)
        self.datesList.pack(expand=True, fill=tk.Y)

        self.datesList.bind('<<TreeviewSelect>>', self.loadReport)

        self.updateDatesList()

        rightPane = tk.Frame(frame)
        rightPane.pack(side=tk.TOP, expand=True, padx=(10,0), pady=10)

        # tk.Label(rightPane, text="Fecha").grid(row=0, column=0, columnspan=2)

        tk.Label(rightPane, text="Ventas").grid(row=1, column=0, columnspan=2, sticky="sw")

        self.salesList = ttk.Treeview(rightPane, columns=("Hora", "MontoTotal", "PagoEnEfectivo", "PagoEnTarjeta"), show="headings")
        self.salesList.column("Hora", width=80)
        self.salesList.column("MontoTotal", width=80)
        self.salesList.column("PagoEnEfectivo", width=100)
        self.salesList.column("PagoEnTarjeta", width=100)
        self.salesList.heading("Hora", text="Hora")
        self.salesList.heading("MontoTotal", text="Monto")
        self.salesList.heading("PagoEnEfectivo", text="Pago en efectivo")
        self.salesList.heading("PagoEnTarjeta", text="Pago en tarjeta")

        self.salesList.grid(row=2, column=0, sticky="nswe")

    def buttonbox(self):
        pass

    def updateDatesList(self):
        for item in self.datesList.get_children():
            self.datesList.delete(item)
        
        sales = Server().SvcSales.getSalesSince("0001-01-01 00:00:00")
        lastdate = datetime.max.date()
        for sale in sales:
            currentdate = sale.Date
            if currentdate < lastdate:
                lastdate = currentdate
                formatDate = currentdate.strftime("%d de %m de %Y")
                self.datesList.insert("", tk.END, sale.Date, values=(formatDate,))

    def updateSalesList(self):
        for item in self.salesList.get_children():
            self.salesList.delete(item)

        date = datetime.strftime(self.selectedDate() )
        sales = Server().SvcSales.getSalesFrom(self.selectedDate)

    def loadReport(self, event):
        pass


