import tkinter as tk
from tkinter import ttk, messagebox

from kernel.server import Server
from kernel.errors import ErrorCode
from kernel.types import Sell

from componentes.largeButton import LargeButton
from constants import AccessMode

from productsCatalog import ProductsCatalog
from payment import Payment

from showError import ShowError

class SellWindow(tk.Toplevel):
    def __init__(self, owner):
        super().__init__(owner)
        self.geometry("800x500")
        self.title("Punto de Venta")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Cash-stack.ico")

        self.Total = None

        self.leftPane = tk.Frame(self)
        self.leftPane.pack(side=tk.LEFT, fill=tk.BOTH, ipadx=10, ipady=10)

        ttk.Separator(self.leftPane, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        buttoncontrol = tk.Frame(self.leftPane)
        buttoncontrol.pack(expand=True)

        LargeButton(buttoncontrol, "Seleccionar", "./recursos/Fatcow-Farm-Fresh-Basket-remove.32.png", self.selectProduct).grid(row=0, column=0)

        ttk.Separator(buttoncontrol, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=4, sticky="nswe", padx=5)

        LargeButton(buttoncontrol, "Agregar", "./recursos/Fatcow-Farm-Fresh-Cart-add.32.png", self.addProduct).grid(row=2, column=0)
        LargeButton(buttoncontrol, "Eliminar", "./recursos/Fatcow-Farm-Fresh-Cart-delete.32.png", self.deleteProduct).grid(row=2, column=1)
        LargeButton(buttoncontrol, "Restar", "./recursos/Fatcow-Farm-Fresh-Shopping-cart-reset.32.png", self.restProduct).grid(row=2, column=2)
        LargeButton(buttoncontrol, "Generar Pago", "./recursos/Fatcow-Farm-Fresh-Coins-in-hand.32.png", self.generatePayment).grid(row=2, column=3, padx=10)

        bottomBar = tk.Frame(self.leftPane)
        bottomBar.pack(side=tk.TOP, fill=tk.X, pady=20)
        barlogo = LargeButton(bottomBar, "", "./recursos/Fatcow-Farm-Fresh-Barcode.32.png", self.BfocusBarCode)
        barlogo.pack(side=tk.LEFT)
        self.EBarCode = tk.Entry(bottomBar, font=("helvetica", 14))
        self.EBarCode.pack(expand=True, fill=tk.X)
        self.EBarCode.bind("<Return>", self.enterProduct)

        self.rightPane = tk.Frame(self)
        self.rightPane.pack(side=tk.RIGHT, fill=tk.BOTH, ipadx=10, ipady=10)
        self.list = ttk.Treeview(self.rightPane, columns=("Producto", "PrecioUnitario", "Cantidad", "SubTotal"), show="headings")
        self.list.heading("Producto", text="Producto")
        self.list.heading("PrecioUnitario", text="Precio Unitario")
        self.list.heading("Cantidad", text="Cantidad")
        self.list.heading("SubTotal", text="SubTotal")
        self.list.pack(expand=True, pady=10, padx=10, anchor="center", fill=tk.BOTH)

        pricePane = tk.Frame(self.rightPane)
        pricePane.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 24), padx=20)
        self.priceDisplay = tk.Label(pricePane, text="$0.00", font=("helvetica", 14))
        self.priceDisplay.pack(side=tk.RIGHT)
        tk.Label(pricePane, text="Total", font=("helvetica", 14)).pack(side=tk.RIGHT, padx=10)

    def generatePayment(self):
        if self.Total == None or self.Total <= 0:
            return

        sell = Sell((
            None,
            self.Total
        ))
        Payment(self, sell)

    def enterProduct(self, event):
        self.addProduct()
        self.EBarCode.delete(0, tk.END)

    def addProduct(self):
        code = self.EBarCode.get()
        print(code)
        if code == None or code == "":
            return
        result = Server().SvcProducts.getProductFromCode(code)

        if result == ErrorCode.ERR_PRODUCT_NOT_FOUND:
            ShowError(self, result, code)
            return
        product = result

        cantidad = 1
        try:
            self.list.insert("", tk.END, product.ProductId, values=(
                product.Name,
                product.Price,
                cantidad,
                product.Price * cantidad))
        except:
            iid = product.ProductId
            cantidad = self.list.item(iid)["values"][2] + 1
            # print(self.list.item(iid))

            self.list.item(iid, values=(
                product.Name,
                product.Price,
                cantidad,
                product.Price * cantidad
            ))

        self.updatePrice()

    def updatePrice(self):
        total = 0
        for iid in self.list.get_children():
            total += float(self.list.item(iid)["values"][3])

        self.priceDisplay.config(text=f"${total:.2f}")
        self.Total = total

    def deleteProduct(self):
        iid = self.list.focus()
        if iid == "":
            return

        self.list.delete(iid)

        self.updatePrice()

    def restProduct(self):
        iid = self.list.focus()
        if iid == "":
            return

        row = self.list.item(iid)["values"]
        name = row[0]
        price = float(row[1])
        cantidad = float(row[2]) - 1

        self.list.item(iid, values=(
            name,
            price,
            float(cantidad),
            price * cantidad
        ))

        self.updatePrice()

        if cantidad <= 0:
            self.list.delete(iid)

    def selectProduct(self):
        catalog = ProductsCatalog(self, AccessMode.SELECT)
        code = catalog.selectedCode
        if code != None:
            self.EBarCode.delete(0, tk.END)
            self.EBarCode.insert(0, str(code))

    def BfocusBarCode(self):
        self.EBarCode.delete(0, tk.END)
        self.EBarCode.focus()