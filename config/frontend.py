from django.utils.translation import gettext_lazy as _


FRONTEND_SETTINGS = {
    'bootstrap_theme'   : 'default', # 
    'theme_mode'        : 'dark', # light or dark
    'theme_accent'      : 'softgreen', # army, ubuntu, deep, blue, softblue, softgreen, green, elegant
    'topbar'            : {
        'background'    : 'black',
        'align'         : 'center',
        'transparent'   : '',
        'integrated'    : True,
    },
    'logo_width'        : '250px',
    'navbar'            : {
        'container'     : 'container',
        'align'         : 'center',
        'transparent'   : '',
        'position'      : 'sticky-top',
        'uppercase'     : True,
        'icon'          : True,
    },
    'jumbotron'         : {
        'overlay_bg'    : 'rgba(0,0,0,.45)',
        'color'         : 'white',
        'align'         : 'center',
        'padding'       : '21vh 0px 45vh 0px',
        'title_class'   : 'h1 m-0',
        'subtitle_class': 'p',
        'buttons'       : [
            {
                'label' : _('Getting Started'),
                'url'   : '#',
                'class' : 'btn-success btn-lg',
                'icon'  : 'fa fa-play'
            },
            {
                'label' : _('Register Now'),
                'url'   : '#',
                'class' : 'btn-primary btn-lg',
                'icon'  : 'fa fa-user'
            },
        ]
    },
    'post'              : {
        'container'     : 'container',
        'visible'       : True,
        'featured_post' : True,
        'layout'        : 'list',
        'max'           : 4,
    },
    'footer'            : {
        'container'     : 'container',
        'align'         : 'center',
        'transparent'   : '',
    }
}