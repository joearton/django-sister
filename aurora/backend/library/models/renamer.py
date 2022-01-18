import os
from django.utils.text import slugify


class BaseModelRenamer:

    def __init__(self, category="file", parentdir='uploads'):
        self.category = category
        self.parentdir = parentdir
        self.ori_fname_length = 25

    def rename_by_user(self, instance, filename):
        [filename, ext] = os.path.splitext(filename)
        filename = '{0}{1}'.format(self.category, ext)
        filepath = os.path.join(instance.user.username, filename)
        return filepath

    def include_parentdir(self, filepath):
        return os.path.join(self.parentdir, filepath)

    def include_protecteddir(self, filepath):
        return os.path.join(self.parentdir, 'P', filepath)

    def get_automatic_filepath(self, instance, filename):
        [fname, ext]  = os.path.splitext(filename)
        category_path = instance.__class__.__name__.lower()
        if hasattr(instance, 'app_user'):
            category_path = os.path.join(instance.app_user.user.username, category_path)
        if hasattr(instance, 'user'):
            category_path = os.path.join(instance.user.username, category_path)
        if hasattr(instance, 'title'):
            fname = instance.title
        if hasattr(instance, 'name'):
            fname = instance.name
        filename = '{0}{1}'.format(slugify(fname[:self.ori_fname_length]), ext)
        filepath = os.path.join(category_path, filename)
        return filepath

    def by_automatic(self, instance, filename):
        filepath = self.get_automatic_filepath(instance, filename)
        return self.include_parentdir(filepath)        
        
    def by_automatic_protected(self, instance, filename):
        filepath = self.get_automatic_filepath(instance, filename)
        return self.include_protecteddir(filepath)
