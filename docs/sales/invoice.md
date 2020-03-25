#### 1. getInvoices(data)
- call url: 'apiv1/inventory/invoices'
- POST data format:

     1. filter = None
    ```
    {
        'action':'get',
        'filter':'none',
        'start':0,
        'end':10,        
    }
    ```

    2. filter = Status
    ```
    {
        'action':'get',
        'filter':'status',
        'start':0,
        'end':10,
        'status':'draft'/'sent'/'due'/'paid'        
    }
    ```

    3. filter by date :
    ```
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'date',
        'start_date': "2019-11-16T08:15:00.000",
        'end_date': "2019-11-16T08:15:00.000",
    }
    ```
    4. filter by customer :
    ```
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'customer',
        'customer_id':1
    }
    ```
    5. filter by multiple:
    ```
    {
        'action':'get',
        'start':0,
        'end':20,
        'filter':'multiple',
        'status':'draft',
        'customer_id':1,
        ...... 
        # need more work after colaborating with front end
    }
    ```
- Response data format:
```
    {
        status:true,
        invoices: [
            ... Invoices_json
        ]
    }
```


#### 2. deleteInvoices(data)
- call url: 'apiv1/inventory/invoices/delete'
- POST data format:
```
    {
        purchase_orders_id: [
            #Invoice_id,
            #Invoice_id,
            ...
        ]
    }
```


#### 3. createInvoice(data)
- call url: 'apiv1/inventory/invoices'
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
        'status': "paid"
    }
```

#### 4. getInvoice(data)
- call url: 'apiv1/inventory/invoice'
- POST data format:
```
    {
        action:'get',
        invoice_id:
    }
```


#### 5. updateInvoice(data)
- call url: 'apiv1/inventory/invoice'
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
        'status':'paid',
    }
```
