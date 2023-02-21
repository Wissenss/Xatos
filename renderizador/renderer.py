import os
import pdfkit
from pdfkit import from_string
from jinja2 import Environment, PackageLoader, FileSystemLoader
from datetime import datetime

config = None
env = None
OUTPUT_PATH = "out.pdf"
if __name__ != "__main__":
    config = pdfkit.configuration(wkhtmltopdf="./renderizador/wkhtmltox/bin/wkhtmltopdf.exe")
    env = Environment(loader=PackageLoader("renderizador"), autoescape=True)
else:
    config = pdfkit.configuration(wkhtmltopdf="./wkhtmltox/bin/wkhtmltopdf.exe")
    env = Environment(loader=FileSystemLoader("./templates/"),)

def render_ticket(**vars):
    template = env.get_template("ticket.html")
    fecha = datetime.today().date().strftime("%d / %m / %Y")
    hora = datetime.today().time().strftime("%H : %M")

    vars["date"] = fecha
    vars["time"] = hora

    html = template.render(**vars)

    #si se corre renderer.py directo se guarda el html previo al render
    if __name__ == "__main__":
        with open("my_new_file.html", "w") as fh:
            fh.write(html)

    file = from_string(html, OUTPUT_PATH, configuration=config)

def print_pdf():
    os.startfile("./renderizador/out.pdf", "print")

if __name__ == "__main__":
    #aca pueden ir test para probar los templates
    #con una lista de prueba etc...
    class Row:
        def __init__(self, name, unitprice, amount, subtotal):
            self.Name = name
            self.UnitPrice = unitprice
            self.Amount = amount
            self.SubTotal = subtotal

    items = []
    items.append(Row("Galletas", "$12", "5", "$60"))
    items.append(Row("Agua", "$10", "2", "$20"))
    items.append(Row("Tequila", "$180", "1", "$180"))
    items.append(Row("Bateria AA", "$90", "1", "$90"))

    vars = {
        "items" : items,
        "total" : 350.00,
        "name" : "Test Page",
        "address" : "Some random address",
        "payment" : 400.00,
        "change" : 50.00
    }

    render_ticket(**vars)