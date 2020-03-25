# API documentation for Frontend Development
- All the js files defining the API calls are located in 'src/api/'.
- All the calls are of POST nature.
- Since we will be using SSH connection, there won't be need to encrypt the POST data.

### API call example : 
- Import API call function form './frontend/src/api/'+name_of_js_file_needed
``` 
    import { loginUser } from '../../api/user';

    loginUser(JSON.stringify(data)).then(data => {
            # handle data
    })
```

### Universal Response during server error: 
```
    {
        status: false,
        errror: #actual error with exception class
    }
```
### Universal Success response: 
```
    {
        status: true
    } 
```


## User_handler 
- Location: '/api/user.js'
- [UserAPI Documentation](users.md)

## Inventory 
- Location: '/api/inventory/...'
- Contains: 
    1. [Items](inventory/item.md)
    2. [Items catagory](inventory/item_catagory.md)
    3. [Places](inventory/place.md)
    4. [Purchase Items](inventory/purchase_item.md)
    5. [Purchase Order](inventory/purchase_order.md)
    6. [Vendor](inventory/vendor.md)