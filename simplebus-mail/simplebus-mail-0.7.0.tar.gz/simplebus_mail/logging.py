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

from logging import Handler
from simplebus import current_bus
from simplebus_mail.mail import Mail
from simplebus_mail.mail import Message


class MailHandler(Handler):
    def __init__(self, sender, recipients, endpoint=None, bus=None):
        super().__init__()
        self.__sender = sender
        self.__recipients = recipients
        self.__mail = Mail(bus or current_bus)
        self.__mail.default_sender = sender
        self.__mail.default_recipients = recipients
        self.__mail.default_endpoint = endpoint

    def emit(self, record):
        subject = self.build_subject(record)
        body = self.format(record)
        message = Message(subject, self.__recipients, body)
        self.__mail.send(message)

    def build_subject(self, record):
        subject = self.__mail.bus.app_id

        if subject:
            subject += ': '

        if record.msg:
            i = record.msg.find('\n')
            if i == -1:
                i = len(record.msg)
            subject += record.msg[:200] if i > 200 else record.msg[:i]

        return subject
