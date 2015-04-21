from colorama import Fore, Back, Style
import os
import sys
import time
import subprocess
import signal
import psutil
import select
import pyuv
import inspect
import functools


class ServiceGroup(object):
    pass

class ServiceEngine(object):
    """Engine that starts services, sets up fixtures and shuts everything down."""
    timeout = 5.0       # TODO : Shutdown timeout
    triggerline = None
    _timedout = False
    _ready = False
    _shutdown_triggered = False
    environ = os.environ
    extra_environ = {}
    ipython_on = False

    def __init__(self, testcase):
        self.testcase = testcase
        self.services = ServiceGroup()

    def saddledir(self):
        """Full path of the saddle directory, usually .saddle in the project dir."""
        return self.testcase.saddle_dir.saddle_dir

    def _logfilename(self):
        return self.saddledir() + os.sep + "test.log"

    def _stdlogdir(self):
        return self.saddledir() + os.sep + "stdlog"

    def _service_pipes(self):
        """All of the stdout and stderr pipes of the services."""
        stdout_pipes = [
            service.stdout_pipe for service in self.all_services() if service.setup_finished
        ]
        stderr_pipes = [
            service.stderr_pipe for service in self.all_services() if service.setup_finished
        ]
        return stdout_pipes + stderr_pipes

    def all_services(self):
        """Unordered list of all services."""
        return [x[1] for x in self.services.__dict__.items()]

    def ready_services(self):
        return [x for x in self.all_services() if x.ready]

    def notready_services(self):
        return [x for x in self.all_services() if not x.ready]

    def services_ready(self):
        """Check that all services are ready."""
        for service in self.all_services():
            if not service.ready:
                return False
        return True

    def _close_pipes(self):
        """Close all the pipes in order to shut the engine down."""
        if not self.pipe_stdout.closed:
            self.pipe_stdout.close()
        for pipe in self._service_pipes():
            if not pipe.closed:
                pipe.close()
        if not self.signal_h.closed:
            self.signal_h.close()
        if not self.timer_handler.closed:
            self.timer_handler.close()
        for handle in self.tail_handles:
            handle.close()
        self.logfile.close()
        sys.stdout.write(Fore.RESET + Back.RESET + Style.RESET_ALL)
        sys.stderr.write(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _pipe_to_service(self):
        """Dictionary linking pipes to service (and whether it is a stderr/stdout pipe), used to figure out who logged what."""
        stdout_pipes = {
            service.stdout_pipe: (service, False) for service in self.all_services() if service.setup_finished
        }.items()
        stderr_pipes = {
            service.stderr_pipe: (service, True) for service in self.all_services() if service.setup_finished
        }.items()
        return dict(stdout_pipes + stderr_pipes)

    def writeline(self, identifier, line, color=''):
        """Log a line to the log file and/or stdout."""
        reset_all = Fore.RESET + Back.RESET + Style.RESET_ALL
        right_justified_name = identifier.rjust(self.longest_service_name() + 10)
        full_line = "{0}{1}[{2}] {3}{4}\n".format(
            reset_all, color, right_justified_name, line, reset_all
        )
        if not self.ipython_on:
            self.pipe_stdout.write(full_line)
        self.pipe_logfile.write(full_line)

    def logline(self, line, title="Saddle", color=''):
        self.writeline(title, line, color)

    def warnline(self, line):
        self.writeline("WARNING", line, color=Fore.YELLOW)

    def remove_log_file(self):
        if os.path.exists(self.testcase.saddle_dir.testlog()):
            os.remove(self.testcase.saddle_dir.testlog())

    def longest_service_name(self):
        """Length of the longest service name."""
        return max([len(service.name) for service in self.all_services()])

    def start(self, ready_queue, messages_to_service_engine,fixtures):
        """Orchestrate processes and I/O pipes."""
        self.start_time = time.time()
        self.ready_queue = ready_queue
        self.messages_to_service_engine = messages_to_service_engine

        os.chdir(self.directory)
        self.fixtures = fixtures
        self.remove_log_file()
        self.logfile = open(self.testcase.saddle_dir.testlog(), "a")

        self.loop = pyuv.Loop.default_loop()

        self.pipe_logfile = pyuv.Pipe(self.loop)
        self.pipe_logfile.open(self.logfile.fileno())

        self.pipe_stdout = pyuv.Pipe(self.loop)
        self.pipe_stdout.open(sys.stdout.fileno())

        for service in self.all_services():
            service.attach_to_service_engine(self)


        for service in self.all_services():
            if service.no_prerequisites():
                service.start()


        def on_pipe_read(handle, data, error):
            if data is None:
                pass #self._close_pipes()
            else:
                service, is_error = self._pipe_to_service()[handle]
                lines = [line for line in data.split('\n') if line != ""]

                for line in lines:
                    decoded_line = unicode(line.decode('utf-8', 'ignore')).encode('utf-8')

                    if is_error:
                        self.writeline("Err {0}".format(service.name), decoded_line, color=Fore.YELLOW)
                    else:
                        self.writeline("    {0}".format(service.name), decoded_line)

                    if not service.loaded:
                        if service.ready_check(line):
                            service.loaded = True
                            self.logline("{0} Loaded.".format(service.name))
                            service.poststart_run()
                            service.poststart_started = True



        def poll_handler(timer_handle):
            """Handle messages from the test thread and timeout."""
            for service in self.all_services():
                # Start the process if its setup thread is done
                if not service.setup_finished and hasattr(service, 'setup_runner') and not service.setup_runner.is_alive():
                    service.setup_finished = True
                    service.start_process()
                    service.stdout_pipe.start_read(on_pipe_read)
                    service.stderr_pipe.start_read(on_pipe_read)

                # If a poststart thread is done...
                if service.poststart_started and not service.ready and not service.poststart_runner.is_alive():
                    service.ready = True

                    # Start any services which rely upon this one as a prerequisite
                    for notstartedservice in [x for x in self.all_services() if not x.started]:
                        if set(notstartedservice.needs).issubset(set(self.ready_services())):
                            notstartedservice.start()

                    # If every service is started, let's start testing.
                    if self.services_ready():
                        startup_duration = time.time() - self.start_time
                        self.logline("READY in {0:.1f} seconds.".format(startup_duration), color=Style.BRIGHT)
                        self.ready_queue.put("READY")
                        self._ready = True
                        return

            if not self.messages_to_service_engine.empty():
                msg = self.messages_to_service_engine.get()
                if not self.pipe_stdout.closed and msg == "SHUTDOWN":
                    self.stop()
                if msg == "IPYTHONON":
                    self.ipython_on = True
                elif msg == "IPYTHONOFF":
                    self.ipython_on = False

            if not self._ready and time.time() - self.start_time > self.timeout and self._timedout == False:
                self.warnline("TIMEOUT")
                self._timedout = True
                self.ready_queue.put("TIMEOUT")
                self.stop()
                return

        def signal_cb(handle, signum):
            """Handle ctrl-C if not in ipython shell"""
            if not self.ipython_on:
                sys.stdout.write("Ctrl-C\n")
                sys.stdout.write(Fore.RESET + Back.RESET + Style.RESET_ALL)
                sys.stderr.write(Fore.RESET + Back.RESET + Style.RESET_ALL)
                self.stop()

        def handle_tail(fullfilename, title, color, handle, filename, events, error):
            with open(fullfilename, 'r') as filehandle:
                filehandle.seek(self.tail_positions[fullfilename])
                tailportion = filehandle.read().split('\n')
            for line in tailportion:
                if line != "":
                    if color is None:
                        self.logline(line, title=title)
                    else:
                        self.logline(line, title=title, color=color)

            self.tail_positions[fullfilename] = os.stat(fullfilename).st_size

        self.signal_h = pyuv.Signal(self.loop)
        self.signal_h.start(signal_cb, signal.SIGINT)

        self.timer_handler = pyuv.Timer(self.loop)
        self.timer_handler.start(poll_handler, 0.01, 0.01)

        self.tail_handles = []
        self.tail_positions = {}


        # TODO: Reimplement touch in a cleaner, more platform agnostic way.
        # TODO: Close tail handles after set up / poststart is finished.
        def starttailing(stdlog, title, color):
            filename = self.testcase.saddle_dir.stdlogdir() + os.sep + stdlog
            os.system("touch " + filename)
            self.tail_positions[filename] = 0
            tail = pyuv.fs.FSEvent(self.loop)
            tail.start(filename, 0, functools.partial(handle_tail, filename, title, color))
            self.tail_handles.append(tail)
            os.system("touch " + filename)

        starttailing("testcase.out", "Test", None)
        starttailing("testcase.err", "Err Test", Fore.YELLOW)

        for service in self.all_services():
            starttailing(service.name.lower() + "_setup.out", "Setup {}".format(service.name), None)
            starttailing(service.name.lower() + "_setup.err", "Err Setup {}".format(service.name), Fore.YELLOW)

            starttailing(service.name.lower() + "_poststart.out", "Post {}".format(service.name), None)
            starttailing(service.name.lower() + "_poststart.err", "Err Post {}".format(service.name), Fore.YELLOW)

        self.loop.run()


    def stop(self):
        """Shut down all saddle services."""
        if not self._shutdown_triggered:
            self._shutdown_triggered = True

            for service in self.all_services():
                service.stop()

            still_running_services = self.all_services()

            for i in range(0, int(self.timeout * 100)):
                for service in still_running_services:
                    if service.is_dead():
                        still_running_services.remove(service)
                        self.logline("{0} Stopped".format(service.name))

                if len(still_running_services) == 0:
                    break

                time.sleep(0.01)

            # If after timeout seconds there are services remaining, commit service genocide.
            for service in still_running_services:
                self.warnline("Killing {0}".format(service.name))
                if not service.is_dead():
                    service.kill()
        self._close_pipes()
