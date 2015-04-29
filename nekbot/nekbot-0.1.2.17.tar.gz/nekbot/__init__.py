#!/usr/bin/env/python
# coding=utf-8

__version__ = 'Mirai 0.1'
__author__ = 'nekmo'

from nekbot.conf import settings
from nekbot.core import NekBot
from nekbot.protocols import Protocols

if '__path__' in globals():
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)