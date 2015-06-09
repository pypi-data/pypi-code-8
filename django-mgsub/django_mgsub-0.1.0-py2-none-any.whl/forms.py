import logging

from django import forms
from django.conf import settings
from django.template import Context
from django.template.loader import get_template, TemplateDoesNotExist
from django.core.mail import EmailMultiAlternatives

from mgsub.mailgun import MailgunList

logger = logging.getLogger('mgsub')


class SignupForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, list_email=None, *args, **kwargs):
        self.mailinglist = MailgunList(list_email)
        super(SignupForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        if not super(SignupForm, self).is_valid():
            return False

        if not self.subscribe():
            self.add_error(None, 'There was a failure adding you to the mailing list')
            return False

        if getattr(settings, 'MGSUB_SEND_WELCOME', True):
            return self.send_welcome()

        return True

    def subscribe(self):
        try:
            return self.mailinglist.subscribe(self.cleaned_data['email'])
        except Exception, e:
            logger.error(e)
            return False

    def unsubscribe(self):
        try:
            return self.mailinglist.unsubscribe(self.cleaned_data['email'])
        except Exception, e:
            logger.error(e)
            return False

    def send_welcome(self):
        email = self.cleaned_data['email']

        subject = getattr(settings, 'MGSUB_WELCOME_SUBJECT', 'Welcome!')
        from_address = getattr(settings, 'MGSUB_WELCOME_FROM',
                               settings.SERVER_EMAIL)
        reply_to = getattr(settings, 'MGSUB_WELCOME_REPLY_TO', None)
        welcome_template = getattr(settings, 'MGSUB_WELCOME_TEMPLATE',
                                   'mgsub/welcome.html')
        welcome_plain = getattr(settings, 'MGSUB_WELCOME_TEMPLATE_PLAIN',
                                'mgsub/welcome.txt')

        context = Context()

        welcome_txt = get_template(welcome_plain).render(context)

        attach_html = True

        try:
            welcome_html = get_template(welcome_template).render(context)
        except TemplateDoesNotExist:
            attach_html = False

        message = EmailMultiAlternatives(subject, welcome_txt, from_address,
                                         to=[email], reply_to=reply_to)
        if attach_html:
            message.attach_alternative(welcome_html, 'text/html')
        message.send()

        return True
