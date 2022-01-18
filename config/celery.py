'''
    # General Celery Command
    celery multi start 2 -Q:1 default -Q:2 starters -c:1 5 -c:2 3 --loglevel=INFO --pidfile=/var/run/celery/${USER}%n.pid --logfile=/var/log/celeryd.${USER}%n.log    
    $ celery -A proj multi start worker1 \
        --pidfile="$HOME/run/celery/%n.pid" \
        --logfile="$HOME/log/celery/%n%I.log"

    $ celery -A proj multi restart worker1 \
        --logfile="$HOME/log/celery/%n%I.log" \
        --pidfile="$HOME/run/celery/%n.pid
    $ celery multi stopwait worker1 --pidfile="$HOME/run/celery/%n.pid"    
'''

import os
from django.conf import settings
from config import CACHE_DIR

# CELERY SETTING
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = settings.TIME_ZONE


# CELERY WORKER
CELERY_PROJECT = 'pilar'
CELERY_DIR = os.path.join(CACHE_DIR, 'celery')
CELERY_PID = os.path.join(CELERY_DIR, 'pid')
CELERY_LOG = os.path.join(CELERY_DIR, 'log')

if not os.path.exists(CELERY_LOG):
    os.makedirs(CELERY_LOG)
if not os.path.exists(CELERY_PID):
    os.makedirs(CELERY_PID)