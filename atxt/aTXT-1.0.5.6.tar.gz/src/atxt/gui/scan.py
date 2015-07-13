#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:17:19
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-04 15:02:15
import os

from PySide import QtCore
from atxt.log_conf import Logger
from atxt.walking import walk, size_str
from atxt.utils import extract_ext


log = Logger.log


class Scan(QtCore.QThread):
    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):
        log.debug('created QThread for Scan')
        opts = self.window.options()
        conta, tsize = 0, 0
        assert len(opts['<path>']) == 1
        for _, _, files in walk(opts['<path>'][0], level=opts['--depth']):
            if not self.FLAG:
                return
            for f in files:
                if extract_ext(f.name) not in opts['tfiles']:
                    continue
                if os.access(f.path, os.R_OK):
                    try:
                        log.info("{c:3d} | {p}".format(c=conta+1, p=f.path))
                    except Exception, e:
                        log.info("{c:3d} |".format(c=conta+1))
                        log.debug(f.path)
                    try:
                        tsize += os.path.getsize(f.path)
                        conta += 1
                    except Exception, e:
                        log.debug('os.path.getsize(f.path) failed:%s' % e)

        log.info('Number of files estimates : %d' % conta)
        log.info('Size on disk estimates : %s' % size_str(tsize))

        self.window.totalfiles = conta
        self.exit()
