# -*- coding: utf-8 -*-
''' Klarna API - checkout - checkout loader

Provides a method for dynamicly loading checkout extensions
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

__all__ = ('get_checkout_classes',)

import logging
from .checkouthtml import CheckoutHTML

logger = logging.getLogger('klarna')


def get_checkout_classes():
    ''' Finds all checkout classes '''

    import os
    import sys
    import imp
    import glob

    classes = []
    modules = ['__init__']

    base = os.path.dirname(__file__)

    for (suffix, mode, t) in imp.get_suffixes():
        for f in glob.glob(os.path.join(base, '*%s' % suffix)):
            name = os.path.basename(f)[:-len(suffix)]
            if name in modules:
                continue
            fullname = '%s.%s' % (__name__, name)
            fp, pathname, description = imp.find_module(name, [base])

            try:
                module = sys.modules[fullname]
                logger.debug('Checkout HTML module (%s) already loaded' % name)
            except:
                # Try to import the module
                (fp, pathname, description) = imp.find_module(name, [base])
                logger.debug('Loading Checkout HTML module from %s' % pathname)
                try:
                    module = imp.load_module(fullname, fp, pathname, description)
                finally:
                    if fp:
                        fp.close()
            modules.append(name)

            # Find all CheckoutHTML subclasses
            for export in dir(module):
                o = getattr(module, export)
                try:
                    if o is not CheckoutHTML and issubclass(o, CheckoutHTML):
                        classes.append(o)
                except TypeError:
                    # not a class
                    pass

    return classes
