import sqlite3

try:
    from types import Product
    from errors import ErrorCode
except:
    from kernel.types import Product
    from kernel.errors import ErrorCode
    

class SvcConfigs:
    def __init__(self, connection:sqlite3.Connection, cursor:sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor

    def setConfig(self, isCreate, configName, value):
        query = ""
        if isCreate:
            query = """
            INSERT INTO Configs(
                Value,
                Name
            )
            VALUES (?, ?);
            """
        else:
            query = """
            UPDATE Configs
            SET
                Value = ?
            WHERE
                Name = ?; 
            """

        self.cursor.execute(query, (value, configName))
        self.connection.commit()

    def getConfig(self, configName):
        query = """
        SELECT value FROM Configs WHERE Name = ?;
        """

        self.cursor.execute(query, (configName,))
        return self.cursor.fetchone()[0]