import sqlite3

DATABASE_PATH = ".\database.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

print("Creating table \"Configs\"...", end=" ")

try:
    cursor.execute("""
    CREATE TABLE Configs(
        ConfigId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(50),
        Value VARCHAR(250)
    );
    """)
    connection.commit()

    cursor.execute("""
    INSERT INTO Configs(
            Value,
            Name
        )
        VALUES(
            'Defaul Shop Name',
            'ShopName'
    );
    """)
    connection.commit()

    cursor.execute("""
    INSERT INTO Configs(
            Value,
            Name
        )
        VALUES(
            'Defaul Shop Address',
            'ShopAddress'
    );
    """)
    
    connection.commit()
    print("Success")
except:
    print("Fail")

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
        CreationTime VARCHAR(10), 
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