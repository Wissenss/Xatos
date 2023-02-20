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

def render_ticket(shopName, shopAddress, items, total):
    template = env.get_template("ticket.html")
    fecha = datetime.today().date().strftime("%d / %m / %Y")
    hora = datetime.today().time().strftime("%H : %M")

    html = template.render(name=shopName, address=shopAddress, items=items, date=fecha, time=hora, total=total)

    # with open("my_new_file.html", "w") as fh:
    #     fh.write(html)

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

    render_ticket(items)