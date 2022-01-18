from celery import Celery
from celery import shared_task
from django.conf import settings
from aurora.backend.library import mail
from aurora.backend.library.auth.tokens import account_activation_token, get_user_pk_token
from django.template.loader import render_to_string
from aurora.backend.users import User
from django.utils.translation import gettext as _
from celery.schedules import crontab


app = Celery('tasks', broker=settings.CELERY_BROKER_URL)


@app.task()
def send_activation_link(site_url, user_pk):
    # remember that parameter will be serialized
    # so never change into complicated variable
    user = User.objects.get(pk=user_pk)
    user_type = _('New User')
    if user.is_staff:
        user_type = _("New Staff")
    message_body = render_to_string('backend/sections/auth/mail_activation.html', {
        'user'      : user,
        'user_type' : user_type,
        'site_url'  : site_url,
        'uid'       : get_user_pk_token(user.pk),
        'token'     : account_activation_token.make_token(user),
    })
    sender  = 'No Reply <{0}>'.format(settings.EMAIL_HOST_USER)
    subject = "{0} - {1}".format(_('New Account Activation'), user.username)
    email   = mail.Mail()
    try:
        message = email.send_message(sender, user.email, subject, message_body)
        user.property.email_sent = True
    except:
        user.property.email_error = True
    user.save()
