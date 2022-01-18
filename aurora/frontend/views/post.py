from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext as _
from aurora.frontend.models import Post
from aurora.frontend.views import frontendView
from django.shortcuts import get_object_or_404
from aurora.backend.library import site
from django.utils.html import strip_tags


class PostLV(frontendView, ListView):
    model = Post
    section_title = _('Posts')
    template_name = 'frontend/sections/posts.html'
    fluid_width = True
    paginate_by = 10


class PostDetailView(frontendView, DetailView):
    model = Post
    section_title = _('Post')
    template_name = 'frontend/sections/post.html'
    fluid_width = True

    def get_section_title(self):
        current_object = self.get_object()
        return current_object.title

    def get_object(self):
        return get_object_or_404(self.model, slugname = self.kwargs['slugname'])

    def get_section_headers(self):
        current_object = self.get_object()
        current_url = "{0}{1}".format(site.get_current_domain(self.request), self.request.path)
        opengraph   = "<meta property='og:url' content='{0}' />".format(current_url)
        opengraph  += "<meta property='og:type' content='article' />"
        opengraph  += "<meta property='og:title' content='{0}' />".format(current_object.title)
        opengraph  += "<meta property='og:description' content='{0}' />".format(strip_tags(current_object.content[:95]))
        if current_object.thumbnail:
            thumbnail_url = current_object.thumbnail.url
        else:
            thumbnail_url = '/static/frontend/media/default-post.jpg'
        opengraph += "<meta property='og:image' content='{0}{1}' />\n".format(site.get_current_domain(self.request), thumbnail_url)
        return opengraph

    def get_context_data(self, *args, **kwargs):
        current_object = self.get_object()
        # menyimpan data meta terkait post
        if current_object.meta:
            # menyimpan data jumlah pengunjung
            if 'view_count' in current_object.meta:
                prev_count = current_object.meta['view_count']
                current_object.meta = {'view_count': prev_count + 1}
            else:
                current_object.meta = {'view_count': 1}
        else:
            current_object.meta = {'view_count': 1}
        current_object.save()
        context = super().get_context_data(*args, **kwargs)
        context['section_headers'] = self.get_section_headers()
        context['related_posts'] = self.model.objects.filter(category = current_object.category).exclude(pk = current_object.pk)[:15]
        return context
