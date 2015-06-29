import ohh
import sys
import getpass
import os
import requests
import json
import dateutil.parser
import psutil
from ohh.background_runner import BackgroundRunner
from datetime import datetime
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


class Runner(object):
    def __init__(self, basedir='~/.ohh'):
        super(Runner, self).__init__()
        self._basedir = os.path.expanduser(basedir)

        if not os.path.isdir(self._basedir):
            os.mkdir(self._basedir)

        self._log_file = os.path.join(self._basedir, 'ohh.log')
        self._pid_file = os.path.join(self._basedir, 'ohh.pid')
        self._config_file = os.path.join(self._basedir, 'ohhrc')
        self._info_file = os.path.join(self._basedir, 'session_info')

        self.config = ConfigParser()
        self._read_config()
        self._background_runner = BackgroundRunner(
            self._pid_file, stdout=self._log_file, stderr=self._log_file)

    def _read_input(self):
        python_version = sys.version_info.major
        if python_version == 3:
            return input()
        else:
            return raw_input()

    def _create_config(self):
        self.config.add_section('ohh')
        for k, v in ohh.DEFAULT_CONFIG.items():
            self.config.set('ohh', k, v)
        self._save_config()

    def _read_config(self):
        if not os.path.isfile(self._config_file):
            self._create_config()
        else:
            self.config.read(self._config_file)

    def _post(self, path, data=None):
        headers = {}
        if data:
            data = json.dumps(data)
            headers['Content-Type'] = 'application/json'
        base_url = self.config.get('ohh', 'endpoint')
        url = os.path.join(base_url, path)
        token = self.config.get('ohh', 'token')
        if token:
            headers['X-Token'] = token
        return requests.post(url, data=data, headers=headers)

    def login(self):
        sys.stdout.write('Email: ')
        email = self._read_input()
        password = getpass.getpass()
        r = self._post('authenticate', {'mail': email, 'password': password})
        if r.status_code == 401:
            raise ohh.OhhError('wrong email or password')
        self._check_http_status('login', r.status_code)
        self.config.set('ohh', 'token', r.json()['token'])
        self._save_config()

    def _save_config(self):
        with open(self._config_file, 'w') as f:
            self.config.write(f)

    def start(self, start_daemon=True):
        info = self.get_session_info()
        if self.is_running() and info and info['status'] == 'active':
            print("Session already started, use 'ohh stop' to stop.")
            return
        self._check_credentials()
        r = self._post('sessions/start')
        self._check_http_status('start', r.status_code)
        self._write_info('active')
        if start_daemon:
            if self.is_running():
                self._background_runner.restart()
            else:
                self._background_runner.start(self, self._basedir)

    def _write_info(self, status):
        with open(self._info_file, 'w') as f:
            f.write(json.dumps({
                'start_time': datetime.now().isoformat(),
                'status': status,
            }))

    def stop(self, kill_daemon=True):
        self._check_credentials()
        r = self._post('sessions/end')
        self._check_http_status('stop', r.status_code)
        if os.path.isfile(self._info_file):
            os.remove(self._info_file)
        if kill_daemon and self.is_running():
            self._background_runner.stop()

    def is_running(self):
        pid = self._background_runner.get_pid()
        return pid and psutil.pid_exists(pid)

    def _check_http_status(self, action, status_code):
        if status_code != 200:
            msg = 'failed to {0}, got status {1}'
            raise ohh.OhhError(msg.format(action, status_code))

    def status(self):
        if self.is_running():
            pid = self._background_runner.get_pid()
            print('ohh is running (pid {0})'.format(pid))
            self.show_info()
        else:
            print('ohh is not running')

    def get_session_info(self):
        if not os.path.isfile(self._info_file):
            return
        with open(self._info_file, 'r') as f:
            status = json.loads(f.read())
            return status

    def show_info(self):
        info = self.get_session_info()
        if info:
            timediff = self._timediff(info['start_time'])
            print("You have been {0} for {1}.".format(info['status'], timediff))

    def _check_credentials(self):
        token = self.config.get('ohh', 'token')
        if token is None or token == 'None':
            raise ohh.OhhError("Please run 'ohh login'")

    def _timediff(self, start_time):
        start_time = dateutil.parser.parse(start_time)
        s = (datetime.now() - start_time).seconds
        if s < 60:
            return '{0} seconds'.format(s)
        elif s < 3600:
            return '{0} minutes and {1} seconds'.format(s // 60, s % 60)
        else:
            return '{0} hours and {1} minutes'.format(s // 3600, s // 60 % 60)

    def run(self, action):
        return getattr(self, action)()
