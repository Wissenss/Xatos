import sqlite3

DATABASE_PATH = "./database.db"

connection = sqlite3.Connection(DATABASE_PATH)
cursor = connection.cursor()

if __name__ == "__main__":

    cursor.execute("DROP TABLE Turns;")
    connection.commit()
    connection.close()