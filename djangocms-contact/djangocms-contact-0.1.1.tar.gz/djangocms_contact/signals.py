from django.core.mail import send_mail
from django.dispatch import Signal, receiver

from .settings import get_setting

contact_signal = Signal(providing_args=['name', 'email', 'subject', 'message'])


@receiver(contact_signal)
def new_message_notification(sender, **kwargs):
    """Sent a "new message" notification to an email address."""

    from_email = get_setting('CMSCONTACT_FROM_EMAIL')
    to_email = get_setting('CMSCONTACT_TO_EMAIL')

    if from_email is not None and to_email is not None:
        message = 'Name: {name}\n'.format(name=kwargs['name'])
        message += 'Email: {email}\n'.format(email=kwargs['email'])
        message += 'Subject: {subject}\n\n'.format(subject=kwargs['subject'])
        message += 'Message:\n{message}\n'.format(message=kwargs['message'])
        send_mail('New message notification', message, from_email, [to_email],
                  fail_silently=False)
