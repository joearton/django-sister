from django.urls.base import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html, mark_safe
from aurora.backend.models import Configuration
from aurora.backend.library import forms, service
from aurora.backend.views.auth.activation import shared_activate_user
from django.contrib.admin import AdminSite
from django.views.generic import TemplateView
from aurora.backend.views.admin import forms
from aurora.backend.library import agregator
from aurora.backend.library.ajax import AjaxHandler
from aurora.boot import get_app_list
from django.conf import settings


AjaxHandler = AjaxHandler()


@AjaxHandler.handler
def activate_celery_worker(request, res, value):
    command = 'start' if value else 'stop'
    res = service.toggle_celery_worker(res, command)
    return res
 

@AjaxHandler.handler
def activate_redis_server(request, res, value):
    command = 'start' if value else 'stop'
    res = service.toggle_redis_server(res, command)
    return res


@AjaxHandler.handler
def manage_apps(request, res, value):
    command = 'start' if value else 'stop'
    res = agregator.manage_apps(request, res, command)
    return res


@AjaxHandler.handler
def get_sys_problems(request, res, value):
    celery_worker = service.is_running('celery', True, True)
    redis_server  = service.is_running('redis-server', True, True)
    system_config = all([celery_worker, redis_server])
    res['status'] = True
    res['data'] = system_config
    return res


class ServiceTV(TemplateView):
    template_name = "backend/admin/service_config.html"
    admin_site = None
    section_title = _('Service Configuration')


    def get_sys_info(self):
        return service.get_sys_info()


    def get_context_data(self, **kwargs):
        context_data  = super().get_context_data()
        context_data['title'] = self.section_title
        context_data['sys_info'] = self.get_sys_info()
        context_data['celery_worker'] = service.is_running('celery', True, True)
        context_data['redis_server']  = service.is_running('redis-server', True, True)
        context_data['last_login_users']  = User.objects.all().order_by('-last_login')[:5]
        admin_context_data = dict(self.admin_site.each_context(self.request))
        admin_context_data.update(context_data)
        return admin_context_data


class ApplicationTV(TemplateView):
    template_name = "backend/admin/application_config.html"
    admin_site = None
    section_title = _('Application Configuration')

    def get_context_data(self, **kwargs):
        context_data  = super().get_context_data()
        context_data['title'] = self.section_title
        context_data['applications'] = get_app_list()
        admin_context_data = dict(self.admin_site.each_context(self.request))
        admin_context_data.update(context_data)
        return admin_context_data


@admin.register(Configuration)
class ConfigAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('ajax', self.admin_site.admin_view(AjaxHandler.as_view()), name="backend.ajax"),
            path('service', self.admin_site.admin_view(ServiceTV.as_view(admin_site=self.admin_site)), name="backend.service_config"),
            path('application', self.admin_site.admin_view(ApplicationTV.as_view(admin_site=self.admin_site)), name="backend.application_config"),
        ]
        return my_urls + urls



