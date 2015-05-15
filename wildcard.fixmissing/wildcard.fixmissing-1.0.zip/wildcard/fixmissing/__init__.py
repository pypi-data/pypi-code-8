import os
from wildcard.fixmissing import interfaces
from wildcard.fixmissing import objects
from zope.interface import Interface
from zope.dottedname.resolve import resolve
import logging
import new
import sys
from persistent import Persistent


logger = logging.getLogger('wildcard.fixmissing')


def alias_module(name, target):
    parts = name.split('.')
    i = 0
    module = None
    while i < len(parts) - 1:
        i += 1
        module_name = '.'.join(parts[:i])
        try:
            __import__(module_name)
        except ImportError:
            new_module = new.module(module_name)
            sys.modules[module_name] = new_module
            if module is not None:
                setattr(module, parts[i - 1], new_module)
        module = sys.modules[module_name]

    setattr(module, parts[-1], target)
    # also make sure sys.modules is updated
    sys.modules[module_name + '.' + parts[-1]] = target


def initialize(context):
    for key in os.environ.keys():
        if not key.startswith('MISSING_'):
            continue
        class_name = key.replace('MISSING_', '')
        value = os.environ[key]
        replacement = None
        if '=' not in value:
            # generate missing
            if class_name[0] == 'I':
                # interface class
                replacement = interfaces
                if not hasattr(interfaces, class_name):
                    setattr(interfaces, class_name, Interface)
            else:
                replacement = objects
                if not hasattr(objects, class_name):
                    setattr(objects, class_name, Persistent)
        else:
            value, replace_string = value.split('=', 1)
            try:
                replacement = resolve(replace_string)
            except:
                logger.warn('Could not import replacement module %s' % replace_string)

        if replacement:
            logger.info('aliasing module for %s.%s' % (
                value, class_name))
            alias_module(value, replacement)
