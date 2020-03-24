# Mandala IMS

### Requirements
- python 3
- libpq-dev python3-dev
- npm
```
sudo apt install libpq-dev python3-dev npm
```

### Installation
- clone the project

- Create a virutalenv
```
 virtualenv -p python3 venv
```

- Activate the virutalenv
```
source venv/bin/activate
```

-Install the dependencies using
```
pip3 install -r requirements.txt
```

- Instal dependencies for reactjs
```
cd frontend
npm install
```
- Initiate database (on project root folder, cd ..)
```
./seeder.sh
```

### Run the project

- To run reactjs:
```
npm start
```

- To build frontend 
```
npm run build
```
- Run the backend Django server
```
python3 manage.py runserver
```

- To create super user
```
python3 manage.py createsuperuser
```

# [Documentation](docs/documentation.md)

## [Reactjs Documentation](frontend/README.md)
## API documentation for Frontend Development
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
- [UserAPI Documentation](docs/users.md)

## Inventory 
- Location: '/api/inventory/...'
- Contains: 
    1. [Items](docs/inventory/item.md)
    2. [Items catagory](docs/inventory/item_catagory.md)
    3. [Places](docs/inventory/place.md)
    4. [Purchase Items](docs/inventory/purchase_item.md)
    5. [Purchase Order](docs/inventory/purchase_order.md)
    6. [Vendor](docs/inventory/vendor.md)