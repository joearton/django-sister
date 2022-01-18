from django.conf import settings
from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Field
from crispy_forms.bootstrap import AppendedText, PrependedText
from captcha.fields import CaptchaField, CaptchaTextInput
from django.utils.translation import gettext as _


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'backend/elements/captcha.html'


class SignUpForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"))
    password = forms.CharField(min_length=settings.BACKEND_SETTINGS['password_policy']['min'],
                max_length=settings.BACKEND_SETTINGS['password_policy']['max'],
                label=_("Password"), widget=forms.PasswordInput)
    confirmation = forms.CharField(min_length=settings.BACKEND_SETTINGS['password_policy']['min'],
                max_length=settings.BACKEND_SETTINGS['password_policy']['max'],
                label=_("Confirmation"), widget=forms.PasswordInput)
    captcha = CaptchaField(widget=CustomCaptchaTextInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_items = ['email', 'password', 'confirmation', 'captcha']
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div('email', css_class='my-1'),
            Div('password', css_class='my-1'),
            Div('confirmation', css_class='my-1'),
            Div('captcha', css_class='my-1'),
            Div(
                Submit(_('Create New Account'), _('Create New Account'), css_class='btn-primary'),
                css_class="text-center d-grid gap-2"
            )
        )


class SignInForm(forms.Form):
    email = forms.CharField(label=_('E-mail'))
    password = forms.CharField(min_length=6, max_length=32, widget=forms.PasswordInput)
    captcha = CaptchaField(widget=CustomCaptchaTextInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                HTML('<span class="input-group-text" id="input1"><i class="fa fa-user"></i></span>'),
                HTML('<input type="text" id="id_email" name="email" class="form-control form-control-lg" placeholder="{0}" aria-describedby="input1" required="True" />'.format(_('E-mail or username'))),
                css_class='input-group mb-3'
            ),
            Div(
                HTML('<span class="input-group-text" id="input2"><i class="fa fa-key"></i></span>'),
                HTML('<input type="password" id="id_password" name="password" class="form-control form-control-lg" placeholder="{0}" aria-describedby="input2"  required="True" />'.format(_('Password'))),
                css_class='input-group mb-3'
            ),
            Div('captcha', css_class='mb-3'),
            Div(
                Div(HTML('<a href="{}">{}</a>'.format(reverse('aurora.backend.signup'), _('Forgot Password?'))), css_class="text-end mb-2"),
                Div(
                    HTML(f'<button type="submit" class="btn btn-primary btn-lg"><i class="fa fa-sign-in-alt"></i> {_("Sign In")}</button>'),
                    css_class="d-grid gap-2 mb-3 text-center"),
            ),
            Div(
                HTML('<a href="{}" class="btn btn-secondary btn-lg"><i class="fa fa-graduation-cap"></i> {}</a>'.format(
                    reverse('aurora.int.signin'), _('Sign In Using Siakad'))),
                css_class = "text-center d-grid gap-2"
            )
        )
