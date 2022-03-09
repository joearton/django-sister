from django.contrib import admin, messages
from django.contrib.admin.decorators import display
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
from aurora.frontend.models import *
from aurora.backend.admin import backendAdmin
from aurora.sister.models import Unit, SDM
from aurora.backend.library.site import get_current_domain


@admin.register(Unit)
class UnitAdmin(backendAdmin):
    pass


@admin.register(SDM)
class SDMAdmin(backendAdmin):
    list_display  = ['nama_sdm', 'nidn', 'jenis_sdm', 'unit']
    list_editable = ['unit',]
