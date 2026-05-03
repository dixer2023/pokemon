@echo off
REM Setup script for Pokemon Pokedex Django project

echo Copying clean settings file...
copy "c:\Users\User\Desktop\pokemon\pokemon\pokemon\pokemon\settings_new.py" "c:\Users\User\Desktop\pokemon\pokemon\pokemon\pokemon\settings.py"

echo Running migrations...
cd c:\Users\User\Desktop\pokemon\pokemon\pokemon
python manage.py migrate

echo Loading Pokemon data...
python manage.py load_pokemon

echo Creating superuser...
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo Starting development server...
python manage.py runserver

pause
