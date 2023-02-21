import tkinter as tk
from tkinter import messagebox
from componentes.navBar import NavBar
from componentes.largeButton import LargeButton

from kernel.server import Server

from WproductsCatalog import ProductsCatalog 
from Wsale import SaleWindow
from WsalesReport import SalesReport
from Wconfig import Configs
from WTurnStart import TurnStart
from WTurnEnd import TurnEnd

from constants import AccessMode

class TabGeneral(tk.Frame):
    def __init__(self, owner: tk.Tk):
        super().__init__(owner)

        self.DVenta = None

        topBar = tk.Frame(self)
        topBar.pack(side=tk.TOP, fill=tk.X)

        content = {
            "":[
                ("Venta", "./recursos/Fatcow-Farm-Fresh-Cash-stack.32.png", self.BVentaClick),
                ("Productos", "./recursos/Fatcow-Farm-Fresh-Basket.32.png", self.BProductosClick)
            ],
            "Reportes":[
                ("Reporte", "./recursos/Fatcow-Farm-Fresh-Document-index.32.png", self.BInformeVentas)
            ],
            "Turnos":[
                ("Iniciar Turno", "./recursos/Fatcow-Farm-Fresh-Clock-play.32.png", self.BIniciarTurno),
                ("Terminar Turno", "./recursos/Fatcow-Farm-Fresh-Clock-stop.32.png", self.BTerminarTurno),
            ],
        }
        self.bar = NavBar(topBar, content, False)
        self.bar.render()
        self.bar.pack(side=tk.LEFT, expand=False, padx=5, pady=5)

        bconfig = LargeButton(topBar, "Configuración", "./recursos/Fatcow-Farm-Fresh-Cog.32.png", self.BConfiguracion)
        bconfig.pack(side=tk.RIGHT, padx=5, pady=5)

    def BVentaClick(self):
        if not(Server().SvcTurns.isTurnOpen()):
            messagebox.showerror(parent=self, title="Error", message="No existe un turno abierto. Debe iniciar uno nuevo.")
            return

        #known bug

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

    def BConfiguracion(self):
        Configs(self, AccessMode.UPDATE)

    def BIniciarTurno(self):
        if Server().SvcTurns.isTurnOpen():
            messagebox.showerror(parent=self, title="Error", message="Ya existe un turno abierto. Cierre el turno actual antes de iniciar uno nuevo.")
            return
        TurnStart(self)
       
    def BTerminarTurno(self):
        if not(Server().SvcTurns.isTurnOpen()):
            messagebox.showerror(parent=self, title="Error", message="No existe un turno abierto. Debe iniciar uno nuevo.")
            return
        TurnEnd(self)

    #Handlers
    def DVentaClosing(self):
        self.DVenta.destroy()
        self.DVenta = None