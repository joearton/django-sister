import os
import importlib
import logging
import json
import inspect
import time
from django.conf import settings


aurora_name    = 'aurora'
aurora_apps    = os.path.join(settings.BASE_DIR, aurora_name)
cache_dir      = os.path.join(settings.BASE_DIR, '.cache')
aurora_json    = os.path.join(cache_dir, f'apps-site-{settings.SITE_ID}.json')
aurora_listdir = os.listdir(aurora_apps)
backend_index  = 0
sass_watches   = {
    # all files on SASS watch dir must be on
    # apps/app_name/static/app_name directory
    # and must have css and scss folder inside it
    'backend': 'bootstrap',
}


def_app_list = {
    'jazzmin'                    : {'required': True, 'editable': False, 'autoload': True},
    'django.contrib.admin'       : {'required': True, 'editable': False, 'autoload': True},
    'django.contrib.auth'        : {'required': True, 'editable': False, 'autoload': True},
    'django.contrib.contenttypes': {'required': True, 'editable': False, 'autoload': True},
    'django.contrib.sessions'    : {'required': True, 'editable': False, 'autoload': True},
    'django.contrib.messages'    : {'required': True, 'editable': False, 'autoload': True},
    'django.contrib.staticfiles' : {'required': True, 'editable': False, 'autoload': True},
    'django.contrib.humanize'    : {'required': True, 'editable': False, 'autoload': True},
    'django.contrib.sites'       : {'required': True, 'editable': False, 'autoload': True},
    'dal'                        : {'required': True, 'editable': False, 'autoload': True},
    'dal_select2'                : {'required': True, 'editable': False, 'autoload': True},
    'debug_toolbar'              : {'required': True, 'editable': False, 'autoload': True},
    'ckeditor'                   : {'required': True, 'editable': False, 'autoload': True},
    'crispy_forms'               : {'required': True, 'editable': False, 'autoload': True},
    'crispy_bootstrap5'          : {'required': True, 'editable': False, 'autoload': True},
    'captcha'                    : {'required': True, 'editable': False, 'autoload': True},
    'mptt'                       : {'required': True, 'editable': True,  'autoload': True},
    'sweetify'                   : {'required': True, 'editable': False, 'autoload': True},
}


def get_mdr_class(app_name):
    mdr_list = []
    middleware_file = os.path.join(aurora_apps, app_name, 'library', 'bootstrap', 'middleware.py')
    if os.path.isfile(middleware_file):
        mdr_module  = f'aurora.{app_name}.library.bootstrap.middleware'
        mdr_classes = dir(importlib.import_module(mdr_module))
        for class_name in mdr_classes:
            if class_name.endswith('Middleware'):
                mdr_class = f'aurora.{app_name}.library.bootstrap.middleware.{class_name}'
                mdr_list.append(mdr_class)
    return mdr_list


def get_context_processor(app_name):
    context = None
    cp_path = os.path.join(aurora_apps, app_name, 'library', 'bootstrap', 'context_processors.py')
    if os.path.isfile(cp_path):
        context = f'aurora.{app_name}.library.bootstrap.context_processors.contextual'
    return context


def get_template_tags(app_name):
    templatetags = {}
    tt_dir = os.path.join(aurora_apps, app_name, 'templatetags')
    if os.path.exists(tt_dir):
        tt_files = [(os.path.basename(t), os.path.join(tt_dir, t)) for t in os.listdir(tt_dir)]
        tt_files = filter(lambda x: x[0].endswith('.py') and not x[0].startswith('__'), tt_files)
        for tt_name, tt_path in list(tt_files):
            name, ext = os.path.splitext(tt_name)
            tt_mdl = importlib.import_module(f'aurora.{app_name}.templatetags.{name}')
            templatetags[name] = []
            for index in inspect.getmembers(tt_mdl, inspect.isfunction):
                templatetags[name].append(index[0])
    return templatetags


def scan_apps(builtin={}):
    app_dict = {
        'created_at' : str(time.time()),
        'dir_length' : len(aurora_listdir),
        'aurora'     : {},
        'builtin'    : builtin,
    }
    for app_name in aurora_listdir:
        app_signer = os.path.join(aurora_apps, app_name, 'apps.py')
        if os.path.isfile(app_signer):
            app_dict['aurora'][app_name] = {'namespace': f'aurora.{app_name}'}
            app_dict['aurora'][app_name]['middlewares'] = get_mdr_class(app_name)
            app_dict['aurora'][app_name]['context'] = get_context_processor(app_name)
            app_dict['aurora'][app_name]['templatetags'] = get_template_tags(app_name)
    with open(aurora_json, 'w') as writer:
        writer.write(json.dumps(app_dict))
    print('Aurora apps are indexed...')


def get_aurora_apps():
    if not os.path.isfile(aurora_json):
        scan_apps()
    with open(aurora_json, 'r') as reader:
        data = json.load(reader)
        if data['dir_length'] != len(aurora_listdir):
            scan_apps()
        return data


def get_app_name(app_name):
    if app_name.find('.') == -1:
        return (app_name, None)
    x = app_name.split('.')
    app_name = x[len(x)-1]
    parent_name = '.'.join(x[:len(x)-1])
    return (app_name, parent_name)


def get_builtin_apps(aurora):
    apps = {}
    for app_name in settings.INSTALLED_APPS:
        if app_name in def_app_list:
            apps[app_name] = def_app_list[app_name]
        else:
            # create default properties for unindexed application
            apps[app_name] = {'required': True, 'editable': True, 'autoload': True}
        name, parent = get_app_name(app_name)
        apps[app_name]['name'] = name
        apps[app_name]['parent'] = parent
        apps[app_name]['templatetags'] = {}
        apps[app_name]['templatetags_count'] = 0
        app_obj = importlib.import_module(app_name)
        if hasattr(app_obj, 'templatetags'):
            tt_mdls = getattr(app_obj, 'templatetags')
            for tt_mdl in list(filter(lambda x: x.startswith('__') == False, dir(tt_mdls))):
                tt_obj = importlib.import_module(f'{app_name}.templatetags.{tt_mdl}')
                ttags  = inspect.getmembers(tt_obj, inspect.isfunction)
                ttags  = [x[0] for x in ttags]
                apps[app_name]['templatetags'][tt_mdl] = ttags
                apps[app_name]['templatetags_count'] += len(ttags)
        if name in aurora['aurora']:
            apps[app_name].update(aurora['aurora'][name])
    apps = dict(sorted(apps.items(), key=lambda x: x[1]['editable'], reverse=True))
    return apps


def get_app_list():
    aurora = get_aurora_apps()
    if not aurora['builtin']:
        aurora['builtin'] = get_builtin_apps(aurora)
    # scan_apps(aurora['builtin'])
    return aurora['builtin']


def is_autoload(app_name):
    app_list = get_app_list()
    if app_name in app_list:
        return app_list[app_name]['autoload']


def load_aurora_apps(installed_apps, middleware, template):
    installed_apps.insert(backend_index, 'aurora.backend')
    scan_apps = get_aurora_apps()
    for app_name, app_data in scan_apps['aurora'].items():
        aurora_app = app_data['namespace']
        if not aurora_app in installed_apps:
            installed_apps.append(aurora_app)
        mdr_list = app_data['middlewares']
        if mdr_list:
            middleware.extend(mdr_list)
        context = app_data['context']
        if context:
            template[0]['OPTIONS']['context_processors'].append(context)
    return [installed_apps, middleware, template]


def scss_to_css(app_name, scss_dir, css_dir):
    '''
        Harus diimport disini karena menggunakan ekstensi C
        ModWSGI is not compatibel with this extentios, except use WSGIApplicationGroup %{GLOBAL}
    '''
    import sass
    if os.path.exists(scss_dir) and os.path.exists(css_dir):
        sass.compile(dirname=(scss_dir, css_dir), output_style='compressed')
        logging.info(f"SASS [{app_name}] are generated...")



def generate_scss_to_css(execute_scss = True):
    watch_scss = []
    for app_name in os.listdir(aurora_apps):
        app_signer = os.path.join(aurora_apps, app_name, 'apps.py')
        if os.path.isfile(app_signer):
            styling_dir = os.path.join(aurora_apps, app_name, 'static', app_name, 'styling')
            if app_name in sass_watches.keys():
                swd_scss = os.path.join(styling_dir, sass_watches[app_name], 'scss')
                swd_css  = os.path.join(styling_dir, sass_watches[app_name], 'css')
                if os.path.exists(swd_scss):
                    if execute_scss:
                        scss_to_css(app_name, swd_scss, swd_css)
                    watch_scss.append(swd_scss)
            # generating scss to css on application styling directory
            scss_dir = os.path.join(styling_dir, 'scss')
            css_dir  = os.path.join(styling_dir, 'css')
            if os.path.exists(scss_dir):
                if execute_scss:
                    scss_to_css(app_name, scss_dir, css_dir)
                watch_scss.append(scss_dir)
    return watch_scss


def generate_js_admin(execute_js = True): # inactive
    watch_js = []
    backend_js_dir = os.path.join(aurora_apps, 'backend', 'static', 'backend', 'scripting')
    for app_name in os.listdir(aurora_apps):
        if not app_name == 'backend':
            app_signer = os.path.join(aurora_apps, app_name, 'apps.py')
            if os.path.isfile(app_signer):
                apps_js_dir = os.path.join(aurora_apps, app_name, 'static', app_name, 'scripting')
                apps_js_file = os.path.join(apps_js_dir, 'admin.js')
                if os.path.isfile(apps_js_file):
                    watch_js.append(apps_js_dir)
    if execute_js:
        with open(os.path.join(backend_js_dir, 'admin.template.js'), 'r') as reader:
            admin_js_template =  reader.read()
            gs_str = ''
            for js_dir in watch_js:
                js_file = os.path.join(js_dir.split('/static/')[1], 'admin.js')
                gs_str += "$.getScript('/static/%s', function(data, textStatus, jqxhr) {})\n".format(js_file)
            with open(os.path.join(backend_js_dir, 'admin.js'), 'w') as writer:
                writer.write(admin_js_template.replace('', gs_str))
    return watch_js
