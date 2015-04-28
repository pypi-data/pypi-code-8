from __future__ import absolute_import

import importlib
import logging
import os
import socket

from conversion import convert_bool

import requests

from requests.exceptions import HTTPError

from zymbit import config, statemachine, util
from zymbit.client import Client
from zymbit.clientid import get_client_id
from zymbit.compat import config
from zymbit.exceptions import NotConnected, TasksFailed
from zymbit.linux.util import create_ssh_key, get_pubkey

CONNECTION_REFUSED = 61

PROVISION_PATH = os.environ.get('PROVISION_PATH', '/provision')


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
        else:
            connected = True

        if connected:
            self.logger.info('connected')
            return True

        self.load_tasks()

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
                print 'line={}'.format(line)

        self.process_tasks()

    def create_ssh_key(self):
        _config = config.get_config()
        tunnel_config = _config.setdefault('tunnel', {})
        identity_file = tunnel_config.get('identity_file', config.TUNNEL_SSH_KEY_PATH)
        if not os.path.exists(identity_file):
            create_ssh_key(identity_file)
            self.logger.info('created ssh key at identity_file={}'.format(identity_file))

        # check to see if config should be written
        if not tunnel_config.get('host'):
            _config['tunnel'].update({
                'identity_file': identity_file,
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

    def load_task(self, name, task_config):
        module_path, class_name = task_config['class_path'].rsplit('.', 1)

        task_module = importlib.import_module(module_path)
        task_class = getattr(task_module, class_name)

        task = task_class(**task_config.get('params', {}))

        # print 'task name={}, task_config={}, task_class={}, task={}'.format(name, task_config, task_class, task)
        self.tasks[name] = task

    def load_tasks(self):
        self.logger.debug('load_tasks')

        _config = config.get_config()
        self.tasks_config = _config.get('tasks', {})
        for name, task_config in self.tasks_config.items():
            # if a task is already loaded, skip
            if name in self.tasks:
                continue

            try:
                self.load_task(name, task_config)
            except Exception, exc:
                self.logger.exception(exc)
                self.logger.error('task name={} raised exception when trying to load it'.format(name))

        return True

    def process_tasks(self):
        reload_tasks = False
        task_names = self.tasks.keys()
        for task_name in task_names:
            task = self.tasks[task_name]

            try:
                # self.logger.debug('task task_name={}, task={}'.format(task_name, task))
                task.loop()
            except Exception, exc:
                self.logger.exception(exc)
                self.logger.error('task_name={} raised exception above'.format(task_name))

                self.quit_task(task_name, task)
                reload_tasks = True

        if reload_tasks:
            raise TasksFailed

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
            self.logger.debug('waiting for provisioning token')
            return

        self.logger.debug('provisioning, client_id={}'.format(client_id))

        client_id = get_client_id()
        provision_url = util.get_api_url(config.PROVISION_PATH)

        ssh_pubkey = get_pubkey(config.TUNNEL_SSH_KEY_PATH)

        data = {
            'token': provisioning_token,
            'client_id': client_id,
            'ssh_pubkey': ssh_pubkey,
        }

        verify = convert_bool(os.environ.get('SSL_CHECK_HOSTNAME', 'true'))

        response = requests.post(provision_url, data=data, verify=verify)

        try:
            response.raise_for_status()
        except HTTPError, exc:
            self.logger.exception(exc)
            self.logger.error(response.content)

            raise

        response_data = response.json()

        self._write_config(response_data, config.TUNNEL_SSH_KEY_PATH)

    def run(self):
        while self._run:
            try:
                super(Connector, self).run()
            except (NotConnected, TasksFailed):
                pass

    def send(self, envelope):
        self.client.send_raw(envelope)

    def _write_config(self, response_data, identity_file):
        _config = config.get_config()
        _config.setdefault('auth', {}).update({
            response_data['client_id']: {
                'uuid': response_data['uuid'],
                'auth_token': response_data['auth_token'],
            },
        })

        # save the SSH tunnel identity file
        _config.setdefault('tunnel', {}).update({
            'identity_file': identity_file,
            'ssh_port': response_data['ssh_port'],
        })

        config.save_config(_config)

    # now that the methods are defined, use the function definitions themselves
    # to setup the state machine transitions
    transitions = {
        connect: {
            True: connected,
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
