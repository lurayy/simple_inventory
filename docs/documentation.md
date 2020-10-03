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

## Accounting
- API: 'api/v1/accouting/'
- Contains:
    1. [Accounts](accounting/accounts.md)
    2. [Account Types](accounting/types.md)
    3. [Ledger Entries](accounting/ledger_entries.md)




#### Please note documents below has not been updated.
## User_handler 
- Location: '/api/user.js'
- [UserAPI Documentation](users.md)

## Inventory 
- Location: '/api/v1/inventory/...'
- Contains: 
    1. [Items](inventory/item.md)
    2. [Items category](inventory/item_category.md)
    3. [Places](inventory/place.md)
    4. [Purchase Items](inventory/purchase_item.md)
    5. [Purchase Order](inventory/purchase_order.md)
    6. [Vendor](inventory/vendor.md)

