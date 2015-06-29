from ohh.daemon import Daemon
import signal
import psutil
from os.path import join
import sys
import collections
import logging
import json
from logging.handlers import RotatingFileHandler


class BackgroundRunner(Daemon):
    def run(self, runner, basedir):
        self._make_logger(basedir)
        self._basedir = basedir
        self._status = 'active'
        self._runner = runner
        self._usage_data = collections.deque(maxlen=60*5)
        signal.signal(signal.SIGINT, self._handle_stop)
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
        self._logger.addHandler(handler)

    def _change_status(self, status):
        if status == 'active':
            self._runner.start(start_daemon=False)
        else:
            self._runner.stop(kill_daemon=False)
        self._usage_data.clear()
        self._status = status
        self._logger.info('status changed to {0}'.format(self._status))
        self._runner._write_info(self._status)

    # TODO: tune logic
    def _is_idle(self):
        if len(self._usage_data) < 60*5:
            return False
        total = 0
        high_usages_count = 0
        for percent in self._usage_data:
            if percent > 10:
                high_usages_count += 1
            total += percent
        return high_usages_count < 30

    def _handle_stop(self, signal, frame):
        self._runner.stop(kill_daemon=False)
        sys.exit(0)

if __name__ == '__main__':
    from ohh.runner import Runner
    import os
    runner = Runner()
    bg_runner = BackgroundRunner('/tmp/ohh.pid')
    bg_runner.run(runner, os.path.expanduser('~/.ohh'))
