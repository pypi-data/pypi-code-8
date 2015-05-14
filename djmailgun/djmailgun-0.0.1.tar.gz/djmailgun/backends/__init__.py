from abc import ABCMeta, abstractmethod

import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.core.mail.message import sanitize_address

from djmailgun import StringIO
from djmailgun.errors import MailgunApiError, MailgunAttributeError
from djmailgun.models import MailgunSettings


class Backend(BaseEmailBackend, metaclass=ABCMeta):
    """
    A Django Email base backend that uses mailgun.
    The backend for the appropriate version will be in a separate file.
    """

    def __init__(self, fail_silently=False, *args, **kwargs):
        super(Backend, self).__init__(fail_silently=fail_silently, *args, **kwargs)

        try:
            self.init_attributes()
        except MailgunAttributeError:
            if fail_silently:
                self._access_key, self._server_name = None, None
            else:
                raise

    def init_attributes(self):
        self._access_key = self.get_attribute('MAILGUN_ACCESS_KEY')
        self._server_name = self.get_attribute('MAILGUN_SERVER_NAME')

    def get_attribute(self, attribute_name):
        try:
            return getattr(settings, attribute_name)
        except AttributeError:
            try:
                setting = MailgunSettings.objects.get(key=attribute_name)
                return setting.value
            except MailgunSettings.DoesNotExist:
                raise MailgunAttributeError

    @abstractmethod
    def get_api_url(self):
        pass

    def open(self):
        """
        Stub for open connection, all sends are done over HTTP POSTs
        """
        pass

    def close(self):
        """
        Close any open HTTP connections to the API server.
        """
        pass

    def _send(self, email_message):
        """
        A helper method that does the actual sending.
        """

        if not email_message.recipients():
            return False

        from_email = sanitize_address(email_message.from_email, email_message.encoding)
        recipients = [sanitize_address(recipient, email_message.encoding) for recipient in email_message.recipients()]

        try:
            response = requests.post(
                self.get_api_url() + 'messages.mime',
                auth=('api', self._access_key),
                data={
                    'to': ', '.join(recipients),
                    'from': from_email
                },
                files={
                    'message': StringIO(email_message.message().as_string())
                }
            )
        except:
            if not self.fail_silently:
                raise
            return False

        if response.status_code != 200:
            if not self.fail_silently:
                raise MailgunApiError(response)
            return False

        return True

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of
        email messages sent.
        """
        num_sent = 0

        if not email_messages:
            return num_sent

        for email_message in email_messages:
            if self._send(email_message):
                num_sent += 1

        return num_sent