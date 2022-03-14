from celery.utils import dispatch
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.views.generic import FormView, TemplateView
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from aurora.backend.users import User
from aurora.backend.tasks import send_activation_link
from django.utils.translation import gettext as _
from aurora.backend.views.auth.forms import SignUpForm
from aurora.backend.views.auth import AuthView
from aurora.backend.library import site



class BaseSignUpView(AuthView):

    def get_auth_info(self):
        auth_info = super().get_auth_info()
        auth_info['title'] = _('Human Resource')
        auth_info['description'] = _('This is sign up page. Sign up using your e-mail to get more features')
        return auth_info


class SignedUpView(BaseSignUpView, TemplateView):
    section_title = _('Thank You')
    template_name = 'backend/sections/auth/signedup.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.current_user = get_object_or_404(User, pk=self.kwargs['pk'], email=self.kwargs['email'])
        rest_time = timezone.now().astimezone() - self.current_user.date_joined.astimezone()
        minute = rest_time.total_seconds()/60
        if minute > 1:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['user'] = self.current_user
        return context_data


class SignUpView(BaseSignUpView, FormView):
    section_title = _('Sign Up')
    template_name = 'backend/sections/auth/signup.html'
    form_class = SignUpForm

    def create_user(self, username, password):
        message = None
        user = User.objects.create(username = username, email = username)
        user.password = make_password(password)
        if settings.BACKEND_SETTINGS['signup_method'] == 'e-mail':
            user.is_active = False
            message = _('Account created, please check your inbox or spam folder')
            user.save()
            send_activation_link.delay(site.get_current_domain(self.request), user.pk)
        else:
            user.is_active = True
            user.save()
            message = _('Account created, please sign in')
        return user


    def form_valid(self, form, *args, **kwargs):
        message = None
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        confirmation = form.cleaned_data.get('confirmation')
        if password != confirmation:
            message = _('Password and confirmation do not match')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            if not user.is_active and not user.property.email_sent:
                message = _('You have not confirmed your e-mail, please check your inbox or spam folder')
                send_activation_link.delay(site.get_current_domain(self.request), user.pk)
        if message:
            messages.add_message(self.request, messages.INFO, message)
            return super().form_invalid(form, *args, **kwargs)
        user = self.create_user(username, password)
        return redirect('aurora.backend.signedup', pk=user.pk, email=user.email)


# send_activation_link.delay("simlitabmas.umko.ac.id", 29)