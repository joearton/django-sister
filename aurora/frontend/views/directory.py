from django import dispatch
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext as _
from aurora.frontend.models import Post
from aurora.frontend.views import frontendView
from django.shortcuts import get_object_or_404
from aurora.backend.library import site
from aurora.sister.models import Unit, SDM
from aurora.backend.vendors.sister.sister import SisterAPI as sister_api



class DirectoryLV(frontendView, ListView):
    section_title = _('University Directory')
    template_name = 'frontend/sections/directory.html'
    fluid_width = True
    model = Unit
    paginate_by = 15
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(jenis=3)
        return qs
    
    def dispatch(self, request, *args, **kwargs):
        profil_pt  = sister_api.get_referensi_profil_pt()
        unit_kerja = sister_api.get_referensi_unit_kerja(
            id_perguruan_tinggi=profil_pt.data.get('id_perguruan_tinggi'))
        for index in unit_kerja.data:
            if not Unit.objects.filter(unit_id=index.get('id')).exists():
                unit = Unit.objects.create(
                    unit_id=index.get('id'),
                    nama=index.get('nama'),
                    jenis=index.get('id_jenis_unit')
                )
        return super().dispatch(request, *args, **kwargs)
        