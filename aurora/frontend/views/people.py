from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext as _
from aurora.frontend.models import Post
from aurora.frontend.views import frontendView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
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
    
    def get_queryset(self):
        qs = self.model.objects.filter(status=SDM.ACTIVE)
        return qs


def peoplePicture(request, slugname):
    sdm  = get_object_or_404(SDM, slugname=slugname)
    foto = sister_api.get_data_pribadi_foto_bypath(id_sdm=str(sdm.id_sdm))
    return HttpResponse(foto['data'], content_type="image/jpeg")


class PeopleDV(frontendView, DetailView):
    section_title = _('People Detail')
    template_name = 'frontend/sections/people_detail.html'
    fluid_width = True
    model = SDM
    
    def get_context_data(self, *args, **kwargs):
        obj = self.get_object()
        context_data = super().get_context_data(*args, **kwargs)
        context_data['profil'] = sister_api.get_data_pribadi_profil_bypath(id_sdm=str(obj.id_sdm))
        context_data['alamat'] = sister_api.get_data_pribadi_alamat_bypath(id_sdm=str(obj.id_sdm))
        context_data['ilmu']   = sister_api.get_data_pribadi_bidang_ilmu_bypath(id_sdm=str(obj.id_sdm))
        return context_data

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, slugname=self.kwargs.get('slugname'))
        return obj
