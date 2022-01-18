from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings
from django.db.utils import ProgrammingError

def get_site_pk():
    try:
        current_site = Site.objects.get_current()
        if current_site:
            SITE_ID = current_site.pk
    except ProgrammingError:
        SITE_ID = settings.SITE_ID
    return SITE_ID
    

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_current_domain(request, target=''):
    scheme  = request.is_secure() and "https" or "http"
    domain  = get_current_site(request).domain
    address = "{0}://{1}{2}".format(scheme, domain, target)
    return address
