import os
from django.conf import settings

# Internationalization

USE_I18N = True

# if you want to change date/time format
USE_L10N = True

USE_TZ = True

# only works when USE_L10N is False
DATE_FORMAT = 'd-m-Y'
DATETIME_FORMAT = 'd/m/Y G:i:s'

SITE_ROOT = os.path.dirname(os.path.realpath(__name__))
LOCALE_PATHS = ( os.path.join(SITE_ROOT, 'locale'), )

LANGUAGES = (
    ('en', 'English'),
    ('id', 'Bahasa Indonesia'),
)

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Jakarta'

