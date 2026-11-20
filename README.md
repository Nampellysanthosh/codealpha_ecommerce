# Bazaar

Bazaar is a Django-based online store with product browsing, search, categories, a session-based shopping cart, user accounts, checkout, order history, and an admin site.

## Features

- Browse products by category and search by product name, description, or category.
- View product details and stock availability.
- Add products to a session-based cart and update quantities.
- Register, sign in, and place orders through checkout.
- View order history and order details.
- Manage products and orders through Django Admin.
- Load sample products with a Django management command.

## Technology

- Python
- Django
- SQLite
- HTML, CSS, and JavaScript
- Pillow

## Project layout

```text
shoping-cart/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── db.sqlite3                 # Local database; ignored by Git
├── bazaar/                    # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── store/                     # Store application
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── admin.py
    ├── migrations/            # Database schema migrations
    ├── management/
    │   └── commands/
    │       └── seed_products.py
    ├── templates/store/       # HTML templates
    └── static/store/          # CSS, JavaScript, and images
```

## Run locally (Windows)

Open PowerShell in the project folder.

1. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

2. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use the virtual environment's Python directly in the commands below, for example `.\venv\Scripts\python.exe`.

3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Create or update the local database:

   ```powershell
   python manage.py migrate
   ```

5. Add the sample catalog (optional; safe to run again):

   ```powershell
   python manage.py seed_products
   ```

6. Create an admin account (optional):

   ```powershell
   python manage.py createsuperuser
   ```

7. Start the development server:

   ```powershell
   python manage.py runserver
   ```

   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for the store or [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) for Django Admin. Keep the terminal running while you use the site.

## Checks

Run Django's configuration check and test discovery with:

```powershell
python manage.py check
python manage.py test
```

The project currently has no automated test cases, so `manage.py test` may report that no tests were found.

## Push the project to GitHub

1. Sign in to GitHub and create a **new empty repository**. Do not initialize it with a README, license, or `.gitignore` because those files are already in this project.
2. Open PowerShell in the project folder and initialize Git:

   ```powershell
   git init
   git branch -M main
   ```

3. Review what Git will include:

   ```powershell
   git status
   ```

   The `.gitignore` excludes the virtual environment, local SQLite database, uploaded media, environment files, and Python cache files. Do not commit passwords, API keys, or other secrets.

4. Stage and commit the project:

   ```powershell
   git add .
   git status
   git commit -m "Add Bazaar Django store"
   ```

5. Connect the local project to the GitHub repository. Replace the URL with the one GitHub shows for your repository:

   ```powershell
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   git push -u origin main
   ```

   GitHub may ask you to authenticate. Use GitHub's browser sign-in, Git Credential Manager, or an SSH remote; do not put a password or access token in the command or source files.

For later updates, use:

```powershell
git add .
git commit -m "Describe your changes"
git push
```

## Deployment note

The built-in Django development server and the local URL above are for development only. Before deploying publicly, configure a private `SECRET_KEY`, set `DEBUG=False`, restrict `ALLOWED_HOSTS`, and use production-ready hosting, database, and static-file settings.
