from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _
from django.dispatch import receiver
from aurora.backend.library.models.renamer import BaseModelRenamer
from aurora.backend.library.validators import *
from aurora.backend.library.choices import *
from django.db import models
import uuid


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    date_deleted = models.DateTimeField(null = True, blank = True, editable=False)

    class Meta:
        abstract = True


class BaseModelUUID(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    date_created = models.DateTimeField(auto_now_add = True, editable=False)
    date_modified = models.DateTimeField(auto_now = True, editable=False)
    date_deleted = models.DateTimeField(null = True, blank = True, editable=False)

    class Meta:
        abstract = True



class Configuration(models.Model):
    name = models.SlugField(max_length = 128, primary_key = True)
    value = models.JSONField()
    protected = models.BooleanField(default = False)

    class Meta:
        pass

    def __str__(self):
        return self.name


class UserProperty(BaseModel):
    validator = Validators(max_size=(500), filetype='image')
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='property')
    picture = models.ImageField(upload_to=BaseModelRenamer(parentdir="backend").by_automatic_protected,
        validators=[validator.validate], verbose_name=_('Picture'), help_text=validator.help_text, null=True, blank=True)
    email_confirmed = models.BooleanField(default = False)
    email_sent = models.BooleanField(default = False)
    email_error = models.BooleanField(default = False)
    password_reset = models.BooleanField(default = False)
    subgroup = models.CharField(_('Sub Group'), max_length=32, null=True, blank=True)
    device = models.CharField(_('Device'), max_length=256, null=True, blank=True)
    browser = models.CharField(_('Browser'), max_length=512, null=True, blank=True)
    ip = models.CharField(_('IP'), max_length=16, null=True, blank=True)

    class Meta:
        verbose_name = _('User Property')
        verbose_name_plural =  _('User Properties')

    def __str__(self):
        return self.user.username


# create account automatically when user created
@receiver(post_save, sender = User)
def update_user_account(sender, instance, created, **kwargs):
    if created:
        if not UserProperty.objects.filter(user=instance).exists():
            UserProperty.objects.create(user = instance)
    instance.property.save()
