from django.utils.translation import gettext_lazy as _
from aurora.backend.library.bootstrap.static import get_static


BACKEND_SETTINGS = {
    'site_title'        : _('Human Resource'),
    'site_subtitle'     : 'Universitas Muhammadiyah Kotabumi',
    'navigation_top'    : {},
    'aurora_backend'    : True,
    'aurora_auth'       : True,
    'maintenance'       : True, # enable maintenance mode/URL in general
    'theme_mode'        : 'light', # light or dark
    'theme_accent'      : 'blue', # army, ubuntu, deep, blue, softblue, modern-green, green, elegant
    'theme_style'       : 'default', # default, minified, floated, simplex, flatpage, topmenu
    'home_url'          : '/pilar/dashboard',
    'maintenance_path'  : 'maintenance',
    'favicon'           : 'backend/media/favicon.png',
    'logo'              : {
        'url'           : 'backend/media/favicon.png',
        'use_text'      : True,
        'height'        : '30px',
    },
    'signup_method'     : 'e-mail',
    'password_policy'   : {'min': 8, 'max': 32},
    'auth_info'         : {
        'title'         : _('Human Resource'),
        'description'   : _('This is sign in page. Use your e-mail or username and password before using our system.'),
        'background'    : get_static('backend/media/human_resource.jpg'),
        'color'         : 'light',
        'overlay'       : 'primary',
        'opacity'       : '.55',
        'link'          : {
            'url'       : '#',
            'target'    : '_self',
            'label'     : _('Readmore'),
        }
    }
}