#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PySide import QtCore
from atxt.lib import aTXT
from atxt.log_conf import Logger
from atxt.workers import run_files, run_paths


log = Logger.log


class Start(QtCore.QThread):
    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):
        log.debug('created QThread for Start')
        opts = self.window.options()

        manager = aTXT()
        manager.options = opts
        opts = manager.options

        res, total, finished = 0, 0, 0

        if manager.options['--file']:
            res = run_files(manager, total, finished)
            if res and len(res) == 2:
                total += res[0]
                finished += res[1]

        if manager.options['--path']:
            res = run_paths(manager, total, finished)
            if res and len(res) == 2:
                total += res[0]
                finished += res[1]

        log.debug("Start finished")
        log.info("Total Files: %s" % str(total))
        log.info("Files Finished: %s" % str(finished))
        log.info("Files Unfinished: %s" % str(total - finished))
        self.exit()
        return
