#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

from __future__ import unicode_literals

version_info = ('0', '1', '1', '1')
# ...setuptools/dist.py:282:
# UserWarning: Normalizing '0.1.1-1' to '0.1.1.post1'
# __version__ = '.'.join(version_info[0:3]) + '-' + version_info[3]

__version__ = '.'.join(version_info)
