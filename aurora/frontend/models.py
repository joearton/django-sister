from django.db import models
from django import forms
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.utils import ProgrammingError
from aurora.backend.library.validators import Validators
from aurora.backend.library.site import Site, CurrentSiteManager, get_site_pk
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
from django.utils.crypto import get_random_string
from aurora.backend.models import BaseModel, User, BaseModel
from aurora.frontend.library.choices import *
from aurora.backend.library.validators import readable_filesize
from ckeditor.fields import RichTextField
from django.utils import timezone
import os
import uuid


class Navbar(BaseModel):
    title = models.CharField(_("Title"), max_length=32)
    url = models.CharField(_("URL"), max_length=3156, default='#')
    icon = models.CharField(_("icon"), max_length=32, blank=True, null=True)
    order = models.PositiveIntegerField(_("Order"), default=0, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
        verbose_name=_("Parent"), null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, default=get_site_pk)

    class Meta:
        verbose_name = _('Navigation Bar')
        ordering = ['-order', 'date_created']

    def __str__(self):
        return self.title


def save_file(instance, filename):
    [name, ext] = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}"
    if not filename.lower().endswith(ext.lower()):
        filename += f"{ext}"
    return os.path.join('frontend/files', str(instance.date_created.year),
        str(instance.date_created.month), filename)


class Files(BaseModel):
    validator = Validators(max_size=(7500), filetype='image/docs')
    name = models.CharField(_("Name"), max_length=1000, null=True, blank=True)
    upload = models.FileField(_("Upload"), upload_to=save_file, validators=[validator.validate],
        help_text=validator.help_text, max_length=1024)
    meta = models.JSONField(_("Meta"), null=True, blank=True, editable=False)
    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")
        ordering = ['date_created']

    def __str__(self):
        ext = os.path.splitext(self.upload.name)[1].lower()
        return f"[{readable_filesize(self.upload.size)}] {self.name} [{ext[1:].upper()}]"


@receiver(pre_delete, sender=Files)
def upload_delete(sender, instance, **kwargs):
    instance.upload.delete(True)


class Category(BaseModel):
    slugname = models.SlugField(_("Slugname"), unique=True, max_length=255)
    name = models.CharField(_('Name'), max_length=512)
    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class AbstractPost(BaseModel):
    validator = Validators(max_size=(500), filetype='image')
    slugname = models.CharField(_('Slugname'), unique=True, max_length=255)
    title = models.CharField(_('Title'), max_length=512)
    content = RichTextField(_('Content'), null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
        verbose_name=_('Category'), blank=True, null=True)
    thumbnail = models.FileField(upload_to="frontend/posts", validators=[validator.validate],
        verbose_name=_('Thumbnail'), help_text=validator.help_text, null=True, blank=True, max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    files = models.ManyToManyField(Files, blank=True, verbose_name=_('Files'))
    password = models.CharField(_('Password'), max_length=256, blank=True, null=True)
    post_type = models.CharField(_('Post Type'), choices=choice_post_type, max_length=512, default='post')
    publish_date = models.DateTimeField(_('Publish Date'), default=timezone.now)
    meta = models.JSONField(_('Meta'), null=True, blank=True, editable=False)
    site = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True
        ordering = ['-date_modified', '-date_created']

    def __str__(self):
        return self.title


@receiver(pre_delete, sender=AbstractPost)
def post_delete(sender, instance, **kwargs):
    instance.thumbnail.delete(True)


class Post(AbstractPost):
    validator = Validators(max_size=(500), filetype='image')
    thumbnail = models.FileField(upload_to="frontend/pages", validators=[validator.validate],
        verbose_name=_('Thumbnail'), help_text=validator.help_text, null=True, blank=True)


class Page(AbstractPost):
    validator = Validators(max_size=(500), filetype='image')
    thumbnail = models.FileField(upload_to="frontend/pages", validators=[validator.validate],
        verbose_name=_('Thumbnail'), help_text=validator.help_text, null=True, blank=True)


class Slideshow(BaseModel):
    validator = Validators(max_size=(750), filetype='image')
    image = models.ImageField(upload_to="frontend/slideshow",
        verbose_name=_('Image'), validators=[validator.validate], help_text=validator.help_text)
    title = models.CharField(_("Title"), max_length=128)
    mobile = models.BooleanField(_("Mobile UI"), default=False)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, default=get_site_pk)

    class Meta:
        verbose_name = _('Slideshow')
        ordering = ['date_created']

    def __str__(self):
        return self.title



@receiver(pre_delete, sender=Slideshow)
def slideshow_delete(sender, instance, **kwargs):
    instance.image.delete(True)


class Sidebar(BaseModel):
    slugname = models.SlugField(unique=True, max_length=255)
    name = models.CharField(_('Title'), max_length=512)
    content = RichTextField(_('Content'))
    order = models.PositiveIntegerField(_('Order'), default=0)
    icon = models.CharField(_('Icon'), max_length=32, blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, default=get_site_pk)

    class Meta:
        verbose_name = _('Sidebar')
        ordering = ['order']

    def __str__(self):
        return self.name


class Configuration(BaseModel):
    jumbotron_clr_choice = [
        ('light', _('Light')),
        ('dark', _('Dark')),
    ]
    validator = Validators(max_size=(500), filetype='image')
    title = models.CharField(_('Title'), max_length=256)
    slogan = models.CharField(_('Slogan'), max_length=256, null=True, blank=True)
    description = models.TextField(_('Short Description'), null=True, blank=True)
    keywords = models.CharField(_('Keywords'), max_length=256)
    logo = models.ImageField(upload_to="frontend/logo", validators=[validator.validate],
        verbose_name=_('Logo (16:9)'), help_text=validator.help_text, null=True, blank=True)
    icon = models.ImageField(upload_to="frontend/icon", validators=[validator.validate],
        verbose_name=_('Icon (1:1)'), help_text=validator.help_text, null=True, blank=True)
    slideshow = models.BooleanField(_('Use Slideshow'), default=False)
    jumbotron = models.BooleanField(_('Use Jumbotron'), default=True)
    jumbotron_bg = models.ImageField(upload_to="frontend/", validators=[validator.validate],
        verbose_name=_('Jumbotron Background'), help_text=validator.help_text, null=True, blank=True)
    jumbotron_clr = models.CharField(_('Jumbotron Color'), max_length=128,
        choices=jumbotron_clr_choice, default='#f1f1f1')
    address = models.CharField(_('Address'), max_length=512)
    email = models.EmailField(_('E-mail'), max_length=128)
    website = models.URLField(_('Website'), max_length=512, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=16)
    facebook = models.URLField(_('Facebook'), max_length=512, null=True, blank=True)
    instagram = models.URLField(_('Instagram'), max_length=512, null=True, blank=True)
    youtube = models.URLField(_('Youtube'), max_length=512, null=True, blank=True)
    site = models.OneToOneField(Site, on_delete=models.SET_NULL, null=True, default=get_site_pk)

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.site.name


