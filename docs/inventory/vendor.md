#### 1. getVendors(data)
- call url: 'apiv1/inventory/vendors'
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

    b. filter by name :
    ```
        {
            "action":"get",
            "start":0,
            "end":5,
            "filter":"name",
            "first_name":
        }
    ```
- Response data format:
```
    {
        status:true,
        vendors: [
            ... vendors_json
        ]
    }
```


#### 2. deletevendors(data)
- call url: 'apiv1/inventory/vendors/delete'
- POST data format:
```
    {
        vendors_id: [
            #vendor_id,
            #vendor_id,
            ...
        ]
    }
```


#### 3. createvendor(data)
- call url: 'apiv1/inventory/vendors'
- POST data format:
```    
    {
        "action":"add",
        "first_name": "Raven2",
        "middle_name": "Ulric2 Davenport",
        "last_name": "Solomon2",
        "email": "qadeg@maili2nator.net",
        "website": "https://www.dogotime.org.uk",
        "tax_number": "974",
        "phone1": "+1 (149) 119-4092",
        "phone2": "+1 (381) 765-8778",
        "address": "Qui in at culpa unde"
    }
```

#### 4. getvendor(data)
- call url: 'apiv1/inventory/vendor'
- POST data format:
```
    {
        action:'get',
        vendor_id:
    }
```


#### 5. updatevendor(data)
- call url: 'apiv1/inventory/vendor'
- POST data format:
```
    {
        "action":"edit",
        "id":2,
        "first_name": "Raven2",
        "middle_name": "Ulric2 Davenport",
        "last_name": "Solomon2",
        "email": "qadeg@maili2nator.net",
        "website": "https://www.dogotime.org.uk",
        "tax_number": "974",
        "phone1": "+1 (149) 119-4092",
        "phone2": "+1 (381) 765-8778",
        "address": "Qui in at culpa unde",
        "is_active":true
    }
```
