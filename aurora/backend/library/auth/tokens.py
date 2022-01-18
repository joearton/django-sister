from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import six


def get_user_pk_token(user_pk):
    user_pk = force_bytes(user_pk)
    user_pk = urlsafe_base64_encode(user_pk)
    return force_text(user_pk)


def get_user_uid(uid):
    uid = urlsafe_base64_decode(uid)
    return force_text(uid)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()
