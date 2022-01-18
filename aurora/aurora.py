import os, re, importlib
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from aurora.boot import aurora_name, load_aurora_apps


# set aurora names
APPS_DIRNAME = aurora_name
CONFIG_DIR   = os.path.join(settings.BASE_DIR, 'config')


def get_site_id(site_file):
    SITE_ID = None
    with open(site_file, 'r') as reader:
        site_setting = reader.read()
        site_setting = re.findall('SITE_ID[\s\w]*=[\s]*\d', site_setting)
        if site_setting:
            SITE_ID = re.findall('\d', site_setting[0])
    if SITE_ID:
        return int(SITE_ID[0])


def scan_config(CONFIG_DIR, site_name=False):
    APP_CONFIG = [x for x in os.listdir(CONFIG_DIR) if not x.startswith('__') and x.endswith('.py')]
    for config in APP_CONFIG:
        [mdl_name, mdl_ext] = os.path.splitext(config)
        mdl_loc = f'config.{mdl_name}'
        if site_name:
            mdl_loc = f'config.{site_name}.{mdl_name}'
        module  = importlib.import_module(mdl_loc)
        # avoid private params __function_name__
        for param in [x for x in dir(module) if not x.startswith('__')]:
            # if variable has been defined
            # only need updated
            obj = module.__getattribute__(param)
            if param in globals():
                previous_obj = globals()[param]
                if type(previous_obj) == dict and type(obj) == dict:
                    updated = True
                    if 'update_previous' in obj:
                        updated = obj['update_previous']
                    if updated:
                        previous_obj.update(obj)
            else:
                globals()[param] = obj


def initialization_config(CONFIG_DIR):
    scan_config(CONFIG_DIR)
    if settings.SITE_ID > 1:
        APP_CONFIG = [x for x in os.listdir(CONFIG_DIR) if not x.startswith('__') and os.path.isdir(os.path.join(CONFIG_DIR, x))]
        for site_dir in APP_CONFIG:
            site_file = os.path.join(CONFIG_DIR, site_dir, '__init__.py')
            SITE_ID   = get_site_id(site_file)
            if SITE_ID == settings.SITE_ID:
                CONFIG_DIR = os.path.join(CONFIG_DIR, site_dir)
                scan_config(CONFIG_DIR, site_dir)
                break


def create_config(CONFIG_DIR, site_id, site_name, site_file):
    sub_config_dir   = os.path.join(CONFIG_DIR, site_name)
    init_config_file = os.path.join(sub_config_dir, '__init__.py')
    if not os.path.exists(sub_config_dir):
        os.makedirs(sub_config_dir)
    with open(init_config_file, 'w') as writer:
        writer.write(f'# Contextual setting for site -> {site_name}\n')
        writer.write(f'# Parent setting -> {site_file}\n\n')
        writer.write(f'SITE_ID = {site_id}\n')


def create_sgi_config(site_id, site_name, gateway):
    sgi_dir  = os.path.join(settings.SITE_DIR, f'{gateway}')
    sgi_file = os.path.join(sgi_dir, f'{site_name}.py')
    if not os.path.exists(sgi_dir):
        os.makedirs(sgi_dir)
    if not os.path.isfile(sgi_file):
        # get parent sgi config
        with open(os.path.join(settings.SITE_DIR.parent, f'{gateway}.py'), 'r') as reader:
            parent_wsgi_data = reader.read()
        with open(sgi_file, 'w') as writer:
            writer.write(f'# Contextual setting for site -> {site_name}\n')
            writer.write(f'# You have to fix environment variable \n\n')
            writer.write(parent_wsgi_data)


def create_gateway_config(site_id, site_name):
    # create WSGI config
    create_sgi_config(site_id, site_name, 'wsgi')
    # create ASGI config
    create_sgi_config(site_id, site_name, 'asgi')



def create_multisite_initset():
    site_setting = [(os.path.basename(site_file), os.path.join(settings.SITE_DIR, site_file)) for site_file in os.listdir(settings.SITE_DIR)]
    site_setting = filter(lambda x: x[0].endswith('.py') and not x[0].startswith('__'), site_setting)
    site_setting = [(x, y, os.path.splitext(x)) for (x, y) in site_setting]
    for site_basename, site_file, (site_name, site_ext) in site_setting:
        SITE_ID = get_site_id(site_file)
        if SITE_ID:
            # create independent site config
            create_config(CONFIG_DIR, SITE_ID, site_name, site_file)
            # create independent site wsgi
            create_gateway_config(SITE_ID, site_name)


def initialization_aurora():
    # create multisite initialization settings
    INSTALLED_APPS, MIDDLEWARE, TEMPLATES = load_aurora_apps(
        settings.INSTALLED_APPS,
        settings.MIDDLEWARE,
        settings.TEMPLATES)
    globals()['INSTALLED_APPS'] = INSTALLED_APPS
    globals()['MIDDLEWARE'] = MIDDLEWARE
    globals()['TEMPLATES'] = TEMPLATES
    create_multisite_initset()


# it must be run in first start
initialization_config(CONFIG_DIR)
initialization_aurora()

