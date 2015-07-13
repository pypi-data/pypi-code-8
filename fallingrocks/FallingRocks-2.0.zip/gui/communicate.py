from PyQt5.QtCore import QObject, pyqtSignal


class Communicate(QObject):
    def __init__(self):
        super(Communicate, self).__init__()
    move_left = pyqtSignal()
    move_right = pyqtSignal()
    pause = pyqtSignal()
    restart = pyqtSignal()
    exit = pyqtSignal()
    win = pyqtSignal()
    message_statusbar = pyqtSignal(str)
