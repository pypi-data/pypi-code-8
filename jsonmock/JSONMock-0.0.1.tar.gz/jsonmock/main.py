from __future__ import absolute_import
__author__ = 'anass'

import os
import sys


if __package__ == '':
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

from jsonmock import serve


def main():
    if len(sys.argv) == 2:
        sys.exit(serve(sys.argv[1]))
    else:
        raise Exception('Please enter a valid command like this: JSONMock path/to/your/json.json ')

