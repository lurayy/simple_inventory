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
    first_name: null/str
    last_name : null /str
    password : null/__nwe_password__
    profile : null / {
        address :  null/ str
        phone_number : null/str
        phone_number2 : null/str
        post : null/str
        profile_image : null / {} / remove  <---- null for no change/ {} - to update image / remove to remove exsisting image
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
    powers : [],
    description : __str__,
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

### 11. Logout Notification 
- api/v1/user/logtime
- GET
[Must be call after user logs out or after deleting token]

### 12. Get activity logs
- api/v1/user/logs/get
- POST
```
{
  'action' : 'get',
  'start' : 0,
  'end' : 25,
  'filter' : 'multiple'/ "None",
  'filters':{
    'date':None,
        'start_date' :
        'end_date' :
    'user':1/None,
    'action' : "LOGIN"/ LOGOUT/ None
  }
}
```

### 13. Role Update:
- api/v1/user/role/update
- POST 
```
{
    action : update,
    role_id :
    name : 
    description
    powers : [],
    values : []
}
``` 


### 14. Password Reset Process
i. Initiate : 
- /api/v1/user/password/forget
```
{
    email : __valid_email__
}
```

A unique code is then mailed to the given email if the user is registered, if not an error response is sent.

ii. Check code validity : 
- /api/v1/user/password/code/validate
```
{
    code : 
}
```

iii. Reset password
- /api/v1/user/password/reset
```
{
    code : 
    password : 
}
```
