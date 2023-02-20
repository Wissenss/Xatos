import sqlite3

try:
    from types import Product
    from errors import ErrorCode
except:
    from kernel.types import Product
    from kernel.errors import ErrorCode
    

class SvcProducts:
    def __init__(self, connection:sqlite3.Connection, cursor:sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor

    def setProduct(self, isCreate, product:Product):
        query = ""
        if isCreate:
            query = """
            INSERT INTO Products(Name, Description, Price, Code)
            VALUES (?, ?, ?, ?);
            """
            self.cursor.execute(query, (
                product.Name, 
                product.Description, 
                product.Price, 
                product.Code))
        else:
            query = """
            UPDATE Products 
            SET
                Name = ?,
                Description = ?,
                Price = ?,
                Code = ?
            WHERE
                ProductId = ?;
            """
            self.cursor.execute(query, (
                product.Name, 
                product.Description, 
                product.Price, 
                product.Code, 
                product.ProductId))

        self.connection.commit()

    def deleteProduct(self, ProductId):
        query = """
            DELETE FROM Products WHERE ProductId = ?;
        """

        self.cursor.execute(query, (ProductId,))
        self.connection.commit()

    def getProductFromId(self, ProductId)-> Product:
        query = """
            SELECT * FROM Products WHERE ProductId = ?;
        """

        self.cursor.execute(query, (ProductId,))
        result = self.cursor.fetchone()

        if not(result):
            return ErrorCode.ERR_PRODUCT_NOT_FOUND
        return Product(result)

    def getProductFromCode(self, ProductCode)-> Product:
        query = """
            SELECT * FROM Products WHERE Code = ?;
        """

        self.cursor.execute(query, (ProductCode,))
        result = self.cursor.fetchone()

        if not(result):
            return ErrorCode.ERR_PRODUCT_NOT_FOUND
        return Product(result)

    def getProducts(self)-> list[Product]:
        query = """
            SELECT * FROM Products WHERE true;
        """

        self.cursor.execute(query)

        products = [Product(dataSet) for dataSet in self.cursor.fetchall()]
        return products

if __name__ == "__main__":
    DATABASE_PATH = "../database.db"
    service = SvcProducts()