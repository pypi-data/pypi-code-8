# -*- coding: utf-8 -*-
''' Klarna API - pclasses - Storage

Defines the shared interface of all PClass storages
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

__all__ = ('PCStorage',)

import logging

from ..error import KlarnaException
from ..pclass import PClass

logger = logging.getLogger('klarna')


class PCStorage(object):
    def add_pclass(self, pclass):
        if not isinstance(pclass, PClass):
            raise TypeError("Supplied pclass object is not an PClass instance")

        if not hasattr(self, '_pclasses'):
            self._pclasses = {}

        # Sanity checks
        if getattr(pclass, 'description', None) is None:
            logger.warning("Missing description on PClass, skipping")
            return
        if getattr(pclass, 'type', None) is None:
            logger.warning("Missing type on PClass, skipping")
            return

        if pclass.eid not in self._pclasses:
            self._pclasses[pclass.eid] = {}
        logger.debug("Adding pclass %s", pclass)
        self._pclasses[pclass.eid][pclass.id] = pclass

    def get_pclass(self, id, eid):
        ''' Get PClass by id and eid '''

        if not hasattr(self, '_pclasses'):
            raise KlarnaException('No PClasses found')

        try:
            pclass = self._pclasses[eid][id]
        except KeyError:
            if eid not in self._pclasses:
                raise KlarnaException("No such EStore ID (%s)" % eid)
            raise KlarnaException("Nu such PClass ID (%s)" % id)

        if not pclass.is_valid():
            raise KlarnaException("Invalid PClass")

        return pclass

    def get_pclasses(self, country, type=None):
        ''' Get dictionaries with PClass instances mapped to eid and pclass id
            filtered by by country and type (if specified)
        '''

        if not hasattr(self, '_pclasses'):
            raise KlarnaException('No PClasses found')

        country = country.upper()
        out = {}
        for eid, pclasses in self._pclasses.items():
            for pid, pclass in pclasses.items():
                if not pclass.is_valid():
                    continue

                if type is not None and pclass.type != type:
                    continue

                if pclass.country != country:
                    continue

                if eid not in out:
                    out[eid] = {}
                out[eid][pclass.id] = pclass
        return out

    def load(self, uri):
        raise KlarnaException("load not implemented by PCStorage subclass")

    def save(self, uri):
        raise KlarnaException("save not implemented by PCStorage subclass")

    def clear(self, uri):
        raise KlarnaException("clear not implemented by PCStorage subclass")
