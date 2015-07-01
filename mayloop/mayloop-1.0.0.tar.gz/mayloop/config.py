import logging

from .logger import log


class Service:
	def __init__(self, host, port, factory):
		self.host = host
		self.port = port
		self.factory = factory


class Pipe:
	def __init__(self, factory, readonly=True):
		self.factory 	= factory
		self.readonly 	= readonly
		self.transport	= None


class Call:
	def __init__(self, func, args, kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs


	def execute(self):
		self.func(*self.args, **self.kwargs)


class Config:
	telnet_enabled = True
	telnet_port = 40001
	services = []
	pipes = []
	logger = log
	after_start = None	

	def __init__(self):
		pass


	def add_pipe(self, factory):
		pipe = Pipe(factory)
		self.pipes.append(pipe)

		return pipe


	def add_service(self, host, port, factory):
		if host is None:
			raise ConfigError('host cannot be none')

		self.check_port_value(port)

		if factory is None:
			raise ConfigError('factory cannot be none')

		self.services.append(Service(host, port, factory))


	def check_port_value(self, port):
		if port is None or port < 0 or port > (2 ** 16 - 1) or type(port) != int:
			raise ConfigError('invalid port')


	def set_logger(self, logger):
		self.loggger = logger

	
	def start_logger(self, target='stdout', level=logging.ERROR):
		self.logger.start(target, level)


	def do_after_start(self, func, *args, **kwargs):
		self.after_start = Call(func, args, kwargs)


	def disable_telnet(self):
		self.telnet_enabled = False


	def set_telnet_port(self, port):
		self.check_port_value(port)
		self.telnet_port = port
