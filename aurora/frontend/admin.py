from os import write
from django.contrib import admin, messages
from django.contrib.admin.decorators import display
from django.utils.text import slugify, Truncator
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, mark_safe, escape
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, reverse
from django import forms
from django.conf import settings
from aurora.frontend.models import *
from aurora.backend.admin import backendAdmin
from aurora.backend.library.validators import readable_filesize
from aurora.backend.library.site import get_current_domain



class NavbarForm(forms.ModelForm):
    class Meta:
        model = Navbar
        widgets = {} 
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        default_urls = [
            ('#', '-----'),
            (reverse('aurora.frontend.post.list'), _('Posts')),
            (reverse('aurora.frontend.contact'), _('Contact')),
            (reverse('aurora.frontend.about'), _('About'))
        ]
        choices = default_urls + self.get_page_urls() + self.get_category_urls()
        self.base_fields['url'] = forms.ChoiceField(choices=choices)
        self.base_fields['url'].initial = '#'
        super().__init__(*args, **kwargs)


    def get_page_urls(self):
        pages = Post.objects.filter(post_type='page')
        page_urls = []
        for page in pages:
            page_url = '{0}'.format(
                reverse('aurora.frontend.post.detail', kwargs={
                    'year': page.publish_date.year,
                    'month': page.publish_date.month,
                    'day': page.publish_date.day,
                    'slugname': page.slugname,
                })
            )
            page_urls.append([page_url, '[Page] {}'.format(page.title)])
        return page_urls


    def get_category_urls(self):
        categories = Category.objects.all()
        category_urls = []
        for category in categories:
            category_url = reverse('aurora.frontend.category.list', kwargs={'category': category.slugname})
            category_urls.append([category_url, '[Category] {}'.format(category.name)])
        return category_urls


class NavbarInline(admin.StackedInline):
    form = NavbarForm
    model = Navbar
    extra = 0


@admin.register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    form = NavbarForm
    search_fields = ['title']
    list_display = ('title', 'order', 'navlink_icon', 'subnavbar')
    list_editable = ('order',)
    inlines = (NavbarInline, )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent=None)

    def navlink_icon(self, obj): 
        if not obj.icon:
            return "-"
        return format_html("<i class='{0}'></i> {0}", obj.icon)
    navlink_icon.short_description = _('Icon')

    def subnavbar(self, obj):
        if obj.navbar_set:
            return obj.navbar_set.count()



@admin.register(Sidebar)
class SidebarAdmin(admin.ModelAdmin):
    pass


@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    def has_module_permission(self, request):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'contents')

    @display(description=_('Contents'))
    def contents(self, obj):
        return obj.post_set.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.exclude(slugname='lain-lain')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'password': forms.PasswordInput()
        }
        fields = '__all__'


@admin.register(Post)
class PostAdmin(backendAdmin):
    form = PostForm
    search_fields = ['title', 'files__name']
    list_display = ('title', 'author', 'publish_date', 'category')
    list_filter = ['category']
    fields = ['title', 'url', 'content', 'thumbnail', 'category', 'files', 'password', 'publish_date', 'site']
    readonly_fields = ['url']
    autocomplete_fields = ['files']
    actions = ["export_as_csv", "unlock_content"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(site=request.site)
        return qs


    def url(self, obj):
        base_url = get_current_domain(self.request)
        current_post_url = '{0}'.format(
            reverse('aurora.frontend.post.detail', kwargs={
                'year': obj.publish_date.year,
                'month': obj.publish_date.month,
                'day': obj.publish_date.day,
                'slugname': obj.slugname,
            })
        )
        return format_html('<a href="{0}{1}" target="_blank">{1}</a>', base_url, current_post_url)


    def generate_slugname(self, obj):
        counter  = 1
        slugname = slugify(obj.title.lower()[:65])
        while True:
            if Post.objects.filter(slugname = slugname).exclude(pk = obj.pk).exists():
                slugname = f"{slugname}-{counter}"
                counter += 1
            else:
                break
        return slugname

    def save_model(self, request, obj, form, change):
        obj.author   = request.user
        obj.slugname = self.generate_slugname(obj)
        super().save_model(request, obj, form, change)


@admin.register(Slideshow)
class SlideshowAdmin(admin.ModelAdmin):
    exclude = ('author', )
    list_display = ('title', 'image', 'mobile')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Configuration)
class configurationAdmin(admin.ModelAdmin):
    list_display = ('site', 'title')
    fieldsets = (
        (_('Site'), {'fields': ('site', 'title', 'slogan', 'slideshow', 'jumbotron')}),
        (_('Appearance'), {'fields': ('logo', 'icon', 'jumbotron_bg', 'jumbotron_clr')}),
        (_('Meta'), {'fields': ('keywords', 'description')}),
        (_('Contact'), {'fields': ('website', 'email', 'phone', 'address'),}),
        (_('Social Media'), {'fields': ('facebook', 'instagram', 'youtube')}),
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        return actions

    def response_add(self, request, obj, post_url_continue=None):
        with open( os.path.join(settings.CACHE_DIR, '.frontend_installed'), 'w') as writer:
            writer.write('Frontend is installed...')
        return super().response_add(request, obj, post_url_continue)

