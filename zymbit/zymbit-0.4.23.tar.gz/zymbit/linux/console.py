import logging
import select
import socket

from zymbit.exceptions import ConnectionError

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 6571


class Console(object):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port

        self._socket = None

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except Exception, exc:
            self.logger.exception(exc)
            self.logger.warning('closing socket errored out, continuing')

        self._socket = None

    def fileno(self):
        return self.socket.fileno()

    def handle_socket_exception(self, socket_exc):
        """
        Handle the socket exception
        :param socket_exc: Exception
        """
        self._socket = None

    @property
    def socket(self):
        if self._socket is not None:
            return self._socket

        host_info = (self.host, self.port)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(1.0)

        try:
            self._socket.connect(host_info)
        except socket.error, exc:
            self.handle_socket_exception(exc)

            raise ConnectionError(
                'Unable to connect to host={}, port={}'.format(self.host, self.port))
        else:
            self.logger.debug('connected to {}'.format(host_info))

        return self._socket

    def read_socket(self):
        buf = ''

        try:
            data = self.socket.recv(4096)
        except socket.error, exc:
            self.logger.exception(exc)

            self.close()

            raise ConnectionError('error reading socket')
        else:
            if not data:
                self.close()

                raise ConnectionError('lost connection')
            else:
                buf += data

        return buf

    def recv(self, timeout=2.0):
        socket_list = [self.socket]

        buf = ''
        while True:
            # Get the list sockets which are readable
            _read, _, _ = select.select(socket_list, [], [], timeout)
            if _read:
                # after getting the first byte, don't wait very long for more
                # this is so the arduino is given time to process the given
                # command, but once we start getting a response, timeout is quick
                timeout = 0.1
            else:
                break

            for _socket in _read:
                if _socket == self.socket:
                    buf += self.read_socket()
                else:
                    raise ConnectionError(
                        'Unknown _socket={}'.format(_socket))

        return buf

    def send(self, buf):
        try:
            self.socket.send(buf)
        except socket.error, exc:
            if exc[0] != 32:
                raise

            self._socket = None
            self.send(buf)
