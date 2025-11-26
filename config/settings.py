import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY','unsafe-dev-secret')
DEBUG = os.getenv('DJANGO_DEBUG','True') == 'True'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS','localhost,127.0.0.1').split(',')
INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'core','shop','users',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[BASE_DIR/'templates'],
    'APP_DIRS':True,
    'OPTIONS':{'context_processors':[
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'core.context_processors.site_info',
    ]},
}]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

JAZZMIN_SETTINGS = {
    "site_title": "Helping Hands Admin",
    "site_header": "Helping Hands",
    "site_brand": "HH",  
    "welcome_sign": "Welcome Founder!",
    "copyright": "Helping Hands",
    "search_model": ["translator.Product", "auth.User"],

    "show_ui_builder": True,

    "topmenu_links": [
        {"name": "Home", "url": "/", "permissions": ["auth.view_user"]},
        {"model": "translator.Product"},
        {"app": "translator"},
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "translator.Product": "fas fa-hand-peace",
        "translator.Order": "fas fa-shopping-cart",
        "translator.ContactMessage": "fas fa-envelope",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
}
JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",      # Other themes: flatly, darkly, litera, cosmo, etc.
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "footer_fixed": True,
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'
LOGOUT_REDIRECT_URL = '/'
LOGOUT_URL = '/users/logout/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@handsigntranslator.com'

# STRIPE_SECRET_KEY = "sk_test_51SWMbMK3aCnFddlHGTIeo9aASIVdeXXa1QxqcRrJTZbhfrrN6Nd8a4DCVR5qkVLtHA9bNWE6wFFsilVO9K6cJQYL008cDl5y9T"
# STRIPE_PUBLIC_KEY = "pk_test_51SWMbMK3aCnFddlH2hohA2SpZla6j4yKLEsjewgf872Q5JTsOEoG1mCo57Ykxns21yYEyr0zoQybhupJqfPD3eDZ00C84AIs9J"
# STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
