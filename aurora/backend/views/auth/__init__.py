from django.http.response import Http404
from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from django.urls.base import reverse
from aurora.backend.views import BaseView
from aurora.backend.models import User
from aurora.backend.library.site import get_client_ip
from django.utils.translation import gettext as _
from django.conf import settings
from aurora.backend.environment import backendEnvironment
from django.conf import settings


class DefaultDashboardView:

    def set_default_role(self, request, role):
        if request.session.has_key('role'):
            del request.session['role']
        if request.user.groups.filter(name=role).exists():
            user = User.objects.get(pk=request.user.pk)
            request.session['role'] = role
            if role == 'participant' and request.user.is_staff:
                user.is_staff = False
            if role in ['admin', 'reviewer', 'accountant'] and not request.user.is_staff:
                user.is_staff = True
            user.save()


    def go_to_dashboard(self, request, url_only=False):
        action = redirect
        if url_only:
            action = reverse
        # if user admin, redirect to Django Admin Panel
        if request.user.is_superuser:
            return action('admin:index')
        if not request.session.has_key('role'):
            return action('aurora.backend.account')
        role = request.session.get('role')
        if request.user.groups.filter(name=role).exists():
            if role == 'participant':
                return action(backendEnvironment.backend['dashboard_url'])
            if role in ['admin', 'reviewer', 'accountant']:
                return action('admin:index')
        


class AuthView(BaseView, DefaultDashboardView):
    section_name = 'auth'
    auth_info = settings.BACKEND_SETTINGS['auth_info']
    auth_help = None

    def dispatch(self, request, *args, **kwargs):
        # record client info for security purpose
        user_agent = request.META.get('HTTP_USER_AGENT')
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            if user_agent:
                user.property.browser = user_agent
                user.property.device = user_agent
            user.property.ip = get_client_ip(request)
            user.property.save()
        return super().dispatch(request, *args, **kwargs)
    

    def get_auth_info(self):
        return self.auth_info

    def get_auth_help(self):
        return self.auth_help

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['auth_info'] = self.get_auth_info()
        context_data['auth_help'] = self.get_auth_help()
        return context_data

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.add_message(self.request, messages.INFO, _('You are signed in...'))
            return self.go_to_dashboard(self.request)
        return super().get(*args, **kwargs)


