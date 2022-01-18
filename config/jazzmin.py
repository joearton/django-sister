from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.conf import settings


USER_MODEL = 'auth.User'
if getattr(settings, "AUTH_USER_MODEL"):
    USER_MODEL = settings.AUTH_USER_MODEL


backend_menu = [
    {
        "name": _('Services'), 
        "url": reverse_lazy('admin:backend.service_config'), 
        "icon": "fas fa-cogs",
        "permissions": ["backend"]
    },
    {
        "name": _('Applications'), 
        "url": reverse_lazy('admin:backend.application_config'), 
        "icon": "fas fa-list-alt",
        "permissions": ["backend"]
    },
]


JAZZMIN_SETTINGS = {
    'site_title': _('Simlitabmas'),
    'site_header': _('Simlitabmas'),
    'site_logo': 'backend/media/favicon.png',
    'welcome_sign': _('Welcome, Administrator!'),
    'copyright': 'ArtonLabs',
    'search_model': USER_MODEL,
    "user_avatar": 'get_profile_picture',
    'topmenu_links': [
        {'model': USER_MODEL},
        {'app': 'frontend'},
        {'app': 'pilar'},
        {"name": _("View Site"), "icon": "fa fa-globe", "url": "/", "new_window": False},
    ],
    "language_chooser": True,
    'usermenu_links': [
        {"name": _("Switch Role"), "icon": "fa fa-user", "url": "aurora.backend.account.role", "new_window": False},
    ],
    'show_sidebar': True,
    # "show_ui_builder": True,
    'navigation_expanded': True,
    'order_with_respect_to': ['backend'],
    'hide_models': ['backend.configuration'],
    'custom_css': 'backend/styling/css/admin.css',
    'custom_js' : 'backend/scripting/admin.js',
    'custom_jss': [],
    "custom_links": {
        "backend": backend_menu,
    },
    'icons': {
        'auth': 'fa fa-users-cog',
        'auth.group': 'fa fa-users',
        USER_MODEL: 'fa fa-user',
        'frontend.configuration': 'fa fa-cog',
        'frontend.post': 'fa fa-bullhorn',
        'frontend.media': 'fa fa-file',
        'frontend.category': 'fa fa-list-alt',
        'frontend.navbar': 'fa fa-bars',
        'frontend.slideshow': 'fa fa-image',
    },
    'default_icon_parents': 'fa fa-angle-double-right',
    'default_icon_children': 'fa fa-angle-double-right',
    'changeform_format': 'horizontal_tabs', #single #horizontal_tabs #collapsible #carousel #vertical_tabs
    'changeform_format_overrides': {
        USER_MODEL: 'horizontal_tabs',
        'auth.group': 'vertical_tabs',
    },
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": True,
    "brand_small_text": True,
    "brand_colour": "navbar-primary text-light",
    "accent": "accent-primary",
    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": True,
    "theme": "yeti",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": True
}