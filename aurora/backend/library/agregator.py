import importlib
import inspect
from django.conf import settings
from aurora.boot import get_aurora_apps, scan_apps


def manage_apps(request, res, command):
    app_name = request.POST.get('app-name')
    builtin  = get_aurora_apps()['builtin']
    if app_name in builtin:
        if builtin[app_name]['editable']:
            if command == 'start':
                builtin[app_name]['autoload'] = True
            else:
                builtin[app_name]['autoload'] = False
    scan_apps(builtin)
    return res
