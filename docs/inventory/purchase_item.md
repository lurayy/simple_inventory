#### Note : There is no getPurchaseItem since, you will get all the data related to the purchase order while quering for the particular purchase order. 


#### 1. deletePucrhaseItems(data)
- call url: 'apiv1/inventory/pitems/delete'
- POST data format:
```
    {
        pucrhase_items_id: [
            #PucrhaseItem_id,
            #PucrhaseItem_id,
            ...
        ]
    }
```

#### 3. createPucrhaseItem(data)
- call url: 'apiv1/inventory/pitems'
- POST data format:
```
    {
        'action':'edit',
        'item': 1,
        'purchase_order':5,
        'quantity':3,
        'non_discount_price': 234,
        'purchase_price':34234,
        'defective':55,
        'discount_type':'fixed',                # discount can be fixed or percent
        'discount':1351,
        'status':'addedtocirculation',          # status can be 'addedtocirculation'/'delivered'/'incomplete'
    }
```

#### 5. updatePucrhaseItem(data)
- call url: 'apiv1/inventory/pitem'
- POST data format:
```
    {
        'action':'edit',
        'item': 1,
        'purchase_order':5,
        'quantity':3,
        'non_discount_price': 234,
        'purchase_price':34234,
        'defective':55,
        'discount_type':'fixed',                # discount can be fixed or percent
        'discount':1351,
        'status':'addedtocirculation',          # status can be 'addedtocirculation'/'delivered'/'incomplete'
    }
```

