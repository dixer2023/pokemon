# Pokemon Pokedex Website

A Django-based Pokemon card display website showing Pokemon and their evolution lines.

## Project Structure

```
pokemon/
├── pokemon/                      # Django project directory
│   ├── manage.py
│   ├── pokemon.csv              # Pokemon data
│   └── pokemon/                 # Django settings
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
│   └── pokedex/                 # Main app
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── templates/           # HTML templates
│       └── static/              # CSS and static files
├── setup.ps1                    # PowerShell setup script
└── setup.bat                    # Batch setup script
```

## Installation & Setup

### Option 1: Using PowerShell (Recommended)

1. Open PowerShell as Administrator
2. Navigate to the project folder: `cd C:\Users\User\Desktop\pokemon\pokemon`
3. Run the setup script:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   .\setup.ps1
   ```

### Option 2: Using Command Prompt

1. Open Command Prompt
2. Navigate to the project folder: `cd C:\Users\User\Desktop\pokemon\pokemon`
3. Run the setup script:
   ```cmd
   setup.bat
   ```

### Manual Setup (If Scripts Don't Work)

1. **First, fix the settings.py file:**
   ```powershell
   Copy-Item -Path "pokemon\pokemon\settings_new.py" -Destination "pokemon\pokemon\settings.py" -Force
   ```

2. **Run migrations:**
   ```cmd
   cd pokemon
   python manage.py migrate
   ```

3. **Load Pokemon data:**
   ```cmd
   python manage.py load_pokemon
   ```

4. **Start the development server:**
   ```cmd
   python manage.py runserver
   ```

5. **Access the site:**
   - Open your browser and go to: `http://127.0.0.1:8000/`

## Features

- **Pokemon Grid Display**: View all Pokemon in a beautiful card grid
- **Pokemon Details**: Click any card to see detailed information
- **Evolution Lines**: See the complete evolution chain for each Pokemon
- **Stats Display**: View HP, Attack, Defense, Sp. Atk, Sp. Def, and Speed
- **Type Badges**: Color-coded Pokemon types
- **Official Artwork**: Pokemon images fetched from PokeAPI

## URLs

- `/` - Main Pokemon grid page
- `/pokemon/<id>/` - Detailed view of a specific Pokemon
- `/admin/` - Django admin panel (after creating superuser)

## Admin Console

To access the admin console:

1. Create a superuser:
   ```cmd
   python manage.py createsuperuser
   ```

2. Go to `http://127.0.0.1:8000/admin/` and log in

## Customization

### Adding More Evolution Chains

Edit `pokedex/models.py` and update the `EVOLUTION_CHAINS` dictionary according to official Pokemon evolution data.

### Styling

All CSS is in `pokedex/static/css/style.css`. Colors, layout, and responsive design can be customized there.

### Templates

Templates are in `pokedex/templates/pokedex/`:
- `index.html` - Grid view of all Pokemon
- `detail.html` - Detailed view of a single Pokemon
- `base.html` - Base template with header and footer

## Data Source

Pokemon data comes from `pokemon.csv` which contains:
- Pokedex number and name
- Types (type1 and type2)
- Base stats (HP, Attack, Defense, etc.)
- Height, weight, and classification
- Capture rate

## Technologies Used

- **Django 5.2.8** - Web framework
- **Python 3.10+** - Programming language
- **SQLite3** - Database
- **HTML5/CSS3** - Frontend
- **PokeAPI** - Official Pokemon artwork

## License

Educational use only. Pokemon is copyright The Pokemon Company.
