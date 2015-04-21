import subprocess
import os
import saddle
import shutil
import subprocess
import sys
import contextlib


class CeleryService(saddle.Service):
    def __init__(self, service_engine, python=sys.executable, beat=False, app=None, loglevel="INFO", concurrency=2, broker=None, needs=None):
        self.python = python
        self.app = app
        self.app_option = [] if app is None else ['--app={}'.format(app), ]

        command = [python, "-u", '-m', 'celery', 'worker', ] \
            + self.app_option \
            + ([] if beat == False else ['--beat', ]) \
            + (['--loglevel={}'.format(loglevel), ]) \
            + ([] if broker is None else ['--broker={}'.format(broker), ]) \
            + (["--concurrency={}".format(concurrency), ])

        super(CeleryService, self).__init__(
            service_engine,
            "Celery", command,
            {'logline': lambda line: "Connected to" in line,},
            needs=needs,
            directory=service_engine.directory
        )

    def celery(self, command, ignore_errors=False):
        command = command.split(' ') if type(command) == str else command
        self.run([self.python, "-u", '-m', 'celery', ] + self.app_option + command, ignore_errors=ignore_errors)

    def inspect(self, command):
        command = command.split(' ') if type(command) == str else command
        self.celery(['inspect', ] + command)

    def control(self, command):
        command = command.split(' ') if type(command) == str else command
        self.celery(['inspect', ] + command)

    def status(self):
        self.celery(['status', ])

    def help(self):
        self.celery(['help', ], ignore_errors=True)
