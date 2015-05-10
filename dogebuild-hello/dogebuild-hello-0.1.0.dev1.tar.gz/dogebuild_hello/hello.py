from dogebuild.plugin.interfaces import *


class HelloTask(Task):
    def __init__(self, message=None):
        if message is None:
            message = "Hi! This is default hello plugin message!"
        self.message = message

    def run(self):
        print(self.message)


class Hello(Plugin):
    def get_active_tasks(self):
        return [HelloTask(self.message)]
