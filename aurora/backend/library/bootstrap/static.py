from django.conf import settings
import os


def get_static(filename):
    return os.path.join(settings.STATIC_URL, filename)
