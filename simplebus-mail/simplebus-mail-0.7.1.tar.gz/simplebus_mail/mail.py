# Copyright 2015 Vinicius Chiele. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from simplebus import Bus
from simplebus_mail import MailError
from simplebus_mail.utils import to_list


class Mail(object):
    def __init__(self, bus=None, config=None):
        self.__bus = None
        self.default_endpoint = None
        self.default_sender = None
        self.default_recipients = None
        self.queue_name = 'mail.outgoing'
        self.raise_errors = False

        if bus:
            self.init_bus(bus)

        if config:
            self.config_from_object(config)

    @property
    def bus(self):
        return self.__bus

    def init_bus(self, bus, config=None):
        if not bus:
            raise MailError('bus parameter must be provided.')

        if not isinstance(bus, Bus):
            raise MailError('bus parameter must be a Bus type.')

        self.__bus = bus

        if config:
            self.config_from_object(config)

    def config_from_object(self, config):
        if isinstance(config, dict):
            self.default_endpoint = config.get('MAIL_DEFAULT_ENDPOINT', 'default')
            self.default_sender = config.get('MAIL_DEFAULT_SENDER')
            self.default_recipients = to_list(config.get('MAIL_DEFAULT_RECIPIENTS'))
            self.queue_name = config.get('MAIL_QUEUE_NAME', 'mail.outgoing')
            self.raise_errors = config.get('MAIL_RAISE_ERRORS', False)
        else:
            self.default_endpoint = getattr(config, 'MAIL_DEFAULT_ENDPOINT', 'default')
            self.default_sender = getattr(config, 'MAIL_DEFAULT_SENDER', None)
            self.default_recipients = to_list(getattr(config, 'MAIL_DEFAULT_RECIPIENTS'))
            self.queue_name = getattr(config, 'MAIL_QUEUE_NAME', 'mail.outgoing')
            self.raise_errors = getattr(config, 'MAIL_RAISE_ERRORS', False)

    def send(self, message, endpoint=None):
        if not self.bus:
            raise MailError('Mail must be initialize.')

        if not isinstance(message, Message):
            raise MailError('Message must be a Message type.')

        endpoint = endpoint or self.default_endpoint

        self.__set_defaults(message)

        try:
            self.bus.push(self.queue_name, message.__dict__, endpoint=endpoint)
        except Exception as e:
            if self.raise_errors:
                raise MailError(e)

    def send_message(self, *args, **kwargs):
        endpoint = kwargs.pop('endpoint', self.default_endpoint)

        self.send(Message(*args, **kwargs), endpoint)

    def __set_defaults(self, message):
        if not message.sender:
            message.sender = self.default_sender

        if not message.recipients:
            message.add_recipient(self.default_recipients)


class Message(object):
    """Encapsulates an email message.

    :param subject: email subject header
    :param recipients: list of email addresses
    :param body: plain text message
    :param html: HTML message
    :param sender: email sender address, or **MAIL_DEFAULT_SENDER** by default
    :param cc: CC list
    :param bcc: BCC list
    :param reply_to: reply-to address
    :param extra_headers: A dictionary of additional headers for the message
    """

    def __init__(self, subject=None,
                 recipients=None,
                 body=None,
                 html=None,
                 sender=None,
                 cc=None,
                 bcc=None,
                 reply_to=None,
                 extra_headers=None):

        self.recipients = to_list(recipients)
        self.subject = subject
        self.sender = sender
        self.reply_to = reply_to
        self.cc = to_list(cc)
        self.bcc = to_list(bcc)
        self.body = body
        self.html = html
        self.extra_headers = extra_headers

    def add_recipient(self, recipient):
        """Adds another recipient to the message."""
        if isinstance(recipient, list):
            for address in recipient:
                self.recipients.append(address)
        else:
            self.recipients.append(recipient)
