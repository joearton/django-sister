import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lwv$zb+$vw3+lcac)bi&qhw%fdk6%2v^l&ab%8=8xrx&f!o93!'


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'dal',
    'dal_select2',
    # 'debug_toolbar',
    'ckeditor',
    'crispy_forms',
    'crispy_bootstrap5',
    'captcha',
    'sweetify',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# default setting start #

# Multi sides features
SITE_DIR = Path(__file__).resolve(strict=True).parent.joinpath('sites')

# enable multi side feature
SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DESIGN_MODE = True

# enable or disable maintenance mode
MAINTENANCE = False

MAINTENANCE_MESSAGE = None

ALLOWED_HOSTS = []

ROOT_URLCONF = 'sister.urls'

WSGI_APPLICATION = 'sister.wsgi.application'
ASGI_APPLICATION = 'sister.asgi.application'

# Static files (CSS, JavaScript, Images)
STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL   = '/media/'
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')


if os.getenv('DJANGO_SETTINGS_MODULE') == __name__:
    from aurora.aurora import *