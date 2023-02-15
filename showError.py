import tkinter as tk
from tkinter import messagebox
from kernel.errors import ErrorCode

class ShowError():
    def __init__(self, owner, Error, Data=None):
        message = self.translateError(Error, Data)
        messagebox.showerror(parent=owner, title="Error", message=message, icon="error")

    def translateError(self, Error, Data):
        if Error == ErrorCode.ERR_PRODUCT_NOT_FOUND:
            return f"No se encontro el producto en la base de datos. \nCódigo: {Data}"
        else:
            return f"Error no registrado"