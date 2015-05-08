import socket
import subprocess
import os
import logging

__author__ = 'nekmo'
__dir__ = os.path.abspath(os.path.dirname(__file__))
LOCAL_HOSTS = ['localhost', '127.0.0.1']
DEVNULL = open(os.devnull, 'wb')
# DEVNULL = None
logger = logging.getLogger('telejson')


class InvalidPort(Exception):
    pass


def check_local_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    return False if result == 0 else True


def find_available_port(from_port, retries=100):
    for i in range(100):
        port = from_port + i
        if check_local_port(port):
            return port
    raise RuntimeError


class TelegramCli(object):
    sender_host = None
    sender_port = None
    receiver_host = None
    receiver_port = None
    command = 'telegram-cli'

    def __init__(self, sender=None, receiver=None, wait=True, disable_color=True):
        self.arguments = {}
        self.set_wait(wait)
        if sender is not False:
            if sender is None:
                sender = ('127.0.0.1', find_available_port(4458))
            self.set_sender(*sender)
        if receiver is not False:
            if receiver is None:
                receiver = ('127.0.0.1', find_available_port(1337))
            self.set_receiver(*receiver)
        self.set_disable_color(wait)

    def set(self, key, value=None):
        self.arguments[key] = value

    def unset(self, key):
        if not key in self.arguments: return
        del self.arguments[key]

    def set_log_level(self, level):
        self.set('-l', level)

    def set_log_file(self, file):
        self.set('-L', file)

    def _set_host_port(self, type, domain, port):
        if domain in LOCAL_HOSTS and check_local_port(port) is False:
            raise InvalidPort
        setattr(self, '%s_host' % type, domain)
        setattr(self, '%s_port' % type, port)

    def set_sender(self, domain, port):
        self._set_host_port('sender', domain, port)
        self.set('-s', '%s:%i' % (domain, port))

    def set_receiver(self, domain, port):
        self._set_host_port('receiver',  domain, port)
        self.set('-P', port)

    def set_wait(self, state):
        self.set('-W') if state else self.unset('-W')

    def set_disable_color(self, state):
        self.set('-C') if state else self.unset('-C')

    def run(self):
        command_line = [self.command]
        for set in self.arguments.items():
            for elem in set:
                if elem is None: continue
                command_line.append(str(elem))
        logger.debug('Running: %s' % ' '.join(command_line))
        subprocess.Popen(command_line, stdout=DEVNULL)


class Telejson(object):
    _sender = None
    _receiver = None

    def __init__(self):
        self.telegram_cli = TelegramCli()

    def get_receiver(self):
        if self._receiver is not None:
            return self._receiver
        from pytg2.receiver import Receiver
        receiver = Receiver(host=self.telegram_cli.sender_host,
                            port=self.telegram_cli.sender_port)
        receiver.start()
        self._receiver = receiver
        return receiver

    def get_sender(self):
        if self._sender is not None:
            return self._sender
        from pytg2.sender import Sender  # send messages, and other querys.
        sender = Sender(host=self.telegram_cli.receiver_host,
                        port=self.telegram_cli.receiver_port)
        self._sender = sender
        return sender

    def handler(self, function):
        from pytg2.utils import coroutine
        @coroutine
        def handler():
            while True:
                msg = (yield)
                function(msg)
        receiver = self.get_receiver()
        receiver.message(handler())

    def start(self):
        self.telegram_cli.run()

    def close(self):
        if self._sender:
            # self._sender.execute_function('safe_quit')
            self._sender.terminate()
        pass