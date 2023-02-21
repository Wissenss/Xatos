import sqlite3
import datetime

class SvcTurns:
    def __init__(self, connection:sqlite3.Connection, cursor:sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor

    def isTurnOpen(self)-> bool:
        self.cursor.execute("""
        SELECT * FROM Turns WHERE IsOpen = TRUE;
        """)

        if self.cursor.fetchone():
            return True
        else:
            return False

    def openTurn(self, efectivoEnCaja:float):
        if self.isTurnOpen():
            raise AssertionError("Turn is already open")

        query = """
        INSERT INTO Turns(
            IsOpen,
            FechaInicio,
            HoraInicio,
            EfectivoInicio
        )
        VALUES(TRUE, ?, ?, ?);
        """

        date = datetime.datetime.today().date().strftime("%Y-%m-%d")
        time = datetime.datetime.now().time().strftime("%H:%M:%S")

        self.cursor.execute(query, (date, time, efectivoEnCaja))
        self.connection.commit()

    def closeTurn(self, efectivoEnCaja:float):
        if not(self.isTurnOpen()):
            raise AssertionError("No turn is open")

        cashCount = self.getCashCount()
        if cashCount != efectivoEnCaja:
            raise AssertionError("Incorrect amount of cash")

        date = datetime.datetime.today().date().strftime("%Y-%m-%d")
        time = datetime.datetime.now().time().strftime("%H:%M:%S")

        query = """
        UPDATE Turns SET
            IsOpen = FALSE,
            FechaFin = ?,
            HoraFin = ?,
            EfectivoFin = ?
        WHERE IsOpen = TRUE;
        """
        self.cursor.execute(query, (date, time, cashCount));
        self.connection.commit()

    def getCashCount(self):
        total = 0.00

        query = """
        SELECT *
        FROM Turns WHERE IsOpen = 1;
        """
        self.cursor.execute(query)
        values = self.cursor.fetchone()
        print(values)
        date = values[2]
        time = values[3]
        total += values[4]

        # date = datetime.datetime.today().date().strftime("%Y-%m-%d")
        # time = datetime.datetime.now().time().strftime("%H:%M:%S")

        query = """
        SELECT SUM(CashPayment) 
            FROM Sales
            WHERE date(CreationDate) >= date(?) AND time(CreationTime) >= time(?);
        """
        self.cursor.execute(query, (date, time,))
        result = self.cursor.fetchone()[0]
        total += result if result != None else 0.00

        return total;