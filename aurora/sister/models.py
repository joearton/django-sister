from operator import mod
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from aurora.backend.models import BaseModel, User, BaseModel
from django.utils.text import slugify
import os


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
    
    

