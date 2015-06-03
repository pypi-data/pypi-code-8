# -*- coding: utf-8 -*-
''' Klarna API - pclasses - storage loader

Provides a method for dynamicly loading pclass storages
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

__all__ = ('get_pclass_storage',)

import logging
from .storage import PCStorage
from ..error import KlarnaException

logger = logging.getLogger('klarna')


def ispcstorage(o):
    '''Check if the object is a pcstorage type'''

    return (isinstance(o, type) and
            o is not PCStorage and
            issubclass(o, PCStorage))


def get_pclass_storage(name):
    ''' Finds and loads a PClass storage backend by name '''

    logger.info('Using PClass storage module %s' % name)

    # A non empty fromlist makes import return the deepest module as it
    # assumes we are going to import some names directly
    try:
        module = __import__('klarna.pclasses.' + name + 'storage',
                            fromlist=[''])
    except ImportError:
        module = __import__(name, fromlist=[''])

    # Find the first PCStorage subclass and instanciate it
    names = getattr(module, '__all__', None) or dir(module)
    for export in names:
        o = getattr(module, export)
        if ispcstorage(o):
            return o()

    raise KlarnaException("No PCStorage subclass found in %r" % module)
