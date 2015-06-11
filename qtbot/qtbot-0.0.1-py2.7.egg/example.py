from PyQt4 import QtGui
import qtbot

app = QtGui.QApplication([])
dlg = QtGui.QFileDialog()
fname = '/foo/bar'
qtbot.handle_modal_widget(fname, wait=False)
dlg.exec_()
assert fname == dlg.selectedFiles()[0];