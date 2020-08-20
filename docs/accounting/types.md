#### 1. Get Account Types : 
- URL : api/v1/accounting/accounts/types/get
```
{
    "action":"get"
}
```

2. Add
- URL : api/v1/accounting/accounts/type/add
```
{
    "action":"add",
    'name' : __str__,
    'header' : __header__
}
```


3. Update
- URL : api/v1/accounting/accounts/type/update
```
{
    "action":"update",
    'name' : null / __str__,
    'header' : null / __header__,
    'status' : null/ {
        is_active : __bool__
    }
}
```

4. Delete
- URL : api/v1/accounting/accounts/types/delete
```
{
    "action":"delete",
    'account_type_ids' : [
        __id__, ...
    ]
    }
}
```

