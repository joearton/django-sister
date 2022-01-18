from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.http import Http404
from django.contrib import messages
from django.views.generic import View
from django.utils.translation import gettext as _
from django.conf import settings
from aurora.backend.environment import backendEnvironment
from aurora.backend.models import User


class SignOutView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'previous_signin_in' in request.session:
                user = User.objects.get(pk=request.session.get('previous_signin_in'))
                if user:
                    if user.is_superuser:
                        logout(request)
                        login(request, user)
                        messages.add_message(request, messages.INFO, _('You are sign in as ') + user.username)
                        if request.user.is_staff:
                            return redirect('admin:index')
                        else:
                            if settings.BACKEND_SETTINGS['aurora_backend']:
                                return redirect(backendEnvironment.backend['dashboard_url'])
                            else:
                                return redirect('admin:index')
            messages.add_message(request, messages.INFO, _('You are signed out'))
            logout(request)
            return redirect(settings.LOGOUT_REDIRECT_URL)
        raise Http404()
