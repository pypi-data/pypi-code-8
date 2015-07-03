#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto


import os

from atxt.check import pdftopng, pdftotext, tesseract
from log_conf import Logger


log = Logger.log



basedir_ = os.path.abspath(__file__)


class Office(object):

    @property
    def msword(self):
        return self._msword

    def __init__(self, msword=None):
        if isinstance(msword, bool):
            try:
                self._msword = self.open()
            except ImportError, e:
                log.error('word office doesnt run. %s' % e)
        else:
            self._msword = msword

    def open(self):
        try:
            log.debug('calling win32 package')
            from win32com import client
        except ImportError, e:
            log.error(e)
            raise e
        try:
            self._msword = client.DispatchEx('Word.Application')
            self._msword.Visible = False
        except Exception, e:
            log.critical('impossible dispatching msword')
            raise e
        log.debug('successful dispatching of msword')
        return self._msword

    def close(self):
        log.debug('closing msword')
        try:
            self._msword.Quit()
        except Exception, e:
            log.debug('fail to close msword: %s'%e)

