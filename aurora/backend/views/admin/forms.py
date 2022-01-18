from django.conf import settings
from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Field
from crispy_forms.bootstrap import AppendedText, PrependedText
from captcha.fields import CaptchaField, CaptchaTextInput
from django.utils.translation import gettext as _


class FormCeleryService(forms.Form):
    celery_worker = forms.BooleanField(label=_('Celery Service'), required=False)

