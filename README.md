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
