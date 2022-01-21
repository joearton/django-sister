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
        profil_pt = sister_api.get_referensi_profil_pt()
        unit_kerja = sister_api.get_referensi_unit_kerja(id_perguruan_tinggi=profil_pt.data.get('id_perguruan_tinggi'))
        sdm = sister_api.get_referensi_sdm()
        pendidikan_s2, pendidikan_s3 = 0, 0
        for index in sdm.data:
            pendidikan_formal = sister_api.get_pendidikan_formal(id_sdm=index['id_sdm'])
            print(pendidikan_formal.data)
            for pendidikan in pendidikan_formal.data:
                if 'jenjang_pendidikan' in pendidikan:
                    if pendidikan['jenjang_pendidikan'] == 'S2':
                        pendidikan_s2 += 1
                    elif pendidikan['jenjang_pendidikan'] == 'S3':
                        pendidikan_s3 += 1
        profil_pt.get('data')['unit_kerja'] = unit_kerja.data
        profil_pt.get('data')['sdm'] = sdm.data
        profil_pt.get('data')['pendidikan_s2'] = pendidikan_s2
        profil_pt.get('data')['pendidikan_s3'] = pendidikan_s3
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
