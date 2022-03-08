from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext as _
from aurora.frontend.models import Post
from aurora.frontend.views import frontendView
from django.shortcuts import get_object_or_404
from aurora.backend.library import site
from django.utils.html import strip_tags
from aurora.backend.vendors.sister import sister


sister_api = sister.SisterAPI()

class DirectoryLV(frontendView, TemplateView):
    section_title = _('Directory')
    template_name = 'frontend/sections/directory.html'
    fluid_width = True
    
    
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        profil_pt  = sister_api.get_referensi_profil_pt()
        unit_kerja = sister_api.get_referensi_unit_kerja(
            id_perguruan_tinggi=profil_pt.data.get('id_perguruan_tinggi'))
        context_data['faculties']   = [x for x in unit_kerja['data'] if x['id_jenis_unit'] == 1]
        context_data['departments'] = [x for x in unit_kerja['data'] if x['id_jenis_unit'] == 3]
        return context_data
        