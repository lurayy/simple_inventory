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
    action : update,
    item_id
    name 
    category : 
    is_active : 
    description
    weight 
    sales_price
    average_cost_price
    barcode
    product_images : [{base64 : __base64__, category}, {base64 : __base64__, category},]    <-------- new images to be added
    remove_image : [__image_id__, image_id__]
}
```