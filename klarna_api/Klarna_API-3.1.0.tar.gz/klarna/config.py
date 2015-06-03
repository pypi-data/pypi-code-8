# -*- coding: utf-8 -*-
''' Klarna API - Config

Defines a Config class that load and saves configuration as json
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

__all__ = ('Config',)

import json
import logging

logger = logging.getLogger('klarna')


class Config(dict):
    ''' Configuration holder for the Klarna instance.

        backed by json on file if Config.store is set to True
    '''

    store = True

    def __init__(self, file=None, **kwargs):
        ''' if a single argument is given it's used as the filename to load
            the configuration from. Else the config is populated from the keyword
            arguments
        '''

        self.file = file

        # Load the file if any
        try:
            if self.file is not None:
                with open(self.file) as fp:
                    self.update(json.load(fp))
        except:
            logger.warn('Could not load config', exc_info=True)

        # Fill the config with values from keyword arguments
        self.update(kwargs)

    def __del__(self):
        try:
            if self.store and self.file is not None:
                self.save()
        except IOError:
            logger.warn('Could not save config', exc_info=True)

    def save(self):
        string = json.JSONEncoder().encode(self)
        with open(self.file, 'w') as fp:
            fp.write(string)
