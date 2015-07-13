from PyQt5.QtCore import QBasicTimer, QTimer
import time


class QBasicTimerWithPause(QBasicTimer):
    def __init__(self, parent):
        QBasicTimer.__init__(self)
        self.startTime = 0
        self.interval = 0
        self.is_started = False
        self.is_paused = False
        self.parent = parent

    def start(self, interval):
        self.is_started = True
        self.interval = interval
        self.startTime = time.time()
        QBasicTimer.start(self, interval, self.parent)
        print("timer")
        # one-shot

    def pause(self):
        if self.is_started:
            self.stop()
            self.is_paused = True
            self.is_started = False
            # self.elapsedTime = self.startTime - time.time()
            # self.startTime -= self.elapsedTime

            # # time() returns float secs, interval is int msec
            # self.interval -= int(self.elapsedTime * 1000)

    def resume(self):
        # if not self.isActive():
        if not self.is_started and self.is_paused:
            self.is_paused = False
            self.is_started = True
            self.start(self.interval)

            self.elapsedTime = self.startTime - time.time()
            self.startTime -= self.elapsedTime

            # time() returns float secs, interval is int msec
            self.interval -= int(self.elapsedTime * 1000)


class QTimerWithPause(QTimer):
    def __init__(self, parent=None):
        QTimer.__init__(self, parent)
        self.startTime = 0
        self.interval = 0
        self.is_started = False
        self.is_paused = False

    def start(self, interval, method):
        self.interval = interval
        self.startTime = time.time()
        self.is_started = True

        # one-shot
        # QTimer.start(self, interval, True)
        self.setSingleShot(True)
        QTimer.singleShot(self.interval, method)

    def pause(self):
        if self.is_started:
            self.stop()
            self.is_started = False
            self.is_paused = True

            # self.elapsedTime = self.startTime - time.time()
            # self.startTime -= self.elapsedTime

            # # time() returns float secs, interval is int msec
            # self.interval -= int(self.elapsedTime * 1000)

    def resume(self, method):
        # if not self.isActive():
        if not self.is_started and self.is_paused:
            self.is_paused = False
            self.is_started = True
            self.start(self.interval, method)
            
            self.elapsedTime = self.startTime - time.time()
            self.startTime -= self.elapsedTime

            # time() returns float secs, interval is int msec
            self.interval -= int(self.elapsedTime * 1000)
