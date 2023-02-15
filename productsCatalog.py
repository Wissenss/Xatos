import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from componentes.navBar import NavBar

from kernel.server import Server
from kernel.types import Product

from productData import ProductData

from constants import AccessMode

class ProductsCatalog(simpledialog.Dialog):
    def __init__(self, owner, mode):
        self.mode = mode
        self.selectedCode = None
        super().__init__(parent=owner)

    def body(self, frame):
        self.geometry("400x300")
        self.title("Catálogo de Productos")
        self.iconbitmap(default="./recursos/Fatcow-Farm-Fresh-Basket.ico")
        content = {
            "": [
                ("Agregar", "./recursos/Fatcow-Farm-Fresh-Basket-add.32.png", self.BAgregar),
                ("Editar", "./recursos/Fatcow-Farm-Fresh-Basket-edit.32.png", self.BEditar),
                ("Consultar", "./recursos/Fatcow-Farm-Fresh-Basket-full.32.png", self.BConsultar),
                ("Eliminar", "./recursos/Fatcow-Farm-Fresh-Basket-delete.32.png", self.BEliminar)
            ],
            "Salir": [
                ("Salir", "./recursos/Fatcow-Farm-Fresh-Door.32.png", self.BSalir)
            ]
        }

        if self.mode == AccessMode.SELECT:
            content [""] =[("Seleccionar", "./recursos/Fatcow-Farm-Fresh-Basket-put.32.png", self.BSeleccionar)]

        bar = NavBar(frame, content, False)
        bar.render()
        bar.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.list = ttk.Treeview(frame, columns=("Nombre", "Codigo"), show="headings")
        self.list.heading("Nombre", text="Nombre")
        self.list.heading("Codigo", text="Código")
        self.list.pack(fill=tk.BOTH,  anchor=tk.CENTER, side=tk.BOTTOM, pady=(0, 10), padx=10,)
        self.UpdateList()

    
    def buttonbox(self):pass #this line prevents the acept and cancel buttons from being render
        # tk.Frame(self, height=0)
    #Actions
    def BAgregar(self):
        ProductData(self, AccessMode.CREATE, None)

    def BConsultar(self):
        if self.list.focus() != "":
            ProductData(self, AccessMode.READ, self.list.focus())

    def BEditar(self):
        if self.list.focus() != "":
            ProductData(self, AccessMode.UPDATE, self.list.focus())
        
    def BEliminar(self):
        iid = self.list.focus()
        if iid==None:
            return

        values = self.list.item(iid)["values"]
        if not(messagebox.askokcancel(title="", message=f"Esta seguro de que desea eliminar el producto seleccionado? Esta accion no se puede deshacer\nNombre: {values[0]}\nCódigo: {values[1]}")):
            return

        Server().SvcProducts.deleteProduct(self.list.focus())
        self.UpdateList()

    def BSalir(self):
        return None, self.destroy()

    def BSeleccionar(self):
        iid = self.list.focus()
        
        if iid !="":
            code = self.list.item(iid)["values"][1]
            self.selectedCode = code
            return self.destroy()

    #-----------------------------
    def UpdateList(self):
        self.list.delete(*self.list.get_children())

        products = Server().SvcProducts.getProducts()
        index = 0
        for product in products:
            iid = product.ProductId
            self.list.insert("", tk.END, iid, values=(product.Name, product.Code))
            index = iid = index + 1