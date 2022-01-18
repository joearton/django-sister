from django import forms
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import os


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def readable_filesize(nbytes):
    i = 0
    while nbytes >= 1000 and i < len(suffixes)-1:
        nbytes /= 1000.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])



class Validators:

    def __init__(self, max_size = None, filetype = 'image', extentions = []):
        self.max_size = max_size
        if not self.max_size:
            self.max_size = settings.UPLOAD_MAX_SIZE
        self.max_size = (self.max_size * 1000) # convert to kilobit (kb)
        self.allowed_exts = extentions
        if not self.allowed_exts :
            if filetype == 'image':
                self.allowed_exts = settings.UPLOAD_EXT_IMAGES
            elif filetype == 'docs':
                self.allowed_exts = settings.UPLOAD_EXT_DOCS
            elif filetype == 'image/docs':
                self.allowed_exts = settings.UPLOAD_EXT_IMAGES + settings.UPLOAD_EXT_DOCS


    def validate_size(self, value):
        self.filesize = value.size
        if self.filesize > self.max_size:
            content = _("Max size") + " {0} ".format(readable_filesize(self.max_size))
            raise forms.ValidationError(content)
        return value


    def validate_ext(self, value):
        filename, ext  = os.path.splitext(value.name)
        if not ext.lower() in self.allowed_exts:
            content = _("Extentions") + " {0} ".format(self.allowed_exts)
            raise forms.ValidationError(content)
        return value


    def validate(self, value):
        validate_ext = self.validate_ext(value)
        if validate_ext:
            validate_size = self.validate_size(value)
            if validate_size:
                return value


    def help_text(self):
        supported_exts = ', '.join(self.allowed_exts)
        max_size = readable_filesize(self.max_size)
        return _("Extentions") + " {0} (".format(supported_exts) + _("Max size") + " {0})".format(max_size)
