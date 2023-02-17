import sqlite3
try:
    from svcProducts import SvcProducts
    from svcSales import SvcSales
except:
    from kernel.svcProducts import SvcProducts
    from kernel.svcSales import SvcSales

DATABASE_PATH = "./database.db"

class Server:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.connection = sqlite3.connect(DATABASE_PATH)
            cls.cursor = cls.connection.cursor()
            
            cls.SvcProducts = SvcProducts(cls.connection, cls.cursor)
            cls.SvcSales = SvcSales(cls.connection, cls.cursor)

            cls.instance = super(Server, cls).__new__(cls)
        return cls.instance