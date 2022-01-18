from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


def get_current_domain(request, target=''):
    scheme  = request.is_secure() and "https" or "http"
    domain  = get_current_site(request).domain
    address = "{0}://{1}{2}".format(scheme, domain, target)
    return address


def get_media_address(request, target=''):
    address = "{1}{2}{3}".format(get_current_domain(request), settings.MEDIA_URL, target)
    return address


def get_static_address(request, target=''):
    address = "{1}{2}{3}".format(get_current_domain(request), settings.STATIC_URL, target)
    return address
