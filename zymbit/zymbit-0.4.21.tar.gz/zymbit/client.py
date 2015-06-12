from __future__ import absolute_import

import Queue
import logging
import random
import select
import socket
import ssl
import time
import datetime

from .exceptions import NotConnected
from .websocket import WebSocketConnectionClosedException
from zymbit import config
from zymbit.clientid import get_client_id

from zymbit.util import get_connection
from zymbit.envelope import get_envelope
from zymbit.timeutil import now

MAX_BACKOFF = 300  # 5 minutes
BACKOFF_JITTER = 10  # 10 seconds
CONNECTION_SETTLE_DT = datetime.timedelta(seconds=10)  # 10 second minimum to clear backoff


class Client(object):
    def __init__(self, handle_disconnect=True, connected_callback=None, client_id=None):
        """
        :param handle_disconnect - bool: internally handle a disconnect an gracefully reconnect; raises exception when False
        :return:
        """
        self.client_id = client_id

        self._connected_callback = connected_callback

        self.handle_disconnect = handle_disconnect

        self._ws = None
        self.is_connected = False
        self.connected_at = None

        self.backoff = 0
        self.backoff_until = None

        self.recv_q = Queue.Queue()

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @property
    def check_hostname(self):
        _config = config.get_config()

        return _config.get('cloud', {}).get('check_hostname')

    def connect(self):
        # simply call the ws property that takes care of establishing a connection
        return self.ws

    @property
    def credentials(self):
        _config = config.get_config()
        client_id = get_client_id()

        return _config.get('auth', {}).get(client_id)

    def _clear_backoff(self):
        if self.connected_at is None:
            return

        # only clear backoff when the connection has been established for more than CONNECTION_SETTLE
        if now() > self.connected_at + CONNECTION_SETTLE_DT:
            self.logger.debug(
                'connected more than {} clearing backoff'.format(CONNECTION_SETTLE_DT)
            )

            self.connected_at = None
            self.backoff = 0
            self.backoff_until = None

            return True

    def close(self):
        # don't close on closed
        if self._ws is None:
            return

        # self._ws.close()
        self.is_connected = False
        self._ws = None

        cleared = self._clear_backoff()
        if not cleared:
            self.backoff += 1
            seconds = min(2**self.backoff, MAX_BACKOFF)
            jitter = datetime.timedelta(seconds=BACKOFF_JITTER*random.random())
            self.backoff_until = jitter + now() + \
                                 datetime.timedelta(seconds=seconds)

            self.logger.debug('backoff={}, backoff_until={}, jitter={}'.format(self.backoff, self.backoff_until, jitter))

    def connected(self):
        """
        Called when websocket connection is initialized
        """
        self.is_connected = True

        self.connected_at = now()
        if self._connected_callback:
            self._connected_callback()

    def fileno(self):
        return self.ws.sock.fileno()

    def recv(self, ws=None):
        ws = ws or self.ws
        sock = ws.sock

        # check if there are pending messages in the queue
        try:
            return self.recv_q.get_nowait()
        except Queue.Empty:
            pass

        r, _, _ = select.select([sock], [], [], 0.01)
        if sock not in r:
            return

        try:
            return ws.recv()
        except WebSocketConnectionClosedException, exc:
            self.close()

            if not self.handle_disconnect:
                raise
        except NotConnected:
            if not self.handle_disconnect:
                raise
        except ssl.SSLError, exc:
            # SSLError: [Errno 8] _ssl.c:1359: EOF occurred in violation of protocol -- arduino
            error_number = exc[0]
            if error_number not in (2, 8):
                self.logger.warning('ssl error #{}, closing connection'.format(error_number))

            self.close()
            if not self.handle_disconnect:
                raise
        except socket.error as exc:
            error_number = exc[0]
            if error_number not in (11, 54):
                self.logger.warning('got socket error {}'.format(error_number))

            self.close()
            if not self.handle_disconnect:
                raise

    def send(self, action, params=None):
        """
        Wrap the given action and params in an envelope and send

        This calls the get_envelope() utility prior to sending the given message.

        :param action: string - upstream action
        :param params: dictionary - contains any data for this action

        :return: the result of send_raw()
        """
        try:
            return self.send_raw(get_envelope(action, params=params, client_id=self.client_id))
        except socket.error, exc:
            if exc[0] != 32:
                raise

            if not self.handle_disconnect:
                raise

            self.close()

            return False
        except WebSocketConnectionClosedException:
            if not self.handle_disconnect:
                raise

            self.close()

            return False  # the message was not sent

    def send_raw(self, message):
        """
        Send raw message

        Do not wrap in an envelope; simply send what was passed in

        :param message: string
        :return: result of websocket.send()
        """
        return self.ws.send(message)

    @property
    def url(self):
        _config = config.get_config()

        return _config.get('cloud', {}).get('websocket_url')

    @property
    def ws(self):
        if self.backoff_until and self.backoff_until > now():
            raise NotConnected()

        if self._ws is not None:
            return self._ws

        try:
            self._ws = get_connection(url=self.url, credentials=self.credentials, check_hostname=self.check_hostname)
        except socket.error, exc:
            # error: [Errno 146] Connection refused -- arduino yun
            # error: [Errno 145] Connection timed out -- arduino yun
            # gaierror: [Errno -2] Name or service not known -- arduino yun
            if exc[0] not in (-2, 61, 145, 146):
                raise

            self.logger.warning('unable to connect to url={}, exc={}'.format(self.url, exc))

            self.close()
            raise NotConnected(exc)

        for _ in range(1000):
            try:
                message = self.recv(ws=self._ws)  # prevent recv() from calling this property
            except Exception, exc:
                raise

            # self.recv() may close the connection, so check if _ws is not None
            if self._ws is None or not self._ws.connected:
                self.close()
                raise NotConnected('connection closed on opening')

            if message:
                self.recv_q.put_nowait(message)

                self.logger.debug('message={}'.format(message))
                self.connected()

                break

            time.sleep(0.01)
        else:
            self.close()

            raise NotConnected('unable to get websocket connection')

        self.logger.debug('got websocket, _ws={}'.format(self._ws))

        return self._ws
