from aurora.backend.environment import BaseAppEnvironment
from django.utils.translation import gettext_lazy as _



class frontendEnvironment(BaseAppEnvironment):
    public = {}
    backend = {}
