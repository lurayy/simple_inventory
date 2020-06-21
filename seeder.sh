rm db.sqlite3
python3 manage.py shell < create_custom_permission.py
python3 manage.py makemigrations user_handler sales inventory payment accounting
python3 manage.py migrate 
python3 manage.py createsuperuser
python3 manage.py shell < seeder.py
python3 manage.py loaddata accounting_seed.json