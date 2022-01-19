from django.views.generic import View, ListView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from aurora.frontend.models import Slideshow, Post, Configuration
from aurora.frontend.views import frontendView
from django.utils.translation import gettext as _
from aurora.backend.vendors.sister import sister
from random import choice

sister_api = sister.SisterAPI()


class FrontendDefault(frontendView, ListView):
    section_title = _('Welcome')
    template_name = "frontend/sections/homepage.html"
    model = Post
    paginate_by = 4
    fluid_width = True


    def get_university_info(self):
        profil_pt  = sister_api.get_referensi_profil_pt()
        unit_kerja = sister_api.get_referensi_unit_kerja(id_perguruan_tinggi=profil_pt.get('data').get('id_perguruan_tinggi'))
        pegawai    = sister_api.get_referensi_sdm()
        profil_pt.get('data')['unit_kerja'] = unit_kerja.get('data')
        profil_pt.get('data')['sdm'] = pegawai.get('data')
        return profil_pt


    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        try:
            configuration = Configuration.objects.get(site = self.request.site)
        except Configuration.DoesNotExist:
            configuration = None
        if configuration:
            context_data['slideshow_desktop'] = Slideshow.objects.filter(
                site = self.request.site,
                mobile = False).order_by('date_created')
            context_data['slideshow_mobile'] = Slideshow.objects.filter(
                site = self.request.site,
                mobile = True).order_by('date_created')
        context_data['university_info'] = self.get_university_info()
        return context_data
