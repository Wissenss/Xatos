import tkinter as tk
from tkinter import simpledialog

from kernel.server import Server
from kernel.types import Product

from constants import AccessMode

class ProductData(simpledialog.Dialog):
    def __init__(self, owner, accessMode, ProductId):
        self.Mode = accessMode
        self.Owner = owner
        self.ProductId = ProductId

        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("400x200")
        self.title("Datos del Producto")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Basket.ico")   

        container = tk.Frame(frame)
        container.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10, ipadx=5, ipady=5)

        # tk.Label(container, text="Id").grid(row=0, column=0, sticky="w")
        # self.EProductId = tk.Entry(container)
        # self.EProductId.grid(row=0, column=1)    

        tk.Label(container, text="Nombre").grid(row=1, column=0, sticky="w")
        self.ENombre = tk.Entry(container)
        self.ENombre.grid(row=1, column=1)

        tk.Label(container, text="Precio").grid(row=2, column=0, sticky="w")
        self.EPrecio = tk.Entry(container)
        self.EPrecio.grid(row=2, column=1)

        tk.Label(container, text="Código").grid(row=3, column=0, sticky="w")
        self.ECodigo = tk.Entry(container)
        self.ECodigo.grid(row=3, column=1)

        tk.Label(container, text="Descripción").grid(row=4, column=0, sticky="w")
        self.EDescripcion = tk.Entry(container)
        self.EDescripcion.grid(row=4, column=1)

        lowerBar = tk.Frame(frame)
        lowerBar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10), ipadx=5)
        if self.Mode != AccessMode.CREATE:
            self.LoadData()
        
        # self.EProductId.configure(state=tk.DISABLED)
        if self.Mode == AccessMode.READ:
            BCerrar = tk.Button(lowerBar, text="Cancelar", command=self.BCancelar)
            BCerrar.pack(side=tk.RIGHT)

            self.ENombre.configure(state=tk.DISABLED)
            self.EPrecio.configure(state=tk.DISABLED)
            self.ECodigo.configure(state=tk.DISABLED)
            self.EDescripcion.configure(state=tk.DISABLED)
        else:
            BCancelar = tk.Button(lowerBar, text="Cancelar", command=self.BCancelar)
            BCancelar.pack(side=tk.RIGHT)
            BAceptar = tk.Button(lowerBar, text="Aceptar", command=self.BAceptar)
            BAceptar.pack(side=tk.RIGHT) 

    def buttonbox(self):
        pass

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
            self.EDescripcion.get(),
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