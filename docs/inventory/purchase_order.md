#### 1. getPurchaseOrders(data)
- call url: 'apiv1/inventory/PurchaseOrders'
- POST data format:

    a. filter: none
    ```
        {
            'action':'get',
            'start':0,
            'end':20,
            'filter':'none'
        }
    ```

    b. filter by date :
    ```
        {
            "action":"get",
            "start":0,
            "end":5,
            "filter":"date",
            "start_date": "2020-02-06T11:03:03",
            "end_date": "2020-03-06T11:05:03"
        }
    ```

    c. filter by vendor :
    ```
        {
            "action":"get",
            "start":0,
            "end":5,
            "filter":"vendor",
            "vendor":1
        }
    ```

    d. filter by status: 
    ```
        {
            "action":"get",
            "start":0,
            "end":5,
            "filter":"status",
            "status":"sent"
            "status_id":1
        }
    ```
    
    e. filter by multiple:
    ```
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'multiple',
        'status':'draft',
        'vendor_id':1,
        ...... 
        # This filter is incomplete. Need more work after colaborating with front end
    }
    ```

- Response data format:
```
    {
        status:true,
        PurchaseOrders: [
            ... PurchaseOrders_json
        ]
    }
```


#### 2. deletePurchaseOrders(data)
- call url: 'apiv1/inventory/porders/delete'
- POST data format:
```
    {
        purchase_orders_id: [
            #PurchaseOrder_id,
            #PurchaseOrder_id,
            ...
        ]
    }
```


#### 3. createPurchaseOrder(data)
- call url: 'apiv1/inventory/porders'
- POST data format:
```
    {
        'action':'add',
        'id':1,
        'invoiced_on': "2019-11-16T08:15:00.000",
        'completed_on: "2019-11-16T08:15:00.000",
        'total_cost': 2500,
        'discount_type': 'fixed',    <- can be fixed or percent
        'discount': 25,
        'added_by':1,                <- added_by id
        'vendor':1,                  <- vendor id 
        'status': 1,                <- status id
    }
```

#### 4. getPurchaseOrder(data)
- call url: 'apiv1/inventory/porder'
- POST data format:
```
    {
        action:'get',
        PurchaseOrder_id:
    }
```


#### 5. updatePurchaseOrder(data)
- call url: 'apiv1/inventory/porder'
- POST data format:
```
    {
        'action':'edit',
        'id':1,
        'invoiced_on': "2019-11-16T08:15:00.000",
        'completed_on: "2019-11-16T08:15:00.000",
        'total_cost': 2500,
        'discount_type': 'fixed',    <- can be fixed or percent
        'discount': 25,
        'added_by':1,                <- added_by id
        'vendor':1,                  <- vendor id 
        'status':'1',
    }
```
