# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import imp
import sys

from django.db import models


def _import_non_local(name, custom_name=None):
    custom_name = custom_name or name

    f, pathname, desc = imp.find_module(name, sys.path[1:])
    module = imp.load_module(custom_name, f, pathname, desc)
    f.close()

    return module


_pp = _import_non_local('pprint', 'std_pprint')


class DjangoUnicodePrettyPrinter(_pp.PrettyPrinter):
    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, unicode):
            return obj.encode('utf8'), True, False
        return _pp.PrettyPrinter.format(self, obj, context, maxlevels, level)

    def pprint(self, obj):
        _pp.PrettyPrinter.pprint(self, obj)
        if isinstance(obj, models.Model):
            _pp.PrettyPrinter.pprint(self, {
                k: v for k, v in obj.__dict__.iteritems()
                if not k.startswith('_')
            })


pprint = DjangoUnicodePrettyPrinter().pprint