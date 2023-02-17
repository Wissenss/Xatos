import sqlite3

DATABASE_PATH = "..\database.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

print("Creating table \"Products\"...", end=" ")

try:
    cursor.execute("""
    CREATE TABLE Products(
        ProductId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(50),
        Description VARCHAR(250),
        Price REAL,
        Code VARCHAR(100)
    );
    """)
    connection.commit()
    print("Success")
except:
    print("Fail")

print("Creating table \"Sales\"...", end=" ")

try:
    #CreationDate format YYYY-MM-DD HH:MM:SS.SSS
    cursor.execute("""
    CREATE TABLE Sales(
        SaleId INTEGER PRIMARY KEY AUTOINCREMENT,
        CreationDate VARCHAR(10), 
        Total REAL,
        CashPayment REAL,
        CardPayment REAL
    );
    """)
    connection.commit()
    print("Success")
except:
    print("Fail")

connection.close()