# -*- coding: utf-8 -*-
from __future__ import absolute_import
def setup():
    from ._exthook import ExtensionImporter
    importer = ExtensionImporter(['kyper-%s', 'kyper_%s'], __name__)
    importer.install()


setup()
del setup
