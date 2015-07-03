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
from atxt.walking import walk, size_str
from atxt.utils import extract_ext


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

        for root, _, files in walk(opts['<path>'][0],
                                   level=opts['--depth']):
            if not self.FLAG:
                # self._part(0)
                self._end_process(True)
                return
            for f in files:
                if extract_ext(f.name) not in opts['tfiles']:
                    continue
                if os.access(f.path, os.R_OK):
                    try:
                        log.info("{c:2d} | {p}".format(c=conta+1, p=f.path))
                    except Exception, e:
                        log.debug(e)
                    self._cursor_end.emit(True)
                    try:
                        tsize += os.path.getsize(f.path)
                        conta += 1
                    except Exception, e:
                        log.debug('os.path.getsize(f.path) failed')

        log.info('Number of files estimates : %d' % conta)
        log.info('Size on disk estimates : %s' % size_str(tsize))

        self.window.totalfiles = conta
        self._cursor_end.emit(True)
        # self._part.emit(100)
        # self._ready.emit(True)
        # self._end_process.emit(True)
        self.exit()
