from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext as _
from aurora.frontend.models import Post
from aurora.frontend.views import frontendView
from django.shortcuts import get_object_or_404
from aurora.backend.library import site
from aurora.sister.models import Unit, SDM
from aurora.backend.vendors.sister import sister
from django.utils.text import slugify


sister_api = sister.SisterAPI()

class PeopleLV(frontendView, ListView):
    section_title = _('People')
    template_name = 'frontend/sections/people.html'
    fluid_width = True
    model = SDM
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data
        