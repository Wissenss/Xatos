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
        self.geometry("200x200")

        frame.pack(expand=True)

        tk.Label(frame, text="Nombre").grid(row=0, column=0, pady=5)
        self.shopName = ttk.Entry(frame)
        self.shopName.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Dirección").grid(row=1, column=0, pady=5)
        self.shopAddress = ttk.Entry(frame)
        self.shopAddress.grid(row=1, column=1, pady=5)

    def buttonbox(self):
        ttk.Button(self, text="Aceptar", command=self.BAceptar).pack(side=tk.BOTTOM, anchor="e")
        ttk.Button(self, text="Cancelar", command=self.BCancelar).pack(side=tk.BOTTOM, anchor="e")

    def BAceptar(self):
        shopName = self.shopName.get()
        shopAddress = self.shopAddress.get()

        Server().SvcConfigs.setConfig(False, "ShopName", shopName)
        Server().SvcConfigs.setConfig(False, "ShopAddress", shopAddress)

        self.destroy()

    def BCancelar(self):
        self.destroy()