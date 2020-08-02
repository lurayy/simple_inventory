python3 manage.py flush
python3 manage.py shell < create_custom_permission.py
python3 manage.py makemigrations user_handler sales inventory payment accounting
python3 manage.py migrate 
python3 manage.py createsuperuser
python3 manage.py shell < seeder.py