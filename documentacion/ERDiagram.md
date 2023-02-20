```mermaid
erDiagram
    Products{
        Int ProductId
        String Name
        String Description
        Rel Price
        String Code
    }

    Sales{
        Int SaleId
        Text CreationDate
        Text CreationTime
        Real Total
        Real CashPayment
        Real CardPayment
    }

    Configs{
        Int ConfigId
        Text Name
        Text Value
    }
```