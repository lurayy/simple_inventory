# API documentation for Frontend Development
All the js files defining the API calls are located in 'src/api/'.
All the calls are of POST nature.
Since we will be using SSH connection, there won't be need to encrypt the POST data.

### API call example : 
Import API call function form './frontend/src/api/'+name_of_js_file_needed
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


# User_handler 
- Location : '/api/user.js'

### loginUser(data)
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

### logOut()
- call url: 'apiv1/users/logout'
- No data needed
- Response : redirection to login


### createUser(data)
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

### getUsers(data)
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

### getUser(data)
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

### updateUser(data)
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

### getCurrentUser()
- call url: 'apiv1/users/current'
- No post data is needed
- give data related to the loggedin user 

