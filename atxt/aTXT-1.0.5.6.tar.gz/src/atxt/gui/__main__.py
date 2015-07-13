#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

import sys

from PySide import QtGui
from atxt.log_conf import Logger
from window import Window


log = Logger.log
__all__ = ['run']


def run():
    app = QtGui.QApplication(sys.argv)
    wds = Window()
    wds.show()
    sys.exit(app.exec_())
    del wds


if __name__ == '__main__':
    run()
