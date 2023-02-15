class Product:
    def __init__(self, dataSet):
        self.ProductId = dataSet[0]
        self.Name = dataSet[1]
        self.Description = dataSet[2]
        self.Price = dataSet[3]
        self.Code = dataSet[4]

class Sell:
    def __init__(self, dataset):
        self.SellId = dataset[0]
        self.Total = dataset[1]