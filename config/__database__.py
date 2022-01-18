# AUTH_USER_MODEL = 'backend.User'

# Remote Database
REMOTE_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'NAME',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

# Local Database
LOCAL_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'NAME',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

DATABASES = LOCAL_DATABASE

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
