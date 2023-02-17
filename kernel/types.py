class Product:
    def __init__(self, dataSet):
        self.ProductId = dataSet[0]
        self.Name = dataSet[1]
        self.Description = dataSet[2]
        self.Price = dataSet[3]
        self.Code = dataSet[4]

class Sale:
    def __init__(self, dataset):
        self.SaleId = dataset[0]
        self.CreationDate = dataset[1]
        self.Total = dataset[2]
        self.CashPayment = dataset[3]
        self.CardPayment = dataset[4]

    def getDateAsDateTime(self):
        return 