## Requirements
- python 3
- libpq-dev python3-dev


```
sudo apt install libpq-dev python3-dev
```

Configure the postgres with the user id, password and database that is on accounting.settings.database 


## Installation
Create a virutalenv
```
virtualenv -p python3 venv
```
Activate the virutalenv and install the dependencies using
```
pip3 install -r requirements.txt
```

## Run
For running the script, use
```
./seeder.sh
python manage.py runserver
```
