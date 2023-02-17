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
        Real Total
    }
```