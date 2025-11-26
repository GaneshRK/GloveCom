Hand Sign Translator - Django project
===================================

This is a ready-to-run Django 5.x project (SQLite) scaffold for the "Hand Sign Translator" startup.
It includes:
- core app (landing, contact, pages)
- shop app (products, cart, checkout with Stripe starter)
- users app (auth, profile)
- Bootstrap 5 templates and static assets

Quick start (Linux / macOS / WSL / Windows with PowerShell):
1. Create virtualenv:
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate
2. Install requirements:
    pip install -r requirements.txt
3. Copy .env.example to .env and fill values (optional)
4. Run migrations and create superuser:
    python manage.py migrate
    python manage.py createsuperuser
5. Run dev server:
    python manage.py runserver
6. Open http://127.0.0.1:8000/

Notes:
- Stripe keys in .env are placeholders. For live payments, replace with real keys and set up webhooks.
- Static files are served by Django in DEBUG mode.

