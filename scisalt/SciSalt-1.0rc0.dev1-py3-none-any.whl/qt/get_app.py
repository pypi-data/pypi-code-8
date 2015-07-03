import sys
from PyQt4 import QtGui


def get_app(argv=sys.argv):
    global app
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication(argv)
    return app
