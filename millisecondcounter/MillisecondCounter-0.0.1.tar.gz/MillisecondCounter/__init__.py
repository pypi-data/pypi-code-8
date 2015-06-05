from datetime import datetime


class ExecutionCounter():

    def __init__(self):
        self.st = datetime.now()

    def finish(self):
        ft = datetime.now() - self.st
        return int(ft.total_seconds() * 1000)
