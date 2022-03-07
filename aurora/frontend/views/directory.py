from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext as _
from aurora.frontend.models import Post
from aurora.frontend.views import frontendView
from django.shortcuts import get_object_or_404
from aurora.backend.library import site
from django.utils.html import strip_tags


class DirectoryLV(frontendView):
    section_title = _('Posts')
    template_name = 'frontend/sections/posts.html'
    fluid_width = True
    paginate_by = 10