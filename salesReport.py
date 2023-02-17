import tkinter as tk
from tkinter import ttk, simpledialog

from kernel.server import Server

from datetime import datetime

class SalesReport(simpledialog.Dialog):
    def __init__(self, owner, mode):
        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("400x400")
        self.title("Reporte de Ventas")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Document-index.ico")

        frame.pack(expand=True, fill=tk.BOTH)

        leftPane = tk.Frame(frame)
        leftPane.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.datesList = ttk.Treeview(leftPane, columns=("Fecha"), show="headings", selectmode=tk.BROWSE)  
        self.datesList.heading("Fecha", text="Fecha")
        self.datesList.column("Fecha", anchor=tk.CENTER, width=10)
        self.datesList.pack(expand=True, fill=tk.BOTH)

        self.datesList.bind('<<TreeviewSelect>>', self.loadReport)

        self.updateDatesList()

        rightPane = tk.Frame(frame)
        rightPane.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)



    def updateDatesList(self):
        for item in self.datesList.get_children():
            self.datesList.delete(item)
        
        sales = Server().SvcSales.getSalesSince("0001-01-01 00:00:00")
        lastdate = datetime.min.date()
        for sale in sales:
            currentdate = datetime.strptime(sale.CreationDate, "%Y-%m-%d %H:%M:%S").date()
            print(currentdate)
            if currentdate > lastdate:
                lastdate = currentdate
                dateTime = datetime.strptime(sale.CreationDate, "%Y-%m-%d %H:%M:%S")
                formatDate = dateTime.strftime("%d de %m de %Y")
                self.datesList.insert("", tk.END, sale.CreationDate, values=(formatDate,))

    def loadReport(self, event):
        pass

    def buttonbox(self):
        pass