import sqlite3
try:
    from svcProducts import SvcProducts
except:
    from kernel.svcProducts import SvcProducts

DATABASE_PATH = "./database.db"

class Server:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.connection = sqlite3.connect(DATABASE_PATH)
            cls.cursor = cls.connection.cursor()
            
            cls.SvcProducts = SvcProducts(cls.connection, cls.cursor)

            cls.instance = super(Server, cls).__new__(cls)
        return cls.instance