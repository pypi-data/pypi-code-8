import sys
import logging

import nanomsg

from omnomnom import models


logger = logging.getLogger(__name__)


class LycheeQueue(object):

    def __init__(self, *args, **kwargs):
        self.proxied = 0
        self.push_address = kwargs.pop('push_address')
        self.pull_address = kwargs.pop('pull_address')
        self.push_socket = kwargs.pop('push_socket', self.get_push_socket())
        self.pull_socket = kwargs.pop('pull_socket', self.get_pull_socket())
        self.push_socket.bind(self.push_address)
        self.pull_socket.bind(self.pull_address)
        self.log = logger

    def get_push_socket(self):
        socket = models.Pip(nanomsg.PUSH)
        return socket

    def get_pull_socket(self):
        socket = models.Pip(nanomsg.PULL)
        return socket

    def stop(self):
        self.log.info(u"Stopping Queue gracefully")
        self.push_socket.close()
        self.pull_socket.close()
        sys.exit(1)

    def start(self):
        self.log.info(u"Queue instance started. Frontend ({0}) <-- > Backend ({1})".format(
            self.pull_address, self.push_address
        ))

        pull_fun = 'recv'
        push_fun = 'send'

        while True:
            try:
                data = getattr(self.pull_socket, pull_fun)()
                self.log.info(u"Proxying message")
                self.log.debug(data)
                self.proxied += 1
                getattr(self.push_socket, push_fun)(data)
                self.log.info(u"Proxied {0} messages".format(self.proxied))
            except Exception as e:
                self.log.error(e, exc_info=1)

        self.pull_socket.close()
        self.push_socket.close()
