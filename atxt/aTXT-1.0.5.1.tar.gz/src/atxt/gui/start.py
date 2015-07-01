#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-20 23:16:24
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-30 19:27:41

from PySide import QtCore
from atxt.lib import aTXT
from atxt.log_conf import Logger
from atxt.workers import run_files, run_paths


log = Logger.log



class Start(QtCore.QThread):
    # _end_process = QtCore.Signal(bool)
    _cursor_end = QtCore.Signal(bool)  # for the textbox

    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):

        log.debug('created QThread for Start')

        self.window._btn_start.setEnabled(False)
        self.window._btn_scan.setEnabled(False)

        opts = self.window.options()

        manager = aTXT()
        manager.options = opts
        opts = manager.options

        # for k in opts.keys():
        #     log.critical((k, opts[k]))

        res = 0
        total = 0
        finished = 0

        if manager.options['--file']:
            res = run_files(manager, thread=self)
            if res and len(res) == 2:
                total += res[0]
                finished += res[1]

        if manager.options['--path']:
            res = run_paths(manager, thread=self)
            if res and len(res) == 2:
                total += res[0]
                finished += res[1]


        log.debug("Start finished")
        log.info("Total Files: %s" % str(total))
        log.info("Files Finished: %s" % str(finished))
        log.info("Files Unfinished: %s" % str(total - finished))

        self._cursor_end.emit(True)
        self.window._btn_start.setEnabled(True)
        self.window._btn_scan.setEnabled(True)
        # self.window._btn_stop.setEnabled(False)
        self.exit()
        return
