# -*- coding: utf-8 -*-
''' Klarna API - pclasses - JSON Storage

Defines the PCStorage implementation storing pclasses using JSON
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

__all__ = ('JSONStorage',)

from .storage import PCStorage, PClass
from ..error import KlarnaException
import os
import json


class JSONStorage(PCStorage):
    ''' Stores PClasses in json
        this class works with the same structure as the php-api
    '''

    def load(self, uri):
        with open(uri, 'r') as fp:
            data = json.load(fp)

        # add pclasses from json-data
        for eid, pclasses in data.items():
            for pclass in pclasses:
                pclass = PClass(**pclass)
                self.add_pclass(pclass)

    def save(self, uri):
        if not hasattr(self, '_pclasses'):
            raise KlarnaException('No PClasses found')

        # Convert pclass database to a structure that json can dump
        output = {}
        for eid, pclasses in self._pclasses.items():
            for pclass in pclasses.values():
                if eid not in output:
                    output[eid] = []
                output[eid].append(dict(list(pclass)))

        string = json.JSONEncoder().encode(output)
        with open(uri, 'w') as fp:
            fp.write(string)

    def clear(self, uri):
        if hasattr(self, '_pclasses'):
            del self._pclasses
        if os.path.exists(uri):
            os.unlink(uri)
