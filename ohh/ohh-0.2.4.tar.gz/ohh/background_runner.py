from ohh.daemon import Daemon
import signal
import psutil
from os.path import join
import sys
import collections
import logging
import json
import sys
from logging.handlers import RotatingFileHandler

if sys.platform == 'darwin':
    from pync import Notifier
else:
    import subprocess


LOG_FORMAT = '%(asctime)-15s %(message)s'


class BackgroundRunner(Daemon):
    def run(self, runner, basedir):
        self._make_logger(basedir)
        self._basedir = basedir
        self._status = 'active'
        self._runner = runner
        self._usage_data = collections.deque(maxlen=60*5)
        signal.signal(signal.SIGINT, self._handle_stop)
        self._logger.info('ohh has started')
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            self._usage_data.append(cpu_usage)
            idle = self._is_idle()
            if idle and self._status == 'active':
                self._change_status('idle')
            elif not idle and self._status == 'idle':
                self._change_status('active')

    def _make_logger(self, basedir):
        logfile = join(basedir, 'ohh.log')
        self._logger = logging.getLogger('ohh')
        handler = RotatingFileHandler(logfile, maxBytes=1024**2)
        handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def _change_status(self, status):
        if status == 'active':
            self._runner.start(start_daemon=False)
        else:
            self._runner.stop(kill_daemon=False)
        self._status = status
        self._logger.info('status changed to {0}'.format(self._status))
        self._runner._write_info(self._status)
        self._notify(status)

    def _notify(self, status):
        msg = '[OHH] You are now ' + status
        if sys.platform == 'darwin':
            Notifier.notify(msg)
        elif sys.platform.startswith('linux'):
            subprocess.Popen(['notify-send', msg])

    # TODO: tune logic
    def _is_idle(self):
        if len(self._usage_data) < 60*5:
            return False
        total = 0
        high_usages_count = 0
        for percent in self._usage_data:
            if percent > int(self._runner.config.get('ohh', 'cpu_threshold')):
                high_usages_count += 1
            total += percent
        return high_usages_count < 30

    def _handle_stop(self, signal, frame):
        self._runner.stop(kill_daemon=False)
        self._logger.info('ohh has stopped')
        sys.exit(0)

if __name__ == '__main__':
    from ohh.runner import Runner
    import os
    runner = Runner()
    bg_runner = BackgroundRunner('/tmp/ohh.pid')
    bg_runner.run(runner, os.path.expanduser('~/.ohh'))
    bg_runner._change_status('idle')
