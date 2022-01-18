from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from aurora.backend.views.auth import signin
from aurora.backend.views.auth.signin import SignInView
from aurora.backend.views.auth.signup import SignUpView, SignedUpView
from aurora.backend.views.auth.role import AccountView, RoleView
from aurora.backend.views.auth.signout import SignOutView
from aurora.backend.views.auth.activation import ActivationView
from aurora.backend.views.backend import DefaultView
from aurora.backend.environment import backendEnvironment



urlpatterns = []

if settings.BACKEND_SETTINGS['aurora_auth']:
    # authorization and authority
    signin_url = 'aurora.backend.signin'
    if backendEnvironment.backend['signin_url'] == signin_url:
        urlpatterns += [path('signin', SignInView.as_view(), name=signin_url)]

    signup_url = 'aurora.backend.signup'
    if backendEnvironment.backend['signup_url'] == signup_url:
        urlpatterns += [
            path('signup', SignUpView.as_view(), name='aurora.backend.signup'),
            path('signedup/<str:pk>/email/<str:email>', SignedUpView.as_view(), name='aurora.backend.signedup'),
            path('activate/account/<str:uid>/<str:token>', ActivationView.as_view(), name='aurora.backend.signup_activation'),
        ]
        
    urlpatterns += [path('signout', SignOutView.as_view(), name='aurora.backend.signout')]


# backend panel
if settings.BACKEND_SETTINGS['aurora_backend']:
    urlpatterns += [
        path('panel/default', DefaultView.as_view(), name='aurora.backend.panel.default'),
        path('account', AccountView.as_view(), name='aurora.backend.account'),
        path('account/role', RoleView.as_view(), name='aurora.backend.account.role'),
    ]


if settings.DEBUG:
    from aurora.backend.library.bootstrap.browser import auto_reload
    urlpatterns += [
        path('debug/auto_reload', auto_reload, name = 'aurora.backend.debug.auto_reload'),
    ]
