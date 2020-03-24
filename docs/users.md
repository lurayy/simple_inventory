
#### 1. loginUser(data)
- call url : apiv1/users/login
- POST data format : 
``` 
{
    username: "USERNAME",
    password: "PASSWORD"
}
```
- Retrun data: 
If login is successful: 
```
{
    status: true
}
```
If login failed:
```
{
    status:false,
    msg : "msg"
}
```

#### 2. logOut()
- call url: 'apiv1/users/logout'
- No data needed
- Response : redirection to login

#### 3. createUser(data)
- call url: 'apiv1/users/create'
- only manager can all this url
- POST Format: 
```
{
    username: "USERNAME",
    password: "password",
    first_name: ,
    last_name: ,
    user_type: ,            #can only be staff or manager
}
```

#### 4. getUsers(data)
- call url: 'apiv1/users/get'
- POST format:
```
{
    action: 'get',
    start: 0,
    end: 20
}
```
- Success response 
```
{
    status: true,
    users: [
        {
            id:
            name:
            status:
            username:
            uuid:
        },
        {
            id:
            name:
            status:
            username:
            uuid:
        }
        ...
    ]
}
```

#### 5. getUser(data)
- call url: 'apiv1/users/get/0'
- POST format for getting info:
```
{
    action: "get",
    user_id: 
    uuid:
}
```
- POST format for deleting/reviving user
```
{
    action: delete/revive
    user_id:
    uuid:
}
```

#### 6. updateUser(data)
- call url: 'apiv1/users/get/0'
- POST format for modifying/updating user's data:
```
{
    action: 'edit',
    user_id: '4',
    uuid: 'c4971e44-a4d8-4675-ad27-e7b3fd24332a',      
    first_name:
    last_name:
    email:
    username:
    user_type:
}
```

#### 7. getCurrentUser()
- call url: 'apiv1/users/current'
- No post data is needed
- give data related to the loggedin user 