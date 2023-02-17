import tkinter as tk
from tkinter import ttk, simpledialog

from kernel.server import Server
from kernel.types import Product

from constants import AccessMode

from componentes.currencyEntry import CurrencyEntry

class ProductData(simpledialog.Dialog):
    def __init__(self, owner, accessMode, ProductId):
        self.Mode = accessMode
        self.Owner = owner
        self.ProductId = ProductId

        super().__init__(parent=owner)

    def body(self, frame:tk.Frame):
        self.geometry("400x215")
        self.title("Datos del Producto")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Basket.ico")   
        frame.pack(expand=True, fill=tk.BOTH)

        frame.pack(side=tk.TOP, expand=True, padx=15, pady=(10, 0))  

        tk.Label(frame, text="Nombre").grid(row=1, column=0, sticky="w")
        self.ENombre = tk.Entry(frame)
        self.ENombre.grid(row=1, column=1, padx=(5, 15), pady=5, sticky="wesn")

        tk.Label(frame, text="Precio").grid(row=2, column=0, sticky="w")
        self.EPrecio = CurrencyEntry(frame, width=20)
        self.EPrecio.grid(row=2, column=1, padx=(5, 15), pady=5, sticky="w")

        tk.Label(frame, text="Código").grid(row=3, column=0, sticky="w")
        self.ECodigo = tk.Entry(frame)
        self.ECodigo.grid(row=3, column=1, padx=(5, 15), pady=5, sticky="wesn")

        tk.Label(frame, text="Descripción").grid(row=4, column=0, sticky="wn")

        self.EDescripcion = tk.Text(frame, height=4)
        self.EDescripcion.grid(row=4, column=1, padx=(5, 15), pady=(5, 0), sticky="wn")

        if self.Mode != AccessMode.CREATE:
            self.LoadData()

    def buttonbox(self):
        lowerBar = tk.Frame(self)
        lowerBar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10), ipadx=5)

        if self.Mode == AccessMode.READ:
            BCerrar = tk.Button(lowerBar, text="Cancelar", command=self.BCancelar)
            BCerrar.pack(side=tk.RIGHT, pady=5)

            self.ENombre.configure(state=tk.DISABLED)
            self.EPrecio.configure(state=tk.DISABLED)
            self.ECodigo.configure(state=tk.DISABLED)
            self.EDescripcion.configure(state=tk.DISABLED)
        else:
            pass
            BCancelar = ttk.Button(lowerBar, text="Cancelar", command=self.BCancelar)
            BCancelar.pack(side=tk.RIGHT, pady=5)
            BAceptar = ttk.Button(lowerBar, text="Aceptar", command=self.BAceptar)
            BAceptar.pack(side=tk.RIGHT, padx=5, pady=5) 

    def LoadData(self):
        product = Server().SvcProducts.getProductFromId(self.ProductId)
        self.ENombre.insert(0, product.Name)
        self.EDescripcion.insert(0, product.Description)
        self.EPrecio.insert(0, product.Price)
        self.ECodigo.insert(0, product.Code)

    def BAceptar(self):
        product = Product((
            self.ProductId,
            self.ENombre.get(),
            self.EDescripcion.get("1.0", tk.END),
            self.EPrecio.get(),
            self.ECodigo.get(),
        ))

        Server().SvcProducts.setProduct(
            self.Mode == AccessMode.CREATE,
            product
        )
            
        self.destroy()
        self.Owner.UpdateList()

    def BCancelar(self):
        self.destroy()