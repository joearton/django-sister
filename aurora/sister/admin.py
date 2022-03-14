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


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1


@admin.register(Unit)
class UnitAdmin(backendAdmin):
    list_display  = ['nama', 'jenis', 'parent', 'subunit']
    list_editable = ['jenis', 'parent']
    inlines = [UnitInline]
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    @admin.display(description=_('SubUnit'))
    def subunit(self, obj):
        return obj.children.count()
    

@admin.register(SDM)
class SDMAdmin(backendAdmin):
    list_display  = ['nama_sdm', 'nidn', 'jenis_sdm', 'unit', 'status']
    list_editable = ['unit', 'status']
