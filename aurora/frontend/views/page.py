from django.contrib import messages
from django.utils.translation import gettext as _
from aurora.frontend.views import frontendView
from django.views.generic import TemplateView


class ContactPage(frontendView, TemplateView):
    section_title = _('Contact')
    fluid_width = True
    template_name = 'frontend/sections/contact.html'


class AboutPage(frontendView, TemplateView):
    section_title = _('About')
    fluid_width = True
    template_name = 'frontend/sections/about.html'
