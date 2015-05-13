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

"""Implements the configuration related objects."""


class Config(object):
    # Default mail sender (from)
    MAIL_DEFAULT_SENDER = None

    # Default mail recipients (to)
    MAIL_DEFAULT_RECIPIENTS = []

    # Queue name where the emails are going to be sent.
    MAIL_QUEUE_NAME = 'mail.outgoing'

    # True indicates that any error on sending emails will be thrown.
    # False indicates that any error should be suppressed.
    MAIL_RAISE_ERRORS = False

    def from_object(self, obj):
        """Load values from an object."""
        if isinstance(obj, dict):
            for key in obj:
                if key.isupper() and key.startswith('MAIL_'):
                    value = obj.get(key)
                    self.__setattr(key, value)
        else:
            for key in dir(obj):
                if key.isupper() and key.startswith('MAIL_'):
                    value = getattr(obj, key)
                    self.__setattr(key, value)

    def __setattr(self, key, value):
        """Sets the value for the specified key whether it exists."""
        if hasattr(self.__class__, key):
            setattr(self, key, value)
