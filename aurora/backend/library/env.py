import os
import importlib
from aurora.backend.models import Configuration
from django.conf import settings


env_mapping = {}

def mix_update_env(parent_env, child_env):
    for key, value in child_env.items():
        if key in parent_env.keys():
            parent_env[key].update(child_env[key])
        else:
            parent_env[key] = value
    return parent_env


def get_apps_env(scope = 'public'):
    '''
        get settings from all apps
    '''
    # predefined configuration
    apps_env = {}
    apps_dir = os.path.join(settings.BASE_DIR, settings.APPS_DIRNAME)
    for app_name in os.listdir(apps_dir):
        app_dir = os.path.join(apps_dir, app_name)
        if os.path.isfile(os.path.join(app_dir, 'environment.py')):
            mod = importlib.import_module(f'aurora.{app_name}.environment')
            cls = getattr(mod, f'{app_name}Environment')
            if scope == 'backend':
                backend_env = cls.backend
                apps_env.update(mix_update_env(apps_env, backend_env))
            else:
                public_env = cls.public
                apps_env[f'{app_name}'] = public_env
    return apps_env


def get_env(env_app_name = None):
    environments = get_apps_env()
    if env_app_name in environments:
        return environments[env_app_name]
    return environments


def get_object_namespace(namespace):
    setting_list = filter(lambda x: x.startswith(namespace), dir(settings))
    setting_dict = {}
    for i in setting_list:
        setting_dict[i] = getattr(settings, i)
    return setting_dict
