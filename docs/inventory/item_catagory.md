#### 1. getItemCatagroies(data)
- call url: 'apiv1/inventory/items/catagroies'
- POST data format:
```
    {
        'action':'get',
        'start':0,
        'end':10,
    }
```
- Response data format:
```
    {
        status:true,
        ItemCatagroies: [
            ... ItemCatagroies_json
        ]
    }
```


#### 2. deleteItemCatagroies(data)
- call url: 'apiv1/inventory/items/catagories/delete'
- POST data format:
```
    {
        ItemCatagroys_id: [
            #ItemCatagroy_id,
            #ItemCatagroy_id,
            ...
        ]
    }
```

#### 3. createItemCatagroy(data)
- call url: 'apiv1/inventory/items/catagroy'
- POST data format:
```
    {
        action:add
        name: "klj"             
    }
```

#### 4. getItemCatagroy(data)
- call url: 'apiv1/inventory/ItemCatagroy'
- POST data format:
```
    {
        action:'get',
        ItemCatagroy_id:
    }
```


#### 5. updateItemCatagroy(data)
- call url: 'apiv1/inventory/items/catagroy'
- POST data format:
```
    {
        'action':'edit',
        is_active :True
        item_category_id: 1
        name: "klj"
    }
```