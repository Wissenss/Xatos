import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from componentes.navBar import NavBar

from kernel.server import Server
from kernel.types import Product

from WproductData import ProductData

from constants import AccessMode

class Configs(simpledialog.Dialog):
    def __init__(self, owner, mode):
        self.mode = mode
        super().__init__(parent=owner)

    def body(self, frame):
        self.title("Datos del Negocio")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Cog.ico")
        self.geometry("300x180")
        self.resizable(False, False)

        frame.pack(expand=True)

        tk.Label(frame, text="Nombre").grid(row=0, column=0, pady=5, padx=5)
        self.shopName = ttk.Entry(frame, width=30)
        self.shopName.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Dirección").grid(row=1, column=0, pady=5, padx=5)
        self.shopAddress = ttk.Entry(frame, width=30)
        self.shopAddress.grid(row=1, column=1, pady=5)

        self.loadData()

    def loadData(self):
        shopName = Server().SvcConfigs.getConfig("ShopName")
        self.shopName.delete(0, tk.END)
        self.shopName.insert(0, shopName)

        shopAddress = Server().SvcConfigs.getConfig("ShopAddress")
        self.shopAddress.delete(0, tk.END)
        self.shopAddress.insert(0, shopAddress)

    def buttonbox(self):
        buttonbox = tk.Frame(self)
        buttonbox.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5)
        ttk.Button(buttonbox, text="Cancelar", command=self.BCancelar).pack(side=tk.RIGHT)
        ttk.Button(buttonbox, text="Aceptar", command=self.BAceptar).pack(side=tk.RIGHT)
        
    def BAceptar(self):
        shopName = self.shopName.get()
        shopAddress = self.shopAddress.get()

        Server().SvcConfigs.setConfig(False, "ShopName", shopName)
        Server().SvcConfigs.setConfig(False, "ShopAddress", shopAddress)

        self.destroy()

    def BCancelar(self):
        self.destroy()