from multiprocessing import context
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext as _
from aurora.frontend.views import frontendView
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from aurora.backend.library import site
from aurora.sister.models import Unit, SDM
from django.utils.text import slugify
from aurora.backend.library.site import get_current_domain
from django.db.models import Q
from django.conf import settings
from urllib.parse import urlparse, urlencode
from weasyprint import HTML
from aurora.backend.vendors.sister.sister import SisterAPI as sister_api
from aurora.backend.vendors.sister.library.template import SisterTemplate
from urllib.parse import urlparse, parse_qs
import os


st = SisterTemplate()
    

class PeopleLV(frontendView, ListView):
    section_title = _('People')
    template_name = 'frontend/sections/people.html'
    fluid_width = True
    model = SDM
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        unit_id = self.request.GET.get('unit')
        if unit_id:
            unit = Unit.objects.get(unit_id=unit_id)
            context_data['unit'] = unit
        keyword = self.request.GET.get('keyword')
        if keyword:
            context_data['keyword'] = keyword
        view = self.request.GET.get('view')
        if view:
            context_data['view'] = view
        return context_data
    
    def get_queryset(self):
        qs = self.model.objects.filter(status=SDM.ACTIVE)
        unit_id = self.request.GET.get('unit')
        if unit_id:
            qs = qs.filter(
                unit__unit_id=unit_id
            )
        keyword = self.request.GET.get('keyword')
        if keyword:
            qs = qs.filter(
                Q(nama_sdm__icontains=keyword) |
                Q(nidn__icontains=keyword)
            )
        for q in qs:
            accessed_at_iso = q.metadata.get('accessed_at_iso')
            if accessed_at_iso:
                q.accessed_at = st.iso_to_datetime(accessed_at_iso)
            expired_at_iso = q.metadata.get('expired_at_iso')
            if expired_at_iso:
                q.expired_at = st.iso_to_datetime(expired_at_iso)
        return qs


def set_context_data(sdm, context_data={}):
    id_sdm = str(sdm.id_sdm)
    smt    = sister_api.get_referensi_semester()
    profil = sister_api.get_data_pribadi_profil_bypath(id_sdm=id_sdm)
    context_data['profil']      = profil
    context_data['alamat']      = sister_api.get_data_pribadi_alamat_bypath(id_sdm=id_sdm)
    context_data['lain']        = sister_api.get_data_pribadi_lain_bypath(id_sdm=id_sdm)
    context_data['ilmu']        = sister_api.get_data_pribadi_bidang_ilmu_bypath(id_sdm=id_sdm)
    context_data['pendidikan']  = sister_api.get_pendidikan_formal(id_sdm=id_sdm)
    context_data['jabfung']     = sister_api.get_jabatan_fungsional(id_sdm=id_sdm)
    context_data['pangkat']     = sister_api.get_kepangkatan(id_sdm=id_sdm)
    context_data['penugasan']   = sister_api.get_penugasan(id_sdm=id_sdm)
    context_data['smt_akhir']   = smt.data[1]
    context_data['pengajaran']  = sister_api.get_pengajaran(id_sdm=id_sdm)
    context_data['penelitian']  = sister_api.get_penelitian(id_sdm=id_sdm)
    context_data['abdimas']     = sister_api.get_pengabdian(id_sdm=id_sdm)
    context_data['publikasi']   = sister_api.get_publikasi(id_sdm=id_sdm)
    context_data['ki']          = sister_api.get_kekayaan_intelektual(id_sdm=id_sdm)
    context_data['penghargaan'] = sister_api.get_penghargaan(id_sdm=id_sdm)
    # check attribute/metadata of response
    sdm.metadata['cache']       = profil.get('cache')
    sdm.metadata['accessed_at_iso'] = profil.get('accessed_at_iso')
    sdm.metadata['expired_at_iso']  = profil.get('expired_at_iso')
    sdm.save()
    return context_data


class PeopleDV(frontendView, DetailView):
    section_title = _('People Detail')
    template_name = 'frontend/sections/people_detail.html'
    fluid_width = True
    model = SDM
    
    
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data()
        context_data = set_context_data(self.obj, context_data)
        return context_data


    def save_people_picture(self, sdm):
        picture = sister_api.get_data_pribadi_foto_bypath(id_sdm=str(sdm.id_sdm))
        ct_pic  = picture.get('content-type')
        if picture.get('data') and ct_pic in ['image/jpeg', 'image/bmp', 'image/gif', 'image/png', 'image/webp']:
            image, ext  = ct_pic.split('/')
            picture_dir = os.path.join(settings.MEDIA_ROOT, 'people', 'pictures')
            if not os.path.exists(picture_dir):
                os.makedirs(picture_dir)
            picture_name = f'{sdm.id_sdm}.{ext}'
            picture_file = os.path.join(picture_dir, picture_name)
            with open(picture_file, 'wb') as writer:
                writer.write(picture.get('data'))
            sdm.metadata['picture_file'] = picture_file
            sdm.metadata['picture_url']  = f'{settings.MEDIA_URL}people/pictures/{picture_name}'
            sdm.metadata['picture_accessed_at_iso'] = picture['accessed_at_iso']
            sdm.metadata['picture_expired_at_iso']  = picture['expired_at_iso']
        return sdm
            

    def get_people_picture(self, sdm):
        # create default picture file and url
        if not sdm.metadata.get('picture_file'):
            sdm.metadata['picture_file'] = os.sep
        if not sdm.metadata.get('picture_url'):
            sdm.metadata['picture_url']  = settings.MEDIA_URL
        sdm.save()
        if not os.path.isfile(sdm.metadata.get('picture_file')):
            sdm = self.save_people_picture(sdm)
            sdm.save()
        picture_expired = sdm.metadata.get('picture_expired_at_iso')
        if picture_expired:
            picture_expired = st.iso_to_datetime(picture_expired)
            if st.get_now_datetime() > picture_expired:
                self.save_people_picture(sdm)
        return sdm.metadata['picture_url']

    
    def get_viewer_info(self, obj):
        # get viewers count information
        viewers = obj.metadata.get('viewers')
        if not viewers:
            obj.metadata['viewers'] = 0
        obj.metadata['viewers'] += 1

        # get referer information
        if not obj.metadata.get('referers'):
            obj.metadata['referers'] = []
        referer = self.request.headers.get('Referer')
        if len(obj.metadata['referers']) > 10: # limit referer
            referers = []
            for counter in range(10):
                referers.append(obj.metadata['referer'][counter])
            obj.metadata['referers'] = referers
        if referer:
            referer = urlparse(referer)
            netloc  = referer.netloc.lower()
            if not netloc in ['localhost:8000']:
                if not netloc in obj.metadata['referers']:
                    obj.metadata['referers'].append(netloc)
        obj.save()
            
                
    def dispatch(self, request, *args, **kwargs):
        self.obj = get_object_or_404(self.model, slugname=self.kwargs.get('slugname'))
        # get viewers, referer, and etc
        self.get_people_picture(self.obj)
        self.get_viewer_info(self.obj)
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_section_title(self):
        obj = self.obj
        return obj.nama_sdm
    
    def get_object(self, queryset=None):
        return self.obj


class CvDownload(frontendView):
    section_title = _('People Detail')
    template_name = 'frontend/sections/people_cv.html'
    model = SDM

    def response_pdf(self, request, report, title):
        pdf_file = HTML(string = report, base_url = get_current_domain(self.request))
        response = HttpResponse(pdf_file.write_pdf(), content_type='application/pdf')
        response['Host'] = get_current_domain(self.request)
        response['Content-Disposition'] = 'inline;filename="{0}-{1}.pdf"'.format(_("CV"), title)
        response['Content-Transfer-Encoding'] = 'binary'
        return response

    def get(self, request, *arg, **kwargs):
        site_url = get_current_domain(request)
        if settings.DEBUG:
            site_url = "http://localhost:8000"
        if not site_url.startswith("http"):
            site_url = settings.HOST_PROTOCOL + site_url
        obj = get_object_or_404(self.model, id_sdm=self.kwargs.get('id_sdm'))
        context_data = set_context_data(obj)
        context_data['site_url'] = site_url
        context_data['object']   = obj
        report = render_to_string(self.template_name, context_data)
        # return render(request, self.template_name, context_data)
        return self.response_pdf(request, report, obj.nama_sdm)

