import tkinter as tk
from componentes.navBar import NavBar
from componentes.largeButton import LargeButton
from kernel.server import Server

from productsCatalog import ProductsCatalog 
from saleWindow import SaleWindow
from salesReport import SalesReport
from constants import AccessMode

class GeneralTab(tk.Frame):
    def __init__(self, owner: tk.Tk):
        # self.owner = owner
        super().__init__(owner)
        content = {
            "":[
                ("Venta", "./recursos/Fatcow-Farm-Fresh-Cash-stack.32.png", self.BVentaClick),
                ("Productos", "./recursos/Fatcow-Farm-Fresh-Basket.32.png", self.BProductosClick)
            ],
            "Reportes":[
                ("Reporte", "./recursos/Fatcow-Farm-Fresh-Document-index.32.png", self.BInformeVentas)
            ]
        }
        bar = NavBar(self, content, False)
        bar.render()
        bar.pack(side=tk.TOP, fill=tk.X, expand=False, padx=5, pady=5)

        self.DVenta = None
        

    def BVentaClick(self):
        if self.DVenta == None:   
            self.DVenta = SaleWindow(self)
            self.DVenta.protocol("WM_DELETE_WINDOW", self.DVentaClosing)
        else:
            self.DVenta.focus_force()
            self.DVenta.BfocusBarCode()

    def BProductosClick(self):
        ProductsCatalog(self, AccessMode.UPDATE)

    def BInformeVentas(self):
        SalesReport(self, AccessMode.UPDATE)

    #Handlers
    def DVentaClosing(self):
        self.DVenta.destroy()
        self.DVenta = None