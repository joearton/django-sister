from django.views.generic import View, TemplateView, CreateView
from django.urls import reverse_lazy
from aurora.backend.views import coreView
from django.utils.translation import gettext as _



class DefaultView(coreView, TemplateView):
    section_title = _('Panel Administrasi')
    section_name = 'panel-default'
    template_name = "backend/sections/backend/default.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data
