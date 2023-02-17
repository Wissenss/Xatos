import sqlite3

try:
    from types import Sale
    from errors import ErrorCode
except:
    from kernel.types import Sale
    from kernel.errors import ErrorCode
    

class SvcSales:
    def __init__(self, connection:sqlite3.Connection, cursor:sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor

    def setSale(self, isCreate, sale:Sale):
        query = ""
        if isCreate:
            query = """
            INSERT INTO Sales(CreationDate, Total, CashPayment, CardPayment)
            VALUES (?, ?, ?, ?);
            """
            self.cursor.execute(query, (
                sale.CreationDate,
                sale.Total,
                sale.CashPayment,
                sale.CardPayment
            ))
        else:
            print("Not implemented yet")

        self.connection.commit()

    def deleteSale(self, SaleId):
        query = """
            DELETE FROM Sales WHERE SaleId = ?;
        """

        self.cursor.execute(query, (SaleId,))
        self.connection.commit()

    def getSalesFrom(self, date):
        query = """
            SELECT * FROM Sales WHERE CreationDate = ?; 
        """

        self.cursor.execute(query, (date,))
        sales = [Sale(dataSet) for dataSet in self.cursor.fetchall()]
        return sales

    def getSalesSince(self, since):
        query = """
            SELECT * FROM Sales WHERE datetime(CreationDate) >= datetime(?) ORDER BY CreationDate;
        """

        self.cursor.execute(query, (since,))

        sales = [Sale(dataSet) for dataSet in self.cursor.fetchall()]
        return sales

    def deleteSales(self, date):
        query = """
            DELETE * FROM Sales WHERE DateTime(CreationDate) = DateTime(?);
        """

        self.cursor.execute(query, (date,))
        self.connection.commit()