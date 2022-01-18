from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class frontendConfig(AppConfig):
    name = 'aurora.frontend'
    verbose_name = _('Frontend')
