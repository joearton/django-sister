from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from aurora.backend.environment import backendEnvironment
from django.contrib import messages
from django.views.generic import View
from aurora.backend.views.auth import DefaultDashboardView
from aurora.backend.users import User
from aurora.backend.library.auth.tokens import account_activation_token, get_user_uid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import importlib


def shared_activate_user(request, user):
    user.is_active = True
    user.property.email_confirmed = True
    user.save()
    if hasattr(settings, 'USER_ACTIVATOR'):
        activator = importlib.import_module(settings.USER_ACTIVATOR)
        activator.activate(user)


class ActivationView(View, DefaultDashboardView):

    def activate_user(self, request, user):
        shared_activate_user(request, user)
        login(request, user)


    def get(self, request, *args, **kwargs):
        try:
            uid  = get_user_uid(self.kwargs['uid'])
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and account_activation_token.check_token(user, self.kwargs['token']):
            self.activate_user(request, user)
            return self.go_to_dashboard(request)
        messages.add_message(request, messages.INFO, _("Account activation failed, please call web administrator"))
        return redirect("aurora.backend.signup")
