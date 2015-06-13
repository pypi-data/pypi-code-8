from __future__ import absolute_import

import importlib
import json
import logging
import os
import socket

from conversion import convert_bool

import requests

from requests.exceptions import ConnectionError, HTTPError

from zymbit import config, statemachine, util
from zymbit.client import Client
from zymbit.clientid import get_client_id
from zymbit.compat import config, util
from zymbit.config import get_config
from zymbit.exceptions import NotConnected, TasksFailed
from zymbit.util import get_device_meta

CONNECTION_REFUSED = 61

PROVISION_PATH = os.environ.get('PROVISION_PATH', '/provision')
SSL_CHECK_HOSTNAME = convert_bool(os.environ.get('SSL_CHECK_HOSTNAME', 'true'))


def get_connector():
    return Connector.instance()


class Connector(statemachine.StateMachine):
    _instance = None

    def __init__(self):
        super(Connector, self).__init__()

        self.client = None
        self.system = util.get_system()

        # tasks that should be run on loop
        self.tasks = {}
        self.tasks_config = {}

    @classmethod
    def instance(cls):
        if cls._instance:
            return cls._instance

        cls._instance = cls()

        return cls._instance

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def connect(self):
        if not self.client:
            self.client = Client()

        # don't reconnect an already-connected client
        connected = self.client.is_connected
        if connected:
            return True

        try:
            self.client.connect()
        except NotConnected:
            pass
        except socket.error, exc:
            if exc[0] not in (111,):
                raise
        else:
            self.logger.info('connected')
            self.load_tasks()

            return True

        # process tasks if not connected
        self.process_tasks()

    def connected(self):
        try:
            line = self.client.recv()
        except socket.error, exc:
            if exc[0] not in (110, 111):
                raise

            self.client.close()
            raise NotConnected
        else:
            if line:
                self.process_message(line)

        processed = self.process_tasks()
        # if tasks are processed, don't sleep
        if processed:
            self.loop_sleep_time = 0.01
        else:
            self.loop_sleep_time = 1.0

        self.logger.debug('processed={}, loop_sleep_time={}'.format(processed, self.loop_sleep_time))

    def create_ssh_key(self):
        _config = config.get_config()
        tunnel_config = _config.setdefault('tunnel', {})
        identity_file = config.TUNNEL_SSH_KEY_PATH
        if not os.path.exists(identity_file):
            util.create_ssh_key(identity_file)
            self.logger.info('created ssh key at identity_file={}'.format(identity_file))

        # check to see if config should be written
        if not tunnel_config.get('host'):
            _config['tunnel'].update({
                'user': 'tunnel',
                'host': 'tunnel.zymbit.com',
            })
            config.save_config(_config)

        return True

    def get_auth(self):
        _config = config.get_config()
        client_id = get_client_id()

        return _config.get('auth', {}).get(client_id)

    def get_provisioning_token(self):
        _config = config.get_config()

        return _config.get('auth', {}).get('provisioning_token')

    def on_config(self, data):
        _config = data['params']
        config.save_config(_config)

    def process_message(self, message):
        try:
            data = json.loads(message)
        except ValueError:
            pass
        else:
            action = data['action']
            action_fn = getattr(self, 'on_{}'.format(action), None)
            if action_fn:
                action_fn(data)
                return

        self.logger.info('message={}'.format(message))

    def load_task(self, name, task_config):
        module_path, class_name = task_config['class_path'].rsplit('.', 1)

        task_module = importlib.import_module(module_path)
        task_class = getattr(task_module, class_name)

        task = task_class(**task_config.get('params', {}))

        self.logger.debug('load task name={}, task_config={}, task_class={}, task={}'.format(
            name, task_config, task_class, task)
        )

        self.tasks[name] = task

    def load_tasks(self):
        _config = config.get_config()
        self.tasks_config = _config.get('tasks', {})

        self.logger.debug('load_tasks, tasks_config={}'.format(self.tasks_config))
        for name, task_config in self.tasks_config.items():
            # if a task is already loaded, skip
            if name in self.tasks:
                self.logger.debug('task name={} already loaded'.format(name))
                continue

            try:
                self.load_task(name, task_config)
                self.logger.info('loaded task name={}'.format(name))
            except Exception, exc:
                self.logger.exception(exc)
                self.logger.error('task name={} raised exception when trying to load it'.format(name))

        return True

    def process_tasks(self):
        processed = None

        reload_tasks = False
        task_names = self.tasks.keys()
        for task_name in task_names:
            task = self.tasks[task_name]

            try:
                # self.logger.debug('task task_name={}, task={}'.format(task_name, task))
                if task.loop():
                    processed = True
            except Exception, exc:
                self.logger.exception(exc)
                self.logger.error('task_name={} raised exception above'.format(task_name))

                self.quit_task(task_name, task)
                reload_tasks = True

        if reload_tasks:
            raise TasksFailed

        return processed

    def quit(self):
        for name, task in self.tasks.items():
            self.quit_task(name, task)

    def quit_task(self, name, task):
        try:
            task.quit()
        except Exception, exc2:
            self.logger.exception(exc2)
            self.logger.error('task name={} raised exception above trying to quit'.format(name))

        self.tasks.pop(name, None)  # don't barf if the task is not in the tasks list

    def reload_tasks(self):
        return self.load_tasks()

    def register(self):
        client_id = get_client_id()
        auth = self.get_auth()
        if auth:
            return True

        provisioning_token = self.get_provisioning_token()
        if not provisioning_token:
            self.logger.debug(
                'waiting for provisioning token, no auth for client_id={}'.format(client_id))
            return

        self.logger.debug('provisioning, client_id={}'.format(client_id))

        provision_url = util.get_api_url(config.PROVISION_PATH)

        ssh_pubkey = util.get_pubkey(config.TUNNEL_SSH_KEY_PATH)

        data = {
            'token': provisioning_token,
            'client_id': client_id,
            'ssh_pubkey': ssh_pubkey,
        }

        data.update(get_device_meta())

        _config = get_config()
        verify = _config.get('cloud', {}).get('check_hostname')
        if verify is None:
            verify = SSL_CHECK_HOSTNAME

        try:
            response = requests.post(provision_url, data=data, verify=verify)
        except ConnectionError, exc:
            self.logger.exception(exc)
            self.logger.error('error making request to provision_url={}'.format(provision_url))

            raise

        try:
            response.raise_for_status()
        except HTTPError, exc:
            self.logger.exception(exc)
            self.logger.error('error making request to provision_url={}, content={}'.format(
                provision_url, response.content)
            )

            raise

        response_data = response.json()

        self._write_config(response_data)

        return True

    def run(self):
        while self._run:
            try:
                super(Connector, self).run()
            except (NotConnected, TasksFailed):
                pass

    def send(self, envelope):
        self.client.send_raw(envelope)

    def _write_config(self, response_data):
        config.save_config(response_data)

    # now that the methods are defined, use the function definitions themselves
    # to setup the state machine transitions
    transitions = {
        connect: {
            True: connected,
            TasksFailed: reload_tasks,
        },
        connected: {
            NotConnected: connect,
            TasksFailed: reload_tasks,
        },
        create_ssh_key: {
            True: load_tasks,
        },
        load_tasks: {
            True: register,
        },
        reload_tasks: {
            True: connect,
        },
        register: {
            True: connect,
        },
        statemachine.StateMachine.start: {
            True: create_ssh_key,
        },
    }
