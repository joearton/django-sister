from django.core.mail import send_mail
from django.conf import settings


class Mail:

    def __init__(self):
        pass

    def send_message(self, sender, destination, subject, message_body):
        send_mail(subject, message_body, sender, [destination], fail_silently = False)
