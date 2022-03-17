import imp
from django.db.utils import OperationalError
from django.forms.models import model_to_dict
from aurora.frontend.models import Navbar, Sidebar, Configuration
from aurora.backend.vendors.sister.library import io


def get_sister_config():
    sister_io = io.SisterIO()
    config    = sister_io.read_config()
    return config    

def get_context_navbar(request):
    navbar_items = Navbar.objects.filter(site=request.site)
    navbar_dict = {}
    new_navbar_dict = {}
    for item in navbar_items:
        navbar_item = {
            'title': item.title, 'url': item.url,
            'icon': item.icon, 'childern': [], 'parent': None,
        }
        key = 'item-{0}'.format(item.id)
        if item.parent:
            navbar_item['parent'] = 'item-{0}'.format(item.parent.id)
            navbar_dict[key] = navbar_item
        else:
            new_navbar_dict[key] = navbar_item
    for key, value in navbar_dict.items():
        new_navbar_dict[value['parent']]['childern'].append(value)
    return new_navbar_dict


def get_sidebar(request):
    sidebar = Sidebar.objects.filter(site=request.site)
    return sidebar


def contextual(request):
    '''
        meload context processor di setiap aplikasi
    '''
    try:
        frontend_config = Configuration.objects.get(site=request.site)
        frontend_config = model_to_dict(frontend_config)
    except Configuration.DoesNotExist or OperationalError:
        frontend_config = {}
    frontend_config['navbar']  = get_context_navbar(request)
    frontend_config['sidebar'] = get_sidebar(request)
    context_proccessor = {
        'f_config': frontend_config,
        'sister_config': get_sister_config()
    }
    return context_proccessor
