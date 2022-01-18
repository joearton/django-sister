from django import forms
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http.response import Http404
from django.urls import reverse
from django.views.generic import FormView
from django.shortcuts import redirect
from aurora.backend.users import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from aurora.backend.views.auth.forms import SignInForm
from aurora.backend.views.auth import DefaultDashboardView
from django.utils.translation import gettext as _
from aurora.backend.views import BaseView
from django.conf import settings
from django import forms


@method_decorator(login_required, name='dispatch')
class AccountView(BaseView, DefaultDashboardView):
    section_title = _('Your Account')
    template_name = 'backend/sections/auth/role_switcher.html'

    def dispatch(self, request, *args, **kwargs):
        role = self.request.session.get('role')
        if request.user.is_superuser:
            return redirect('admin:index')
        if role is None:
            group_count = request.user.groups.count()
            if group_count == 0 or group_count > 1:
                return redirect('aurora.backend.account.role')
            if group_count == 1:
                user_role = self.request.user.groups.all()[0]
                self.set_default_role(self.request, user_role.name)
        return self.go_to_dashboard(self.request)
    

class RoleForm(forms.Form):
    role = forms.CharField(required=True, widget=forms.HiddenInput())


@method_decorator(login_required, name='dispatch')
class RoleView(BaseView, FormView, DefaultDashboardView):
    section_title = _('Role Chooser')
    template_name = 'backend/sections/auth/role_switcher.html'
    form_class = RoleForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        self.set_default_role(self.request, role)
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.session.has_key('role'):
            messages.info(self.request, _('You are authorized as ') + self.request.session.get('role').title())
        return self.go_to_dashboard(self.request, url_only=True)