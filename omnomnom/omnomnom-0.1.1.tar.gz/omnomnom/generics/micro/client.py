import nanomsg

from omnomnom import models
from omnomnom import exceptions
from omnomnom.generics.micro import marshalling


class BasicMicroClient(object):
    socket_type = nanomsg.REQ
    default_send_timeout = 100
    marshaller = marshalling.JsonMarshaller()

    def __init__(self, address, **kwargs):
        self.address = address
        self.propagate_exc = kwargs.pop('propagate_exc', False)

    def get_socket(self):
        return models.Pip(self.socket_type)

    def __enter__(self):
        self.socket = self.get_socket()
        self.socket.connect(self.address)
        self.socket._set_send_timeout(self.default_send_timeout)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()


class MicroClient(BasicMicroClient):

    def send_request(self, request):
        self.socket.send(request)

    def get(self, executable, args=None, kwargs=None):
        msg = models.Message(
            executable=executable,
            args=args, kwargs=kwargs
        )
        request = self.marshaller.prepare_request(msg)

        try:
            self.send_request(request=request)
            response_data = self.socket.recv()
            return self.marshaller.process_response_data(
                data=response_data
            )
        except nanomsg.NanoMsgAPIError:
            if self.propagate_exc:
                msg = u"Timeout {0} exceeded".format(self.default_send_timeout)
                raise exceptions.PipConnectionException(msg)


class MicroSubClient(BasicMicroClient):
    socket_type = nanomsg.SUB

    def __init__(self, address, **kwargs):
        super(MicroSubClient, self).__init__(address, **kwargs)
        self.subscribe_to = kwargs.pop('subscribe_to', '')

    def get_socket(self):
        socket = models.Pip(self.socket_type)
        socket.set_string_option(
            nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, self.subscribe_to
        )
        return socket

    def receive(self):
        response_data = self.socket.recv()
        return self.marshaller.process_response_data(
            data=response_data
        )

    def get_responses(self):
        while True:
            yield self.receive()
