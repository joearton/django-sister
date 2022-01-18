from django.contrib.auth import authenticate, login
from django.contrib import messages
from aurora.backend.users import User
from aurora.backend.views.auth.forms import SignInForm
from aurora.backend.tasks import send_activation_link
from django.utils.translation import gettext as _
from django.views.generic import FormView
from aurora.backend.views.auth import AuthView
from aurora.backend.library import site


class SignInView(AuthView, FormView):
    section_title = _('Sign In')
    template_name = 'backend/sections/auth/signin.html'
    form_class = SignInForm

    def get_auth_info(self):
        auth_info = super().get_auth_info()
        return auth_info

    def form_valid(self, form, *args, **kwargs):
        if self.request.session.has_key('signup_url'):
            del self.request.session['signup_url']
        message = None
        username = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            return self.go_to_dashboard(self.request)
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user:
            if not user.is_active:
                message = _('You have not confirmed your e-mail, please check your inbox or spam folder')
                if user.property.email_sent:
                    site_url = site.get_current_domain(self.request)
                    send_activation_link(site_url, user.pk)
        else:
            message = _('Account not found, please sign up if you have not created yet')
            self.request.session['signup_url'] = True
        if message:
            messages.add_message(self.request, messages.INFO, message)
        return super().form_invalid(form, *args, **kwargs)
