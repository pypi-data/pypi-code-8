import logging

from mayloop.mainloop import MainLoop
from mayloop.config import Config
from mayloop.imported.twisted.internet_protocol import Factory
from .mock_protocols import TestServer, DumpData


def start_only_telnet():
	config = Config()
	config.start_logger(level=logging.DEBUG)

	server = MainLoop(config)
	server.start()


def start_test_server(protocol=TestServer):
	config = Config()
	config.add_service('', 40002, Factory.forProtocol(protocol))
	config.start_logger(level=logging.DEBUG)

	server = MainLoop(config)
	server.start()


if __name__ == '__main__':
	#start_only_telnet()
	start_test_server()

