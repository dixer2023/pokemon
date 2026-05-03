# Setup script for Pokemon Pokedex Django project

Write-Host "Restoring clean settings file..." -ForegroundColor Green
Copy-Item -Path "c:\Users\User\Desktop\pokemon\pokemon\pokemon\pokemon\settings_new.py" `
          -Destination "c:\Users\User\Desktop\pokemon\pokemon\pokemon\pokemon\settings.py" `
          -Force

Write-Host "Running migrations..." -ForegroundColor Green
Set-Location "c:\Users\User\Desktop\pokemon\pokemon\pokemon"
& python manage.py migrate

Write-Host "Loading Pokemon data..." -ForegroundColor Green
& python manage.py load_pokemon

Write-Host "Starting development server..." -ForegroundColor Green
& python manage.py runserver
