from __future__ import absolute_import
__author__ = 'anass'

import os
import sys


if __package__ == '':
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

from jsonmock import serve

if __name__ == '__main__':
    sys.exit(serve('test/file.json'))
