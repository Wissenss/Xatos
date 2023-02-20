import datetime

class Product:
    def __init__(self, dataSet):
        self.ProductId = dataSet[0]
        self.Name = dataSet[1]
        self.Description = dataSet[2]
        self.Price = dataSet[3]
        self.Code = dataSet[4]

class Sale:
    def __init__(self, dataset=None):
        self.SaleId = None
        self._Date = None
        self._Time = None
        self.Total = None
        self.CashPayment = None
        self.CardPayment = None

        if dataset != None:
            self._setFromDataSet(dataset) 
    
    def _setFromDataSet(self, dataset):
        self.SaleId = dataset[0]
        self._Date = dataset[1]
        self._Time = dataset[2]
        self.Total = dataset[3]
        self.CashPayment = dataset[4]
        self.CardPayment = dataset[5]

    def getDataSet(self):
        return (
            self.SaleId,
            self._Date,
            self._Time,
            self.Total,
            self.CashPayment,
            self.CardPayment,
        )

    @property
    def Date(self):
        return datetime.datetime.strptime(self._Date, "%Y-%m-%d").date()
    
    def getDateAsStr(self)-> str:
        return self._Date

    @Date.setter
    def Date(self, dateIn):
        if isinstance(dateIn, str):
            self._Date = dateIn

        if isinstance(dateIn, datetime.date):
            self._Date = dateIn.strftime("%Y-%m-%d")

    @property
    def Time(self):
        return datetime.datetime.strptime(self._Time, "%H:%M:%S").time()
    
    def getTimeAsStr(self)-> str:
        return self._Time

    @Time.setter
    def Time(self, timeIn):
        if isinstance(timeIn, str):
            self._Time = timeIn

        if isinstance(timeIn, datetime.time):
            self._Time = timeIn.strftime("%H:%M:%S")