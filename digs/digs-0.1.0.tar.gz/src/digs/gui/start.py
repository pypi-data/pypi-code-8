#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide import QtCore
from digs.logger import Logger
from digs.worker import scraper


log = Logger.log


class Start(QtCore.QThread):
    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):
        log.debug('created QThread for Start')
        opts = self.window.options()
        try:
            scraper(opts['<url>'], opts['--depth'],
                    opts['--to'], opts['--sameroot'], opts['-o'])
        except Exception, e:
            log.error(e)
        self.exit()
        return
