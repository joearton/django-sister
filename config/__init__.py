import os
from pathlib import Path
from django.conf import settings


# prepare application logs
CACHE_DIR = os.path.join(settings.BASE_DIR, '.cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


# AURORA_LOADER = ['middleware', 'context_proccessor']