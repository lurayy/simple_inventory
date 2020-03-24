#### 1. getPlaces(data)
- call url: 'apiv1/inventory/places'
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
        places: [
            ... places_json
        ]
    }
```


#### 2. deletePlaces(data)
- call url: 'apiv1/inventory/places/delete'
- POST data format:
```
    {
        places_id: [
            #place_id,
            #place_id,
            ...
        ]
    }
```


#### 3. createPlace(data)
- call url: 'apiv1/inventory/places'
- POST data format:
```
    {
        action: add
        name: "klj"             
    }
```


#### 4. getPlace(data)
- call url: 'apiv1/inventory/place'
- POST data format:
```
    {
        action:'get',
        place_id:
    }
```


#### 5. updatePlace(data)
- call url: 'apiv1/inventory/place'
- POST data format:
```
    {
        action: edit
        name: "klj"             
    }
```


#### 6. assignPlace(data)
- call url: 'apiv1/inventory/places/assign'
- POST data format:

    a. For assignment
        ```
        {
            'action':'assign',
            'place_id':1,
            'purchase_item':2,
            'stock':3        
        }
    ```

    b. For deletion
    ```
        {
            'action':'delete',
            'id':2
            'place_id':1,
            'purchase_item':3,
        }
    ```

    c. For update:
    ```
        {
            'action':'edit',
            'id':3,
            'stock':3        
        }
    ```