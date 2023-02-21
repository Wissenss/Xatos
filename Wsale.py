import os
import tkinter as tk
from tkinter import ttk, messagebox

from kernel.server import Server
from kernel.errors import ErrorCode
from kernel.types import Sale

from renderizador.renderer import render_ticket

from componentes.largeButton import LargeButton
from constants import AccessMode

from WproductsCatalog import ProductsCatalog
from Wpayment import Payment

from WshowError import ShowError

class SaleWindow(tk.Toplevel):
    def __init__(self, owner):
        super().__init__(owner)
        self.geometry("800x500")
        self.minsize(800, 500)
        self.title("Punto de Venta")
        self.iconbitmap("./recursos/Fatcow-Farm-Fresh-Cash-stack.ico")

        self.Total = None

        self.leftPane = tk.Frame(self)
        self.leftPane.pack(side=tk.LEFT, fill=tk.BOTH, ipadx=10, ipady=10)

        ttk.Separator(self.leftPane, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0), pady=5)

        buttoncontrol = tk.Frame(self.leftPane)
        buttoncontrol.pack(expand=True)

        LargeButton(buttoncontrol, "Seleccionar", "./recursos/Fatcow-Farm-Fresh-Basket-put.32.png", self.selectProduct).grid(row=0, column=0)
        LargeButton(buttoncontrol, "Cancelar", "./recursos/Fatcow-Farm-Fresh-Bin-empty.32.png", self.cancelSell).grid(row=0, column=3)

        ttk.Separator(buttoncontrol, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=4, sticky="nswe", padx=5)

        LargeButton(buttoncontrol, "Agregar", "./recursos/Fatcow-Farm-Fresh-Cart-add.32.png", self.addProduct).grid(row=2, column=0)
        LargeButton(buttoncontrol, "Eliminar", "./recursos/Fatcow-Farm-Fresh-Cart-delete.32.png", self.deleteProduct).grid(row=2, column=1)
        LargeButton(buttoncontrol, "Restar", "./recursos/Fatcow-Farm-Fresh-Shopping-cart-reset.32.png", self.restProduct).grid(row=2, column=2)
        LargeButton(buttoncontrol, "Pago (F5)", "./recursos/Fatcow-Farm-Fresh-Coins-in-hand.32.png", self.generatePayment).grid(row=2, column=3, padx=10)

        bottomBar = tk.Frame(self.leftPane)
        bottomBar.pack(side=tk.TOP, fill=tk.X, pady=20)
        barlogo = LargeButton(bottomBar, "", "./recursos/Fatcow-Farm-Fresh-Barcode.32.png", self.BfocusBarCode)
        barlogo.pack(side=tk.LEFT)
        self.EBarCode = tk.Entry(bottomBar, font=("helvetica", 14))
        self.EBarCode.pack(expand=True, fill=tk.X)
        self.EBarCode.bind("<Return>", self.enterProduct)

        self.rightPane = tk.Frame(self)
        self.rightPane.pack(side=tk.RIGHT, fill=tk.BOTH, ipadx=0, ipady=10, expand=True)

        #list 
        style = ttk.Style()
        style.configure("SellList.Treeview.Heading", font=(None, 12))

        self.list = ttk.Treeview(self.rightPane, columns=("Producto", "PrecioUnitario", "Cantidad", "SubTotal"), show="headings", style="SellList.Treeview", selectmode=tk.BROWSE)
        self.list.heading("Producto", text="Producto")
        self.list.heading("PrecioUnitario", text="Precio Unitario")
        self.list.heading("Cantidad", text="Cantidad")
        self.list.heading("SubTotal", text="SubTotal")

        self.list.column("Producto", anchor=tk.W, width=10)
        self.list.column("PrecioUnitario", anchor=tk.CENTER, width=10)
        self.list.column("Cantidad", anchor=tk.CENTER, width=10)
        self.list.column("SubTotal", anchor=tk.E, width=10)

        self.list.tag_configure('font', font=(None, 12))
        self.list.tag_configure('odd', background="#dedede")

        self.list.pack(expand=True, pady=10, padx=10, anchor="center", fill=tk.BOTH)

        pricePane = tk.Frame(self.rightPane)
        pricePane.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 24), padx=20)
        self.priceDisplay = tk.Label(pricePane, text="$0.00", font=("helvetica", 14))
        self.priceDisplay.pack(side=tk.RIGHT)
        tk.Label(pricePane, text="Total", font=("helvetica", 14)).pack(side=tk.RIGHT, padx=10)

        #shortcuts
        self.bind("<F5>", self.F5shortCut)

        self.BfocusBarCode()

    def F5shortCut(self, event):
        self.generatePayment()

    def generatePayment(self):
        if self.Total == None or self.Total <= 0:
            return
        
        Payment(self, self.Total)

    def enterProduct(self, event):
        self.addProduct()
        self.EBarCode.delete(0, tk.END)

    def renderTags(self):
        for index, item in enumerate(self.list.get_children()):
            tags = ()
            if index%2==0:
                tags = ('font', 'odd')
            else:
                tags = ('font')
            
            self.list.item(item, tags=tags)

    def addProduct(self):
        code = self.EBarCode.get()
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
                f"${product.Price:.2f}",
                cantidad,
                f"${product.Price * cantidad:.2f}"
            ))
        except:
            iid = product.ProductId
            cantidad = self.list.item(iid)["values"][2] + 1
            # print(self.list.item(iid))

            self.list.item(iid, values=(
                product.Name,
                f"${product.Price:.2f}",
                cantidad,
                f"${product.Price * cantidad:.2f}"
            ))

        self.renderTags()
        self.updatePrice()

    def updatePrice(self):
        total = 0
        for iid in self.list.get_children():
            stringNum = self.list.item(iid)["values"][3].replace("$", "")
            total += float(stringNum)

        self.priceDisplay.config(text=f"${total:.2f}")
        self.Total = total

    def deleteProduct(self):
        iid = self.list.focus()
        if iid == "":
            return

        self.list.delete(iid)

        self.renderTags()
        self.updatePrice()

    def restProduct(self):
        iid = self.list.focus()
        if iid == "":
            return

        row = self.list.item(iid)["values"]
        name = row[0]
        price = float(row[1].replace("$", ""))
        cantidad = int(row[2]) - 1

        self.list.item(iid, values=(
            name,
            f"${price:.2f}",
            cantidad,
            f"${price * cantidad:.2f}"
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

    def clearData(self):
        for item in self.list.get_children():
            self.list.delete(item)

        self.updatePrice()
        self.BfocusBarCode()

    def cancelSell(self):
        if not(messagebox.askokcancel(parent=self, title="Cancelar Venta", message=f"Esta accion borrará todos los productos marcados\nDesea continuar?")):
            return
        self.clearData()

    def generateTicket(self):
        class Row:
            def __init__(self):
                self.Name = None
                self.UnitPrice = None
                self.Amount = None
                self.SubTotal = None

        items = []
        children = self.list.get_children()
        for child in children:
            row = Row()
            values = self.list.item(child)["values"]

            row.Name = values[0]
            row.UnitPrice = values[1]
            row.Amount = values[2]
            row.SubTotal = values[3]

            items.append(row)

        total = self.priceDisplay.cget("text")

        name = Server().SvcConfigs.getConfig("ShopName")
        address = Server().SvcConfigs.getConfig("ShopAddress")

        render_ticket(name, address, items, total)
        os.startfile("out.pdf", "print")