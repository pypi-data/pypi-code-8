import multiprocessing
import signal
import logging
import functools
import getpass
import json

import faulthandler
from setproctitle import setproctitle

import swf.actors


logger = logging.getLogger(__name__)


__all__ = ['MultiProcessActor']


def get_hostname():
    import socket

    return socket.gethostname()


def reset_signal_handlers(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        return func(*args, **kwargs)

    wrapped.__wrapped__ = func
    return wrapped


def will_release_semaphore(method):
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        finally:
            self._semaphore.release()

    wrapped.__wrapped__ = method
    return wrapped


class MultiProcessActor(swf.actors.Actor):
    """Multi-processing implementation of a SWF actor.

    """
    def __init__(self,
                 domain,
                 task_list=None,
                 nb_children=None,
                 *args, **kwargs):
        self.is_alive = False
        if not nb_children:
            nb_children = multiprocessing.cpu_count()
        self.nb_children = nb_children
        self._semaphore = multiprocessing.Semaphore(self.nb_children)
        self._children_processes = set()

        super(MultiProcessActor, self).__init__(
            domain,
            task_list,
            *args,
            **kwargs
        )

    @property
    def identity(self):
        """Identity when polling decision task.

        http://docs.aws.amazon.com/amazonswf/latest/apireference/API_PollForDecisionTask.html

        Identity of the decider making the request, which is recorded in the
        DecisionTaskStarted event in the workflow history. This enables
        diagnostic tracing when problems arise. The form of this identity is
        user defined. Minimum length of 0. Maximum length of 256.

        """
        return json.dumps({
            'user': getpass.getuser(),   # system's user.
            'hostname': get_hostname(),  # Main hostname.
            'pid': os.getpid(),          # Current pid.
        })[:256]  # May truncate value to fit with SWF limits.

    def set_process_name(self, name=None):
        if name is None:
            name = self.name

        setproctitle('{}[{}]'.format(name, self.state))

    def bind_signal_handlers(self):
        """Binds signals for graceful shutdown.

        - SIGTERM and SIGINT lead to a graceful shutdown.
        - SIGSEGV, SIGFPE, SIGABRT, SIGBUS and SIGILL displays a traceback
          using the faulthandler library.

        """
        def signal_graceful_shutdown(signum, frame):
            """
            Note: Function is nested to have a reference to *self*.

            """
            if not self.is_alive:
                return

            logger.info(
                'signal %d caught. Shutting down %s',
                signum,
                self.name,
            )
            self.is_alive = False
            self.stop(graceful=True)

        faulthandler.enable()
        signal.signal(signal.SIGTERM, signal_graceful_shutdown)
        signal.signal(signal.SIGINT, signal_graceful_shutdown)

    def foreach_child(self, func, message=''):
        for process in list(self._children_processes):
            logger.info(
                "%s's subprocess (pid=%d)%s",
                self.name,
                process.pid,
                ': %s' % message if message else '',
            )
            func(process)
            yield process

    def foreach_child_remove(self, func, message=''):
        for process in self.foreach_child(func, message):
            self._children_process.remove(process)

    def stop_gracefully(self, join_timeout=60):
        self.foreach_child_remove(
            lambda process: process.join(join_timeout),
            "gracefully stopping",
        )

    def stop_forcefully(self):
        self.foreach_child_remove(
            lambda process: process.terminate(),
            "terminating",
        )

    def stop(self, graceful=True, join_timeout=60):
        """Stop the actor processes and subprocesses.

        :param graceful: wait for children processes?
        :type  graceful: bool.
        :param join_timeout: maximum time to wait for children.
        :type  join_timeout: int.
        """
        logger.info('stopping %s', self.name)
        self.is_alive = False  # No longer take requests.

        if graceful:
            self.stop_gracefully(join_timeout)
        else:
            self.stop_forcefully()
