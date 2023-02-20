import sqlite3
import datetime

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
            INSERT INTO Sales(
                CreationDate,
                CreationTime, 
                Total, 
                CashPayment, 
                CardPayment)
            VALUES (?, ?, ?, ?, ?);
            """
            self.cursor.execute(query, (
                sale.getDateAsStr(),
                sale.getTimeAsStr(),
                sale.Total,
                sale.CashPayment,
                sale.CardPayment
            ))
        else:
            #this probably wont need to be implemented
            print("Not implemented yet")

        self.connection.commit()

    def deleteSale(self, SaleId):
        query = """
            DELETE FROM Sales WHERE SaleId = ?;
        """

        self.cursor.execute(query, (SaleId,))
        self.connection.commit()

    def getSalesFrom(self, date)-> list[Sale]:
        query = """
            SELECT * FROM Sales WHERE CreationDate = ?; 
        """

        self.cursor.execute(query, (date,))
        sales = [Sale(dataSet) for dataSet in self.cursor.fetchall()]
        return sales

    def getSalesSince(self, since)-> list[Sale]:
        if isinstance(since, str):
            pass
        elif isinstance(since, datetime.date):
            since = datetime.date.strftime(since, "%H:%M:%S")
        else:
            raise f"invalid input: {since}"

        query = """
            SELECT * FROM Sales WHERE date(CreationDate) >= date(?) ORDER BY CreationDate DESC;
        """

        self.cursor.execute(query, (since,))

        sales = [Sale(dataSet) for dataSet in self.cursor.fetchall()]
        return sales

    def deleteSales(self, date):
        if isinstance(date, str):
            pass
        elif isinstance(date, datetime.date):
            date = datetime.date.strftime(date, "%H:%M:%S")
        else:
            raise f"invalid input: {date}"

        query = """
            DELETE * FROM Sales WHERE date(CreationDate) = date(?);
        """

        self.cursor.execute(query, (date,))
        self.connection.commit()