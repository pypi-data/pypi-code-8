#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:17:19
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-30 14:12:25
import os

from PySide import QtCore
from atxt.encoding import encoding_path
from atxt.log_conf import Logger
import atxt.walking as wk


log = Logger.log



class Scan(QtCore.QThread):
    # _end_process = QtCore.Signal(bool)
    _cursor_end = QtCore.Signal(bool)
    # _part = QtCore.Signal(int)
    # _ready = QtCore.Signal(bool)

    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):
        log.debug('created QThread for Scan')
        opts = self.window.options()

        # self._part.emit(0)

        conta, tsize = 0, 0
        # FIXME
        # factor = 0.1 if opts['depth'] != 0 else 0.01 * opts['depth']
        assert len(opts['<path>']) == 1

        for root, _, files in wk.walk(opts['<path>'][0],
                                      sdirs=[],
                                      level=opts['--depth'],
                                      tfiles=opts['tfiles']):
            if not self.FLAG:
                # self._part(0)
                self._end_process(True)
                return
            for f in files:
                # self._part.emit(conta * factor)
                file_path = os.path.join(root, f.name)
                file_path = encoding_path(file_path)
                if os.access(file_path, os.R_OK):
                    conta += 1
                    try:
                        log.info("[%d] : %s" % (conta, file_path))
                    except Exception, e:
                        log.debug(e)
                    self._cursor_end.emit(True)
                    try:
                        tsize += os.path.getsize(file_path)
                    except Exception, e:
                        log.debug('os.path.getsize(file_path) failed')

        log.info('[Number of files estimates] : %d' % conta)
        log.info('[Size on disk estimates]: %s' % wk.size_str(tsize))

        self.window.totalfiles = conta
        self._cursor_end.emit(True)
        # self._part.emit(100)
        # self._ready.emit(True)
        # self._end_process.emit(True)
        self.exit()
