#### Note : There is no getInvoiceItem since, you will get all the data related to the Invoice order while quering for the particular Invoice order. 


#### 1. deleteInvoiceItems(data)
- call url: 'apiv1/inventory/invoiceitem/delete'
- POST data format:
```
    {
        pucrhase_items_id: [
            #invoice_item_id,
            #invoice_tem_id,
            ...
        ]
    }
```

#### 3. createInvoiceItem(data)
- call url: 'apiv1/inventory/invoiceitems'
- POST data format:
```
    {
        'action':'add',
        'item': 1,
        'purchase_item':5,
        'sold_from':2,
        'invoice':3,
        'quantity':3,
        'price':34234,
        'tax_total':55,
        'discount_type':'fixed',
        'discount':1351,
        'sub_total':54,
        'total':234
    }
```

#### 5. updatePucrhaseItem(data)
- call url: 'apiv1/inventory/invoiceitem'
- POST data format:
```{
        'invoice_item_id':2
        'action':'edit',
        'item': 1,
        'purchase_item':5,
        'sold_from':2,
        'invoice':3,
        'quantity':3,
        'price':34234,
        'tax_total':55,
        'discount_type':'fixed',
        'discount':1351,
        'sub_total':54,
        'total':234
    }
```

