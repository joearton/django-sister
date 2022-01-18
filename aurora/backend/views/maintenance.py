from django.contrib import messages
from django.http import Http404
from django.views.generic import TemplateView
from aurora.backend.views import BaseView
from django.conf import settings


class MaintenanceView(BaseView, TemplateView):
    template_name = 'backend/sections/maintenance.html'

    def dispatch(self, request, *args, **kwargs):
        if not settings.MAINTENANCE:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['maintenance_message'] = settings.MAINTENANCE_MESSAGE
        return context_data
