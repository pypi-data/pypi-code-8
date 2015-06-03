# -*- coding: utf-8 -*-
''' Klarna API - PClass

Defines the class for holding PClasses
'''

# Copyright 2015 Klarna AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# python3k campatibility
from __future__ import print_function
import sys
if sys.version_info >= (3,):
    basestring = str
    long = int

__all__ = ('PClass',)

import time
from .const import *


class PClass(object):
    fields = ('eid', 'id', 'description', 'months', 'startfee', 'invoicefee',
        'interestrate', 'minamount', 'country', 'type', 'expire')

    class Type(object):
        INVOICE = -1
        CAMPAIGN = 0
        ACCOUNT = 1
        SPECIAL = 2
        FIXED = 3
        DELAY = 4
        MOBILE = 5

    @property
    def description(self):
        'Description'
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def months(self):
        'Number of months'
        return self._months

    @months.setter
    def months(self, value):
        if value not in('-', ''):
            self._months = int(value)
        else:
            value = None

    @property
    def startfee(self):
        'Starting fee'
        return self._startfee

    @startfee.setter
    def startfee(self, value):
        self._startfee = float(value)

    @property
    def invoicefee(self):
        'Invoicing/handling fee'
        return self._invoicefee

    @invoicefee.setter
    def invoicefee(self, value):
        self._invoicefee = float(value)

    @property
    def interestrate(self):
        'Interest rate'
        return self._interestrate

    @interestrate.setter
    def interestrate(self, value):
        self._interestrate = float(value)

    @property
    def minamount(self):
        'Minimum amount to use this PClass'
        return self._minamount

    @minamount.setter
    def minamount(self, value):
        self._minamount = float(value)

    @property
    def country(self):
        'Country'
        return self._country

    @country.setter
    def country(self, value):
        try:
            self._country = lookup(Countries, value)
        except ValueError:
            raise UnknownCountry(value)

    @property
    def id(self):
        'ID'
        return self._id

    @id.setter
    def id(self, value):
        self._id = int(value)

    @property
    def type(self):
        'Type'
        return self._type

    @type.setter
    def type(self, value):
        self._type = int(value)

    @property
    def eid(self):
        'Merchant ID or Estore ID connect to this PClass'
        return self._eid

    @eid.setter
    def eid(self, value):
        self._eid = int(value)

    @property
    def expire(self):
        'Valid until/expire unix timestamp'
        return self._expire

    @expire.setter
    def expire(self, value):
        if isinstance(value, (int, long, float)):
            self._expire = value
        elif isinstance(value, basestring) and value not in ('-', ''):
            self._expire = time.mktime(time.strptime(value, '%Y-%m-%d'))
        else:
            self._expire = None

    def is_valid(self, now=None):
        ''' True if this PClass is not expired '''

        if getattr(self, 'expire', None) is None:
            # No expire, or unset? assume valid
            return True

        if now is None:
            now = time.time()

        return now < self.expire

    def __init__(self, *args, **kwargs):
        ptk = ('id', 'description', 'months', 'startfee', 'invoicefee',
            'interestrate', 'minamount', 'country', 'type', 'expire', 'eid')

        # Map positional arguments to their respective names
        for k, v in zip(ptk, args):
            kwargs[k] = v

        # Allow desc as a shorthand for description
        if 'desc' in kwargs:
            kwargs['description'] = kwargs['desc']
            del kwargs['desc']

        # Set the attributes
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __lt__(self, other):
        spec = PClass.Type.SPECIAL
        if self.type == spec and other.type != spec:
            return True
        elif self.type != spec and other.type == spec:
            return False

        return self.description < other.description

    def __iter__(self):
        for k in self.fields:
            if k == 'country':
                yield (k, Countries[self.country])
            elif k == 'type':
                yield (k, self.type)
            else:
                yield (k, getattr(self, k, ''))

    def __repr__(self):
        return '(PClass %s)' % ', '.join(
            ['%s = %r' % (k, getattr(self, k))
                for k in self.fields if hasattr(self, k)])
