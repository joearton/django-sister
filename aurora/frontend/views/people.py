from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext as _
from aurora.frontend.models import Post
from aurora.frontend.views import frontendView
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from aurora.backend.library import site
from aurora.sister.models import Unit, SDM
from aurora.backend.vendors.sister import sister
from django.utils.text import slugify
from django.conf import settings
import os


sister_api = sister.SisterAPI()

'''
sdms = sister_api.get_referensi_sdm()
for index in sdms.data:
    unit = Unit.objects.get(unit_id=index['id_sms'])
    try:
        sdm  = SDM.objects.get_or_create(
            id_sdm = index['id_sdm'],
            nama_sdm = index['nama_sdm'],
            slugname = slugify(index['nama_sdm']),
            nidn = index['nidn'],
            nip = index['nip'],
            jenis_sdm = index['jenis_sdm'],
            unit = unit,
        )
    except:
        print(index['nama_sdm'])
'''
    

class PeopleLV(frontendView, ListView):
    section_title = _('People')
    template_name = 'frontend/sections/people.html'
    fluid_width = True
    model = SDM
    paginate_by = 15
    
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        unit_id = self.request.GET.get('unit')
        if unit_id:
            unit = Unit.objects.get(unit_id=unit_id)
            context_data['unit'] = unit
        return context_data
    
    def get_queryset(self):
        qs = self.model.objects.filter(status=SDM.ACTIVE)
        unit_id = self.request.GET.get('unit')
        if unit_id:
            qs = qs.filter(unit__unit_id=unit_id)
        return qs



def peoplePicture(request, slugname):
    sdm = get_object_or_404(SDM, slugname=slugname)
    if not os.path.isfile(sdm.metadata.get('picture_file')):
        foto    = sister_api.get_data_pribadi_foto_bypath(id_sdm=str(sdm.id_sdm))
        ct_foto = foto.get('content-type')
        if ct_foto in ['image/jpeg', 'image/bmp', 'image/gif', 'image/png', 'image/webp']:
            image, ext  = ct_foto.split('/')
            picture_dir = os.path.join(settings.MEDIA_ROOT, 'SDM', 'pictures')
            if not os.path.exists(picture_dir):
                os.makedirs(picture_dir)
            picture_name = f'{sdm.id_sdm}.{ext}'
            picture_file = os.path.join(picture_dir, picture_name)
            with open(picture_file, 'wb') as writer:
                writer.write(foto.get('data'))
            sdm.metadata['picture_file'] = picture_file
            sdm.metadata['picture_url']  = f'{settings.MEDIA_URL}SDM/pictures/{picture_name}'
            sdm.save()
    return HttpResponse(sdm.metadata['picture_url'])
        


class PeopleDV(frontendView, DetailView):
    section_title = _('People Detail')
    template_name = 'frontend/sections/people_detail.html'
    fluid_width = True
    model = SDM
    
    def get_context_data(self, *args, **kwargs):
        obj    = self.get_object()
        id_sdm = str(obj.id_sdm)
        smt     = sister_api.get_referensi_semester()
        context_data = super().get_context_data(*args, **kwargs)
        context_data['profil']     = sister_api.get_data_pribadi_profil_bypath(id_sdm=id_sdm)
        context_data['alamat']     = sister_api.get_data_pribadi_alamat_bypath(id_sdm=id_sdm)
        context_data['lain']       = sister_api.get_data_pribadi_lain_bypath(id_sdm=id_sdm)
        context_data['ilmu']       = sister_api.get_data_pribadi_bidang_ilmu_bypath(id_sdm=id_sdm)
        context_data['pendidikan'] = sister_api.get_pendidikan_formal(id_sdm=id_sdm)
        context_data['jabfung']    = sister_api.get_jabatan_fungsional(id_sdm=id_sdm)
        context_data['pangkat']    = sister_api.get_kepangkatan(id_sdm=id_sdm)
        context_data['penugasan']  = sister_api.get_penugasan(id_sdm=id_sdm)
        context_data['smt_akhir']  = smt.data[1]
        context_data['pengajaran'] = sister_api.get_pengajaran(id_sdm=id_sdm)
        context_data['penelitian'] = sister_api.get_penelitian(id_sdm=id_sdm)
        context_data['abdimas']    = sister_api.get_pengabdian(id_sdm=id_sdm)
        context_data['publikasi']  = sister_api.get_publikasi(id_sdm=id_sdm)
        context_data['ki']         = sister_api.get_kekayaan_intelektual(id_sdm=id_sdm)
        return context_data

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, slugname=self.kwargs.get('slugname'))
        return obj
