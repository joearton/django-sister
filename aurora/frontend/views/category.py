from django.views.generic import View, ListView
from django.urls import reverse_lazy
from aurora.frontend.models import Slideshow, Post, Category
from aurora.frontend.views import frontendView
from django.utils.translation import gettext as _


class CategoryLV(frontendView, ListView):
    section_title = _('Category')
    template_name = "frontend/sections/homepage.html"
    model = Post
    paginate_by = 11

    def get_section_title(self):
        category = Category.objects.get(slugname = self.kwargs['category'])
        return category.name

    def get_queryset(self):
        category = Category.objects.get(slugname = self.kwargs['category'])
        return self.model.objects.filter(genre = 'post', category=category)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['slideshow_desktop'] = Slideshow.objects.filter(mobile = False).order_by('id')
        context_data['slideshow_mobile'] = Slideshow.objects.filter(mobile = True).order_by('id')
        return context_data
