import random

import nanomsg

from omnomnom import models
from omnomnom import exceptions


class LycheeClient(object):
    default_send_timeout = 100

    def __init__(self, addresses, standalone=False, **kwargs):
        self.addresses = [addresses] if isinstance(addresses, (str, unicode))\
            else addresses
        self.standalone = standalone
        self.propagate_exc = kwargs.pop('propagate_exc', False)

    def __enter__(self):
        self.socket = models.Pip(nanomsg.PUSH)
        if self.standalone:
            address = self.get_worker_address()
            self.socket.connect(address=address)
        else:
            self.socket.connect(address=self.addresses[0])
        self.socket._set_send_timeout(self.default_send_timeout)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def get_worker_address(self):
        # when there are multiple worker families
        # (e.g few workers bind to one socket and few bind to another one)
        # this function picks one of them and binds to particular socket
        return random.choice(self.addresses)

    def send_task(self, task_instance):
        transport_data = task_instance.to_json()
        self.socket.send_json(transport_data)

    def execute(self, fun, args=None, kwargs=None):
        args = args if args else ()
        kwargs = kwargs if kwargs else {}
        task = fun.__name__ if not isinstance(fun, (str, unicode)) else fun

        is_from_main = lambda x: x.__module__ == '__main__'

        if not isinstance(fun, (str, unicode)) and is_from_main(fun):
            raise ValueError(u'Cannot enqueue functions from __main__ module')

        try:
            t = models.Task(
                task_name=task,
                task_args=args, task_kwargs=kwargs
            )
            self.send_task(t)
        except nanomsg.NanoMsgAPIError:
            if self.propagate_exc:
                msg = u"Timeout {0} exceeded".format(self.default_send_timeout)
                raise exceptions.PipConnectionException(msg)
