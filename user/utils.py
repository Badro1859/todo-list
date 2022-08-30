from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import threading

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str,  DjangoUnicodeDecodeError

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified))


generate_token = TokenGenerator()


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):

    email_subject = 'Activate your account'

    current_site = get_current_site(request) if request is not None else ""
    email_body = render_to_string('user/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    email.fail_silently = False
    email.send()

    print('the email sent succeffuly to {}'.format(user.email))
    # if not settings.TESTING:
    #     EmailThread(email).start()
