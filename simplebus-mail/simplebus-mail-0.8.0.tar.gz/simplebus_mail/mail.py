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

"""SimpleBus extension for sending email."""

from collections import OrderedDict
from simplebus import Bus
from simplebus_mail.config import Config
from simplebus_mail.exceptions import SendMailError
from simplebus_mail.message import Message


class Mail(object):
    """Provides methods to send emails through the Bus."""

    def __init__(self, bus=None):
        self.__bus = None
        self.config = Config()

        if bus:
            self.init_bus(bus)

    @property
    def bus(self):
        """Gets the current bus."""
        return self.__bus

    def init_bus(self, bus):
        """Initializes the Mail with a SimpleBus instance."""

        if bus is None:
            raise ValueError('bus parameter cannot be None.')

        if not isinstance(bus, Bus):
            raise TypeError('bus parameter must be a Bus type.')

        if self.bus:
            raise RuntimeError('Mail is already initialized.')

        self.__bus = bus

    def send(self, message):
        """Sends the specified message to a SimpleBus."""

        if not self.bus:
            raise RuntimeError('Mail must be initialize. Maybe you forgot to call init_bus.')

        if not isinstance(message, Message):
            raise TypeError('Message must be a Message type.')

        self.__set_defaults(message)

        message.validate()

        try:
            self.bus.push(self.config.MAIL_QUEUE_NAME, self.__to_dict(message))
        except Exception as e:
            if self.config.MAIL_RAISE_ERRORS:
                raise SendMailError(e)

    def send_message(self, *args, **kwargs):
        """Sends the specified message to a SimpleBus."""
        self.send(Message(*args, **kwargs))

    def __set_defaults(self, message):
        """Sets the default values to the specified message."""

        if not message.sender:
            message.sender = self.config.MAIL_DEFAULT_SENDER

        if not message.recipients and self.config.MAIL_DEFAULT_RECIPIENTS:
            message.recipients = self.config.MAIL_DEFAULT_RECIPIENTS.copy()

    @staticmethod
    def __to_dict(message):
        d = OrderedDict()

        if message.sender:
            d['sender'] = message.sender

        if message.recipients:
            d['recipients'] = message.recipients

        if message.cc:
            d['cc'] = message.cc

        if message.bcc:
            d['bcc'] = message.bcc

        if message.reply_to:
            d['reply_to'] = message.reply_to

        if message.headers:
            d['headers'] = message.headers

        if message.subject:
            d['subject'] = message.subject

        if message.body:
            d['body'] = message.body

        return d
