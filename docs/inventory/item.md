#### 1. getItems(data)
- call url: 'apiv1/inventory/items'
- POST data format:
```
    {
        action: get,
        start: 0,
        end: 10
    }
```
- Response data format:
```
    {
        status:true,
        items: [
            ... items_json
        ]
    }
```


#### 2. deleteItems(data)
- call url: 'apiv1/inventory/items/delete'
- POST data format:
```
    {
        items_id: [
            #item_id,
            #item_id,
            ...
        ]
    }
```

#### 3. createItem(data)
- call url: 'apiv1/inventory/items'
- POST data format:
```
    {
        name,
        sales_price
        category
        description
        weight
        average_cost_price
        barcode 
        product_image : [
            {
                base64 :
                category : THUMBNAIL/PRODUCT
            }
            ...
        ]
    }
```

#### 4. getItem(data)
- call url: 'apiv1/inventory/item'
- POST data format:
```
    {
        action:'get',
        item_id:
    }
```


#### 5. updateItem(data)
- call url: 'apiv1/inventory/item'
- POST data format:
```
    {
        'action':'edit',
        item_id: 1
        name: "klj"
        is_active:True,
        catagory: 1
    }
```

