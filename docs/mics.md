1. Get Activities logs 
- /user/activities/logs
```
{
    action : get,
    filter : none,
    start : __int__,
    end : __int__
}
```

```
{
    action : get,
    filter : multiple,
    filters : {
        model : __str__ (sales/invoice, inventory/item, inventory/purchase_order etc) / Null,
        action  : delete, create, update, soft_delete / Null,
        object_id  : int,
        object_str : str,
        user : user_id,
        date_range : {
            date_from : 
            date_upto :
        }
    },
    start : ,
    end : ,
}
```

2. Get authentication log (login/logout)
- /user/auth/logs
```
{
    action : get,
    filter : multiple,
    filters : {
        action  : login , logout / Null,
        user : user_id,
        date_range : {
            date_from : 
            date_upto :
        }
    },
    start : 
    end : 
}
```
