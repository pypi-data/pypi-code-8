import sys
import logging

import nanomsg

from omnomnom import handlers
from omnomnom import models
from omnomnom import result_backends
from omnomnom import utils


class LycheeWorker(object):
    process_fun = 'recv_json'

    def __init__(self, address, **kwargs):
        self.address = address
        self.name = self.get_name(**kwargs)
        self.standalone = self.is_standalone(**kwargs)
        self.socket = self.get_socket(**kwargs)
        self.setup_socket(**kwargs)

        self.result_backend = self.get_result_backend(**kwargs)
        self.init_result_backend(**kwargs)
        self.handler = self.get_handler(**kwargs)
        self.log = logging.getLogger(__name__)

    def get_name(self, **kwargs):
        name = kwargs.get('name', None)
        return name if name else u'W-{0}'.format(utils.generate_name())

    def get_socket(self, **kwargs):
        socket = models.Pip(nanomsg.PULL)
        return socket

    def get_result_backend(self, **kwargs):
        result_backend = kwargs.get('result_backend', None)
        return result_backend or result_backends.DummyResultBackend()

    def init_result_backend(self, **kwargs):
        self.result_backend.setup(**kwargs)

    def is_standalone(self, **kwargs):
        return kwargs.get('standalone', False)

    def setup_socket(self, **kwargs):
        if self.standalone:
            self.socket.bind(self.address)
        else:
            self.socket.connect(self.address)

    def get_handler(self, **kwargs):
        if self.standalone:
            return handlers.FuturesHandler(
                result_backend=self.result_backend, **kwargs
            )
        return handlers.BasicHandler(result_backend=self.result_backend, **kwargs)

    def stop(self):
        self.log.info(u"Stopping {0} gracefully.".format(self.name))
        self.handler.close()
        self.socket.close()
        self.result_backend.terminate()
        sys.exit(1)

    def start(self):
        self.log.info(u"{0} Started on {1}".format(self.name, self.address))

        if self.standalone:
            self.log.info(u"{0} runs in standalone mode".format(self.name))

        while True:
            try:
                data = getattr(self.socket, self.process_fun)()
                task = models.Task.from_task_data(data)
                self.log.debug(u'{0} received {1}'.format(
                    self.name, task.get_info()
                ))
                self.handler.process_task(task)
            except Exception as e:
                self.log.error(e, exc_info=1)

        self.socket.close()