# clustercron/compat.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

'''
clustercron.compat
------------------
'''

import sys

PY3 = sys.version_info[0] == 3
OLD_PY2 = sys.version_info[:2] < (2, 6)
