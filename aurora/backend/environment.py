from django.utils.translation import gettext_lazy as _

class BaseAppEnvironment:
    name    = ''
    public  = {}
    backend = {}


class backendEnvironment(BaseAppEnvironment):
    backend = {}
