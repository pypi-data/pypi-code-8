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

"""Implements the message related objects."""

from simplebus_mail.exceptions import MailMalformedError


class Message(object):
    """Encapsulates an email message."""

    def __init__(self, sender=None,
                 recipients=None,
                 subject=None,
                 body=None,
                 cc=None,
                 bcc=None,
                 reply_to=None,
                 headers=None):

        self.sender = sender
        self.recipients = recipients or []
        self.subject = subject
        self.body = body
        self.cc = cc or []
        self.bcc = bcc or []
        self.reply_to = reply_to
        self.headers = headers or {}

    def validate(self):
        if self.sender is None:
            raise MailMalformedError('Sender cannot be None.')

        if not isinstance(self.sender, str):
            raise MailMalformedError('Sender must be a str.')

        if not isinstance(self.recipients, list):
            raise MailMalformedError('Recipients must be a list.')

        if len(self.recipients) == 0:
            raise MailMalformedError('Recipients must have at least one address.')

        if self.body is not None and not isinstance(self.body, str):
            raise MailMalformedError('Body must be a str.')

        if not isinstance(self.cc, list):
            raise MailMalformedError('Cc must be a list.')

        if not isinstance(self.bcc, list):
            raise MailMalformedError('Bcc must be a list.')

        if self.reply_to is not None and not isinstance(self.reply_to, str):
            raise MailMalformedError('Reply_to must be a str.')

        if not isinstance(self.headers, dict):
            raise MailMalformedError('Headers must be a dict.')
