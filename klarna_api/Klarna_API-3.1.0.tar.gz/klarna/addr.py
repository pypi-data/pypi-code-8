'''Klarna API - Address

Provides Address class which holds a single address of a person or company
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

__all__ = ('Address',)

from .error import KlarnaException, UnknownCountry
from .const import *
from .util import basestring

import re


class Address(object):
    fields = (
        'email', 'telno', 'cellno', 'fname', 'lname', 'company', 'careof',
        'street', 'house_number', 'house_extension', 'zip', 'city', 'country'
    )

    @property
    def email(self):
        'Email address'
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def telno(self):
        'Phone number'
        return self._telno

    @telno.setter
    def telno(self, value):
        self._telno = value

    @property
    def cellno(self):
        'Cellphone number'
        return self._cellno

    @cellno.setter
    def cellno(self, value):
        self._cellno = value

    @property
    def fname(self):
        'First name'
        return self._fname

    @fname.setter
    def fname(self, value):
        self._fname = value

    @property
    def lname(self):
        'Last name'
        return self._lname

    @lname.setter
    def lname(self, value):
        self._lname = value

    @property
    def company(self):
        'Company name'
        return self._company

    @company.setter
    def company(self, value):
        self.is_company = True
        self._company = value

    @property
    def careof(self):
        'Care of, C/O'
        return self._careof

    @careof.setter
    def careof(self, value):
        self._careof = value

    @property
    def street(self):
        'Street address'
        return self._street

    @street.setter
    def street(self, value):
        self._street = value

    @property
    def zip(self):
        'Zip Code'
        return self._zip

    @zip.setter
    def zip(self, value):
        self._zip = value

    @property
    def city(self):
        'City'
        return self._city

    @city.setter
    def city(self, value):
        self._city = value

    @property
    def country(self):
        'Country code'
        return self._country

    @country.setter
    def country(self, value):
        try:
            self._country = lookup(Countries, value)
        except ValueError:
            raise UnknownCountry(value)

    @property
    def house_number(self):
        'House number'
        return self._house_number

    @house_number.setter
    def house_number(self, value):
        self._house_number = value

    @property
    def house_extension(self):
        'House Extension'
        return self._house_extension

    @house_extension.setter
    def house_extension(self, value):
        self._house_extension = value

    def __init__(self, **kwargs):
        self.is_company = False
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)

    def __iter__(self):
        for k in self.fields:
            if hasattr(self, k):
                yield k

    def __getitem__(self, key):
        return getattr(self, key, '')

    def __contains__(self, key):
        return getattr(self, key, None)

    def __repr__(self):
        return '(Addr %s)' % ', '.join(
            ['%s = %r' %
                (k, getattr(self, k)) for k in self.fields if hasattr(self, k)])
