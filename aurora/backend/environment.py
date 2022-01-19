from django.utils.translation import gettext_lazy as _

class BaseAppEnvironment:
    name    = ''
    public  = {}
    backend = {}


class backendEnvironment(BaseAppEnvironment):
    backend = {
        'title'         : 'Admin',
        'dashboard_url' : 'aurora.pilar.dashboard',
        'signin_url'    : 'aurora.backend.signin',
        'signup_url'    : 'aurora.backend.signup',
        'signout_url'   : 'aurora.backend.signout',
    }
