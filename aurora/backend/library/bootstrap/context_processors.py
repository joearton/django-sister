from aurora.backend.library import env
from django.conf import settings


def contextual(request):
    config = {
        'base_dir': settings.BASE_DIR,
        'debug': settings.DEBUG,
    }
    if hasattr(settings, 'HOST_PROTOCOL'):
        config['host'] = settings.HOST_PROTOCOL
    if hasattr(settings, 'FRONTEND_SETTINGS'):
        config['frontend'] = settings.FRONTEND_SETTINGS
    if hasattr(settings, 'BACKEND_SETTINGS'):
        config['backend'] = settings.BACKEND_SETTINGS
    context_proccessor = {
        "env": {
            'public': env.get_env('public'),
            'backend': env.get_apps_env('backend'),
        },
        'config': config,
    }
    return context_proccessor
