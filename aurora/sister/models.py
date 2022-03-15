from operator import mod
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from aurora.backend.models import BaseModel, User, BaseModel
from django.utils.text import slugify
import os


class University(BaseModel):
    id_pt = models.UUIDField(_('ID PT'), editable=False, unique=True)
    kode = models.CharField(_('Kode'), max_length=16)
    nama = models.CharField(_('Nama'), max_length=128)
    telepon = models.CharField(_('Telepon'), max_length=128, null=True, blank=True)
    faximile = models.CharField(_('Faximile'), max_length=128, null=True, blank=True)
    email = models.CharField(_('E-mail'), max_length=65, null=True, blank=True)
    website = models.CharField(_('Website'), max_length=64, null=True, blank=True)
    jalan = models.CharField(_('Jalan'), max_length=128, null=True, blank=True)
    dusun = models.CharField(_('Dusun'), max_length=128, null=True, blank=True)
    rt = models.IntegerField(_('RT'), null=True, blank=True)
    rw = models.IntegerField(_('RW'), null=True, blank=True)
    kelurahan = models.CharField(_('Kelurahan'), max_length=128, null=True, blank=True)
    kode_pos = models.CharField(_('Kode Pos'), max_length=16, null=True, blank=True)
    nama_wilayah = models.CharField(_('Nama Wilayah'), max_length=128, null=True, blank=True)
    sk_pendirian = models.CharField(_('SK Pendirian'), max_length=128, null=True, blank=True)
    tanggal_sk = models.CharField(_('Tanggal SK Pendirian'), max_length=128, null=True, blank=True)
    status = models.CharField(_('Status'), max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = _('University')
        verbose_name_plural = _('Universities')

    def __str__(self):
        return self.nama
    

class Unit(BaseModel):
    unit_id = models.UUIDField(_('Unit'), editable=False)
    nama = models.CharField(_('Nama'), max_length=128)
    jenis = models.IntegerField(_('Jenis'))
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Unit')
        ordering = ['jenis']

    def __str__(self):
        return self.nama



class SDM(BaseModel):
    ACTIVE   = 1
    INACTIVE = 0
    CHOICES_STATUS = [
        [ACTIVE, _('Active')],
        [INACTIVE, _('Inactive')]
    ]
    id_sdm = models.UUIDField(_('ID SDM'), editable=False)
    nama_sdm = models.CharField(_('Nama SDM'), max_length=128)
    slugname = models.SlugField(_('ID Unik'), max_length=128, unique=True)
    nidn = models.CharField(_('NIDN'), max_length=16, null=True, blank=True, unique=True)
    nip = models.CharField(_('NIP'), max_length=28, null=True, blank=True)
    jenis_sdm = models.CharField(_('Jenis SDM'), max_length=16, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='people')
    metadata = models.JSONField(_('Metadata'), null=True, blank=True, default=dict)
    status = models.IntegerField(_('Status'), default=1, choices=CHOICES_STATUS)

    class Meta:
        verbose_name = _('SDM')
        verbose_name_plural = _('SDM')
        ordering = ['nama_sdm']

    def __str__(self):
        return self.nama_sdm
    
    

