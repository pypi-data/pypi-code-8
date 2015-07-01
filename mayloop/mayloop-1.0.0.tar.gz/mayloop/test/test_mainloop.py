from unittest import TestCase, main as ut_main, skip
import logging
from threading import Thread
from multiprocessing import Process
from time import sleep

from mutils.system import is_py3

from mayloop.mainloop import MainLoop
from mayloop.config import Config
from mayloop.imported.twisted.internet_protocol import Factory
from .mock_protocols import ReturnFixedMessage
from .mock_client import Client

if is_py3():
	from queue import Queue
else:
	from Queue import Queue


class TestMainLoop(TestCase):
	server_process 		= None
	port 			= 40002
	multiple_client_counts 	= [10, 100]
	exp_response 		= 'test response'
	server_logfile		= 'server.log'

	@classmethod
	def setUpClass(cls):
		ReturnFixedMessage.message = cls.exp_response


	@classmethod
	def tearDownClass(cls):
		if cls.server_process is not None:
			print('stopping server..')
			cls.server_process.terminate()


	@classmethod
	def start_server_loop(cls, port):
		config = Config()
		config.add_service('', port, Factory.forProtocol(ReturnFixedMessage))
		config.start_logger(target=cls.server_logfile, level=logging.DEBUG)

		server = MainLoop(config)
		server.start()


	def start_server(test_func):
		def new_func(self):
			if self.server_process is None:
				print('starting server..')
				TestMainLoop.server_process = Process(target=TestMainLoop.start_server_loop, args=(self.port,))
				TestMainLoop.server_process.start()
				sleep(1)
			test_func(self)
		return new_func


	@start_server
	def test_single_client(self):
		client = Client('', self.port)
		client.connect()
		client.close()

		self.assertEquals(client.response, self.exp_response)


	@start_server
	def test_multiple_clients_serial(self):
		for i in self.multiple_client_counts:
			for j in range(i):
				client = Client('', self.port)
				client.connect()
				client.close()
				
				self.assertEquals(client.response, self.exp_response)


	@start_server
	def test_multiple_clients_parallel(self):
		def client_thread(port, client_id, results):
			client = Client('', port)
			client.connect()
			client.close()
		
			results.put((client_id, client.response))


		for i in self.multiple_client_counts:
			threads = []
			results = Queue()
			for j in range(i):
				t = Thread(target=client_thread, args=(self.port, j, results))
				t.start()
				threads.append(t)
				if (j+1)%10 == 0: sleep(0.01)

			for j in range(i):
				threads[j].join()
				client_id, response = results.get()
				self.assertEquals(response, self.exp_response, msg='client %d failed'%client_id)



if __name__ == '__main__':
	ut_main()

