from django.http import JsonResponse
from django.http import Http404
from django.utils.translation import gettext as _
from aurora.backend.views import BaseView
from django.conf import settings
import json
import os
import importlib


AJAX_DIR = os.path.join(settings.CACHE_DIR, 'ajax')
if not os.path.exists(AJAX_DIR):
    os.makedirs(AJAX_DIR)



class AjaxHandler:

    response = {'status': False, 'data': None, 'messages': '', 'error_code': False}

    def __init__(self):
        self.handlers = {}
        self.scopes = {}

    def dispatch(self, request, *args, **kwargs):
        # for security, avoid direct access to autocomplete
        if not 'Sec-Fetch-Site' in request.headers:
            raise Http404()
        sfs = request.headers.get('Sec-Fetch-Site')
        if not sfs == 'same-origin':
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


    def handler(self, func):
        func_name = func.__name__
        if not func_name in self.handlers:
            self.handlers[func_name] = func
        else:
            raise ValueError(_('The same handler has been activated'))
        return self.handlers


    def post(self, request, **kwargs):
        if request.method == "POST" and request.is_ajax():
            name  = request.POST.get('name')
            value = request.POST.get('value')
            if name in self.handlers:
                self.response = self.handlers[name](request, self.response, value)
            else:
                self.response['error_code'] = '404' # no handler
                self.response['message'] = _('No handler registered')
        return JsonResponse(self.response)


    def as_view(self):
        return self.post
