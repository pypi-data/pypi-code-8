import os
import time
import subprocess
import signal
import psutil
import re
import pyuv
import sys
import saddle_service_logs
import multiprocessing
from saddle_dir import SaddleDir
from saddle import libfaketime


class SaddleServiceException(Exception):
    pass


# TODO: Allow stopping and starting and *waiting* of services from other thread. Use queue. Make this thread methods for stop/start private.
# TODO: Allow services to be considered started after a preset number of seconds? Use test function?

class Service(object):
    def __init__(self, service_engine, name, command, readysignal, directory=None, no_libfaketime=False, env_vars=None, needs=None):
        if "[" in name or "]" in name:
            raise SaddleServiceException("[ and ] characters not allowed in service name")

        if " " in name:
            raise SaddleServiceException("Spaces are not allowed in service names.")

        if name in ["Test", "Saddle", "Harness", ]:
            raise SaddleServiceException("{0} is not an allowed service name.".format(name))

        self.service_engine = service_engine

        if directory is None:
            self.directory = service_engine.saddledir()
        else:
            self.directory = directory

        self.name = name
        self.command = command

        self.env_vars = {} if env_vars is None else env_vars

        if not no_libfaketime:
            faketime_filename = '{}/faketime.txt'.format(service_engine.saddledir())

            self.env_vars = dict(
                self.env_vars.items() + libfaketime.get_environment_vars(faketime_filename).items()
            )

        self.term_signal_sent = False
        self.logs = saddle_service_logs.ServiceLogs(name)
        self.loaded = False
        self.ready = False
        self.started = False
        self.needs = needs
        self.readysignal = readysignal
        self.loop = None
        self.setup_finished = False
        self.poststart_started = False
        if "logline" in readysignal:
            self.ready_check = readysignal['logline']
        else:
            self.ready_check = lambda line: False

    def no_prerequisites(self):
        return self.needs is None or self.needs == []

    def attach_to_service_engine(self, service_engine):
        self.service_engine = service_engine
        self.logline = service_engine.logline
        self.warnline = service_engine.warnline
        self.logs.set_logfilename(service_engine._logfilename())
        self.loop = service_engine.loop

    def setup(self):
        pass

    def run_setup(self):
        try:
            sys.stdout = open(self.service_engine._stdlogdir() + os.sep + self.name.lower() + "_setup.out", "a", 0)
            sys.stderr = open(self.service_engine._stdlogdir() + os.sep + self.name.lower() + "_setup.err", "a", 0)
            self.setup()
        except Exception, e:
            self.warnline("Exception during 'Setup {}':".format(self.name))
            self.warnline(str(e))
            self.service_engine.ready_queue.put("ERROR")

    def start(self):
        self.started = True
        self.setup_runner = multiprocessing.Process(target=self.run_setup)
        self.setup_runner.start()

    def poststart(self):
        pass

    def run_poststart(self):
        try:
            sys.stdout = open(self.service_engine._stdlogdir() + os.sep + self.name.lower() + "_poststart.out", "a", 0)
            sys.stderr = open(self.service_engine._stdlogdir() + os.sep + self.name.lower() + "_poststart.err", "a", 0)
            self.poststart()
        except Exception, e:
            self.warnline("Exception during 'Poststart {}':".format(self.name))
            self.warnline(str(e))
            self.service_engine.ready_queue.put("ERROR")

    def poststart_run(self):
        self.poststart_runner = multiprocessing.Process(target=self.run_poststart)
        self.poststart_runner.start()

    def run(self, command, shell=False, ignore_errors=False, stdin=False):
        """Run a command for this service."""
        try:
            subprocess.check_call(
                command,
                stdout=sys.stdout,
                stderr=sys.stderr,
                stdin=sys.stdin if stdin else None,
                env=self.env_vars,
                shell=shell
            )
        except subprocess.CalledProcessError:
            if ignore_errors:
                pass
            else:
                raise

    def start_process(self):
        self.logline("Starting {0}".format(self.name))
        os.chdir(self.directory)
        self.process = subprocess.Popen(
            self.command,
            bufsize=0,                  # Ensures that all stdout/err is pushed to us immediately.
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env_vars,
            preexec_fn=os.setpgrp       # Ctrl-C signal is not passed on to the process.
        )

        self.stdout_pipe = pyuv.Pipe(self.loop)
        self.stdout_pipe.open(self.process.stdout.fileno())

        self.stderr_pipe = pyuv.Pipe(self.loop)
        self.stderr_pipe.open(self.process.stderr.fileno())

    def stop(self):
        """Ask politely, first, with SIGINT and SIGQUIT."""
        if hasattr(self, 'process'):
            if self.process.poll() is None:
                self.logline("Stopping {0}".format(self.name))
                self.term_signal_sent = True

                # Politely ask all child processes to die first
                for childproc in psutil.Process(self.process.pid).get_children(recursive=True):
                    childproc.send_signal(signal.SIGINT)

                self.process.send_signal(signal.SIGINT)
                self.process.send_signal(signal.SIGQUIT)
            else:
                self.warnline("{0} stopped prematurely.".format(self.name))
        else:
            self.warnline("{0} was never successfully started.".format(self.name))

    def is_dead(self):
        if not hasattr(self, 'process'):
            return True
        else:
            return self.process.poll() is not None

    def kill(self):
        """Murder the children of this service in front of it, and then murder the service itself."""
        if not self.is_dead():
            self.warnline("{0} did not shut down cleanly, killing.".format(self.name))
            for child in psutil.Process(self.process.pid).get_children(recursive=True):
                os.kill(child.pid, signal.SIGKILL)
            self.process.kill()
