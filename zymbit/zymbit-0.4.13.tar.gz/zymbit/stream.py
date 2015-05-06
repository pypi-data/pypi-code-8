from __future__ import absolute_import

import logging
import socket
import time

from zymbit.exceptions import NotConnected
from zymbit.websocket import WebSocketConnectionClosedException

from .client import Client


class Stream(Client):
    def __init__(self, subscriptions):
        self.subscriptions = subscriptions

        super(Stream, self).__init__(connected_callback=self.online)

    @property
    def logger(self):
        name = '{}.{}'.format(__name__, self.__class__.__name__)
        return logging.getLogger(name)

    def handle(self, envelope):
        pass

    def loop(self):
        pass

    def online(self):
        """
        Called when websocket connection is initialized
        """
        self.logger.debug('connected, subscribing ...')
        for routing_key in self.subscriptions:
            params = {'routing_key': routing_key}
            self.logger.debug('subscribe params={}'.format(params))
            self.send('subscribe', params)

    def run(self):
        while True:
            try:
                envelope = self.recv()
            except socket.error as exc:
                if exc[0] == 11:
                    self.loop()
                    time.sleep(1.0)
                    continue

                self.logger.exception(exc)
                self.logger.error('socket closed, resetting connection')

                self._ws = None
            except NotConnected:
                time.sleep(1.0)
            except WebSocketConnectionClosedException:
                self._ws = None
            else:
                if envelope is None:
                    time.sleep(1.0)
                    continue

                self.handle(envelope)
