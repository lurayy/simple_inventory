# User Handler 

### 1. Create user 
- /api/v1/user/add
- POST
```
{
    action : add,
    username : __str__,
    email : __str__,
    password : __str__,
    first_name : 
    last_name :
    role_id : __id__,
    profile : null / {
        address : 
        phone_number : 
        phone_number2 :
        post :
        profile_image : null / {}
    }
}
```

### 2. User Listing 
- /api/v1/user/list
- POST
```
{
    action : get
    filter : none
    start : 
    end : 
}
```

#### To get single user data  : 
- /api/v1/user/list
- POST
```
{
    action : get,
    filter : id,
    user_id
}
```

- name 
```
{
    action : get,
    filter : name
    name : __str__
}
```

- role  
```
{
    action  : get,
    filter : role,
    role_id : __id__
}
```

- Status
```
{
    action  : get,
    filter  : status,
    is_active : bool
}
```


### 3. Update user 
- /api/v1/user/update
- POST
```
{
    action : update,
    email : null/__str__,
    first_name: null/str
    last_name : null /str
    password : null/__nwe_password__
    profile : null / {
        address :  null/ str
        phone_number : null/str
        phone_number2 : null/str
        post : null/str
        profile_image : null / {}
    }
}
```

#### self deactivate : 
```
{
    action : deactivate
}
```

### 4. Activate / Delete user 
- /api/v1/user/delete
- POST
```
{
    action : deactivate
    user_id : 
}
```

```
{
    action : activate
    user_id : 
}
```

### 5. Get Roles : 
- /api/v1/user/roles/get
- POST
```
{
    action : get
}
```

### 6. Get role : 
- /api/v1/user/role/get
- POST
```
{
    action : get,
    role_id : __id__
}
```

### 7. Get list of valid powers
- /api/v1/user/role/valid
```
{
    action : get
}
```

### 8. Create New Role: 
- api/v1/user/role/add
```
{
    action : add,
    name : 
    powers : []
    value : [__bool__, ...]
}
```

### 9. Delete Role : 
- api/v1/user/role/delete
```
{
    action  : delete,
    role_id  : id
}
```

### 10. Assign Role : 
- /api/v1/user/role/assign
```
{
    action  : assign 
    user_id : id,
    role_id : id
}
```