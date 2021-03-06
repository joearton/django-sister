import imp
from typing import Iterable
from django.views.generic import View, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.base import TemplateView
from aurora.frontend.models import Slideshow, Post, Configuration
from aurora.frontend.views import frontendView
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.text import slugify
from aurora.sister.models import Unit, SDM, University
from aurora.backend.vendors.sister.sister import SisterAPI as sister_api
from aurora.backend.vendors.sister.library.template import SisterTemplate


st = SisterTemplate()

class FrontendDefault(frontendView, ListView):
    section_title = _('Welcome')
    template_name = "frontend/sections/homepage.html"
    model = Post
    paginate_by = 4
    fluid_width = True


    def fetch_university(self):
        university = sister_api.get_referensi_profil_pt()
        if university.data:
            uni = university.data
            if not University.objects.filter(id_pt=uni['id_perguruan_tinggi']).exists():
                University.objects.create(
                    id_pt=uni['id_perguruan_tinggi'],
                    kode=uni['kode_perguruan_tinggi'],
                    nama=uni['nama_perguruan_tinggi'],
                    telepon=uni['telepon'],
                    faximile=uni['faximile'],
                    email=uni['email'],
                    website=uni['website'],
                    jalan=uni['jalan'],
                    dusun=uni['dusun'],
                    rt=uni['rt'],
                    rw=uni['rw'],
                    kelurahan=uni['kelurahan'],
                    kode_pos=uni['kode_pos'],
                    nama_wilayah=uni['nama_wilayah'],
                    sk_pendirian=uni['sk_pendirian'],
                    tanggal_sk=uni['tanggal_sk_pendirian'],
                    status=uni['status_perguruan_tinggi'],
                )
        return University.objects.all()[0]


    def fetch_units(self, university):
        unit_kerja = sister_api.get_referensi_unit_kerja(id_perguruan_tinggi=str(university.id_pt))
        for unit in unit_kerja.data:
            # fix unit name sent by web service
            nama = unit['nama']
            if nama.lower().find('program studi') != -1:
                nama = nama.replace('Program Studi', '')
            if nama.lower().find('fakultas') != -1:
                nama  = nama.replace('Fakultas', '')
                nama  = "Fakultas" + nama

            if not Unit.objects.filter(unit_id=unit['id']).exists():
                Unit.objects.create(
                    unit_id=unit['id'],
                    nama=nama,
                    jenis=unit['id_jenis_unit']
                )
            else:
                unit_obj = Unit.objects.get(unit_id=unit['id'])
                unit_obj.unit_id = unit['id']
                unit_obj.nama = nama
                unit_obj.jenis = unit['id_jenis_unit']
                unit_obj.save()
        units = Unit.objects.all()
        return units


    def fetch_people(self):           
        people = sister_api.get_referensi_sdm()
        for sdm in people.data:
            unit = Unit.objects.get(unit_id=sdm['id_sms'])
            if not SDM.objects.filter(id_sdm=sdm['id_sdm']).exists():
                SDM.objects.create(
                    id_sdm=sdm['id_sdm'],
                    nama_sdm=sdm['nama_sdm'],
                    slugname=slugify(sdm['nama_sdm']),
                    nidn=sdm['nidn'],
                    nip=sdm['nip'],
                    jenis_sdm=sdm['jenis_sdm'],
                    unit=unit
                )
            else:
                person = SDM.objects.get(id_sdm=sdm['id_sdm'])
                person.nama_sdm = sdm['nama_sdm']
                person.slugname = slugify(sdm['nama_sdm'])
                person.nidn = sdm['nidn']
                person.nip = sdm['nip']
                person.jenis_sdm =sdm['jenis_sdm']
                unit = unit
                person.save()
        return SDM.objects.all()
                        

    def get_university_info(self):
        university = University.objects.all()
        if not university:
           university = self.fetch_university()
        else:
            university   = university[0]
            expired_univ = st.get_expired_datetime(university.date_modified, days=7)
            if st.get_now_datetime() > expired_univ:
                university = self.fetch_university()

        units = Unit.objects.all()
        if  units:
            units = self.fetch_units(university)
        else:
            expired_units = st.get_expired_datetime(units[0].date_modified, days=7)
            if st.get_now_datetime() > expired_units:
                units = self.fetch_units(university)

        people = SDM.objects.all()
        if not people:
            people = self.fetch_people()
        else:
            expired_people = st.get_expired_datetime(people[0].date_modified, days=7)
            if st.get_now_datetime() > expired_people:
                people = self.fetch_people()
        return [university, units, people]


    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        try:
            configuration = Configuration.objects.get(site = self.request.site)
        except Configuration.DoesNotExist:
            configuration = None
        if configuration:
            context_data['slideshow_desktop'] = Slideshow.objects.filter(
                site = self.request.site, mobile = False).order_by('date_created')
            context_data['slideshow_mobile'] = Slideshow.objects.filter(
                site = self.request.site, mobile = True).order_by('date_created')
        if sister_api.check_config():
            [university, units, people] = self.get_university_info()
            context_data['university']  = university
            context_data['units']  = units
            context_data['people'] = people
        else:
            messages.warning(self.request, _("Sister server can't be reached"))
        return context_data
