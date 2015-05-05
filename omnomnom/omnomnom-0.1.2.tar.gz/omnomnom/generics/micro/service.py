import pprint
import logging
import functools

import nanomsg

from omnomnom import models
from omnomnom import exceptions
from omnomnom.generics.micro import utils
from omnomnom.utils import setup_loghandlers
from omnomnom.generics.micro import marshalling


class MicroServiceExecutionMeta(type):

    def __new__(cls, name, bases, attrs):
        new_attrs = attrs.copy()
        new_attrs['executables'] = {}

        for (el, val) in attrs.iteritems():
            if isinstance(val, models.Executable):
                is_valid, error = utils.validate_executable(val)
                if not is_valid:
                    raise exceptions.MicroServiceInitializationException(error)

                executable_name = getattr(val, 'name', el)
                new_attrs['executables'][executable_name] = val

        return super(MicroServiceExecutionMeta, cls).__new__(cls, name, bases, new_attrs)


class BasicMicroService(object):
    __metaclass__ = MicroServiceExecutionMeta

    name = None
    authentication_class = None
    socket_type = nanomsg.REP
    marshaller = marshalling.JsonMarshaller()

    def __init__(self, address, **kwargs):
        self.address = address
        self.name = self.get_name(**kwargs)
        self.marshaller = self.get_marshaller(**kwargs)
        self.authentication_class = self.get_authentication_class(**kwargs)
        self.socket_type = self.get_socket_type(**kwargs)
        self.socket = kwargs.pop('socket', self.get_socket(**kwargs))
        self.setup_socket(**kwargs)
        self.init_service(**kwargs)

    def get_marshaller(self, **kwargs):
        return self.marshaller

    def get_authentication_class(self, **kwargs):
        return self.authentication_class

    def get_name(self, **kwargs):
        return self.name or self.__class__.__name__

    def get_socket_type(self, **kwargs):
        return self.socket_type

    def get_socket(self, **kwargs):
        if not self.socket_type:
            raise RuntimeError(u"socket_type must be specified")

        socket = models.Pip(self.socket_type)
        return socket

    def setup_socket(self, **kwargs):
        # used to add initial socket options
        # and bind/connect
        self.bind()

    def receive_data(self):
        return self.socket.recv()

    def send_response(self, response):
        self.socket.send(response)

    def connect(self):
        self.socket.connect(self.address)

    def bind(self):
        self.socket.bind(self.address)

    def run(self, *args, **kwargs):
        raise NotImplementedError

    def init_service(self, **kwargs):
        # log handlers and additional setup
        # like for instance database connection
        log_level = kwargs.get('log_level', 'DEBUG')
        setup_loghandlers(level=log_level)

    def register_executable(self, name, executable):
        if name in self.executables:
            msg = u"{0} is already registered".format(name)
            raise exceptions.MicroServiceRegistrationException(msg)

        is_valid, error = utils.validate_executable(executable)

        if not is_valid:
            raise exceptions.MicroServiceRegistrationException(error)

        self.executables[name] = executable

    def to_registry(self, name, *args, **kwargs):
        return functools.partial(
            utils.register_executable, registry=self.executables,
            name=name, *args, **kwargs
        )

    def get_executables_information(self):
        printer = pprint.PrettyPrinter(indent=4)
        printer.pprint(self.executables)

    def execute(self, msg):
        try:
            executable = self.executables[msg.executable]
        except KeyError:
            msg = u"Executable {0} is not registered".format(msg.executable)
            raise exceptions.MicroServiceExecutionException(msg)

        return executable(service=self, *msg.args, **msg.kwargs)


class Fruit(BasicMicroService):

    def handle(self):
        request_data = self.receive_data()
        #logging.debug(u"Service received {0}".format(request_data))

        try:
            msg = self.marshaller.process_request_data(data=request_data)
            result = self.execute(msg)
            response = self.marshaller.prepare_response(result=result)
            self.send_response(response)
        except Exception as e:
            # import traceback
            # traceback.print_exc()
            logging.error(e)
            response = self.marshaller.prepare_response(err=e)
            self.send_response(response)

    def run(self, *args, **kwargs):
        logging.info(u"Starting {0}".format(self.name))
        logging.info(u"Registered executables: {0}".format(
            self.executables.keys())
        )

        while True:
            self.handle()


class PubFruit(BasicMicroService):
    socket_type = nanomsg.PUB