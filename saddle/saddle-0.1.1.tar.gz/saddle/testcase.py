from IPython.terminal.embed import InteractiveShellEmbed
from IPython.core import ultratb
from saddle_traceback import SaddleTraceback
from saddle_dir import SaddleDir
from service_engine import ServiceEngine
import unittest
import datetime
import time
import signal
import os
import sys
import IPython
import multiprocessing
import humanize
import colorama
import shutil
import fcntl
import inspect
import traceback
import subprocess

# TODO : Allow stopping, starting, restarting and waiting until stop/start is finished.
# TODO : Create whole class for saddledir that creates, gets path, removes, pgid, etc.
# TODO : Test access to the internet and fail fast.

class TestCase(unittest.TestCase):
    """Base test case class for a saddle functional test."""
    fixtures = None
    timedelta = datetime.timedelta(0)

    def configure_services(self):
        pass

    def log(self, message):
        """Print a normal priority message."""
        sys.stdout.write(message + u'\n')

    def warn(self, message):
        """Print a higher priority message."""
        sys.stderr.write(message + u'\n')

    def _shutdown_old_process(self):
        if os.path.exists(self.saddle_dir.pgid()):
            with open(self.saddle_dir.pgid(), "r") as pgid_file_handle:
                pgid = pgid_file_handle.read()

            try:
                pgid_int = int(pgid)
            except ValueError:
                self.warn("""Could not interpret PGID file contents: "{0}".""".format(pgid))
                sys.exit(1)

            try:
                os.killpg(pgid_int, signal.SIGINT)
                self.warn("Shutting down old test...")
            except OSError, e:
                if e.strerror == 'No such process':
                    return

            time.sleep(self.service_engine.timeout)

            try:
                os.killpg(pgid_int, signal.SIGKILL)
                self.warn("Killing old test...")
                os.remove(self.saddle_dir.pgid())
            except OSError, e:
                self.warn("Error killing old process group.")

    def redirect_stdout(self):
        """Redirect stdout to file so that it can be tailed and aggregated with the other logs."""
        self.hijacked_stdout = sys.stdout
        self.hijacked_stderr = sys.stderr
        # 0 must be set as the buffer, otherwise lines won't get logged in time.
        sys.stdout = open(self.saddle_dir.testcaseout(), "a", 0)
        sys.stderr = open(self.saddle_dir.testcaseerr(), "a", 0)

    def unredirect_stdout(self):
        """Redirect stdout back to stdout."""
        sys.stdout = self.hijacked_stdout
        sys.stderr = self.hijacked_stderr

    def op(self, trigger=""):
        """Open this test with op."""
        if subprocess.call(['which op'], shell=True) == 0:
            subprocess.call("op {} {}".format(sys.argv[0], trigger), shell=True)
        else:
            self.warn("""op not installed! 'sudo pip install op' to use.""")

    def setUp(self):
        """Generic functional test set up."""
        self.saddle_dir = SaddleDir(self.project_directory)
        self.service_engine = ServiceEngine(self)
        self.services = self.service_engine.services
        self.configure_services()
        # TODO: Raise exception if two of the services are named the same

        for service in self.service_engine.all_services():
            service.logs.set_logfilename(self.service_engine._logfilename())

        self.saddle_dir.clean()

        self._shutdown_old_process()

        with open(self.saddle_dir.pgid(), "w") as pgid_file_handle:
            pgid_file_handle.write(str(os.getpgid(os.getpid())))

        self.ready_queue = multiprocessing.Queue()
        self.messages_to_service_engine = multiprocessing.Queue()

        service_process_args = (self.ready_queue, self.messages_to_service_engine, self.fixtures)

        self._service_process = multiprocessing.Process(target=self.service_engine.start, args=service_process_args)
        self._service_process.start()
        self.redirect_stdout()


        what_happened = self.ready_queue.get()
        if what_happened == "READY":
            return
        elif what_happened == "ERROR":
            self.shutdown()
            raise RuntimeError("Service engine received an error during set up.")
        elif what_happened == "TIMEOUT":
            self.shutdown()
            raise RuntimeError("Service engine timed out starting up.")

    def time_travel(self, delta):
        """Mock moving forward or backward in time by shifting the system clock fed to the services tested."""
        self.timedelta = self.timedelta + delta
        self.log("Time traveling to {0}".format(humanize.naturaltime(self.now())))
        # TODO: Move some of this code to libfaketime __init__.py
        with open(self.saddle_dir.faketime(), "w") as faketimetxt_handle:
            faketimetxt_handle.write("@" + self.now().strftime("%Y-%m-%d %H:%M:%S"))

    def now(self):
        """Get a current (mocked) datetime. This will be the current datetime unless you have time traveled."""
        return datetime.datetime.now() + self.timedelta

    def ipython(self, message=None):
        """Pause a test and break into an IPython shell."""
        frame = inspect.stack()[1][0] # 1 = Frame above this one = calling method, 0 = Get Frame
        self._launch_ipython(frame, message)

    def _launch_ipython(self, frame, message=None):
        self.messages_to_service_engine.put("IPYTHONON")
        sys.stdout.write(colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL)
        sys.stderr.write(colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL)
        self.unredirect_stdout()

        # Make stdin blocking - so that redis-cli (among others) can work.
        flags = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
        if flags & os.O_NONBLOCK:
            fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, flags & ~os.O_NONBLOCK)

        InteractiveShellEmbed()(message, local_ns=frame.f_locals, global_ns=frame.f_globals)

        # Make stdin non-blocking again
        flags = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
        if flags & ~os.O_NONBLOCK:
            fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, flags | os.O_NONBLOCK)
        self.messages_to_service_engine.put("IPYTHONOFF")
        self.redirect_stdout()

    #def kernel(self):
        #"""Launch IPython console and connect to an existing kernel. You must use IPython.embed_kernel() in your code to use this."""
        #os.system("{0} -m IPython console --existing".format(sys.executable))

    def shutdown(self):
        self.messages_to_service_engine.put("SHUTDOWN")
        self._service_process.join()
        os.remove(self.saddle_dir.pgid())

    def tearDown(self):
        if sys.exc_info() != (None, None, None):
            functions = []
            tb_id = 0
            tb = sys.exc_info()[2]

            while tb is not None:
                functions.append(SaddleTraceback(tb_id, tb))
                tb = tb.tb_next
                tb_id = tb_id + 1

            # TODO : Make it appear much more like %tb4
            message = "functions =\n{}".format(functions.__repr__())
            self.ipython(message=message)

        self.shutdown()
