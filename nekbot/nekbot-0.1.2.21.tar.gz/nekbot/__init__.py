#!/usr/bin/env/python
# coding=utf-8
import os
import gettext

MODULE = 'nekbot'
LOCALES_DIR = 'locales'
__version__ = 'Mirai 0.1'
__author__ = 'nekmo'
__dir__ = os.path.abspath(os.path.dirname(__file__))

gettext.bindtextdomain(MODULE) #  os.path.join(__dir__, LOCALES_DIR)
gettext.textdomain(MODULE)
_ = gettext.gettext
_n = gettext.ngettext

from nekbot.conf import settings
from nekbot.core import NekBot
from nekbot.protocols import Protocols

t = gettext.install('nekbot', LOCALES_DIR)


if '__path__' in globals():
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)