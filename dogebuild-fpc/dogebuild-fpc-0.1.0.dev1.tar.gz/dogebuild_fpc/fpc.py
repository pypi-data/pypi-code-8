from dogebuild.plugin.interfaces import *

import subprocess


class FpcTask(Task):
    def __init__(self, dir):
        self.dir = dir

    def run(self):
        subprocess.call(["fpc", str(self.dir)])


class Fpc(Plugin):
    def get_active_tasks(self):
        return [FpcTask(self.dir)]
