import struct
import socket
from time import sleep


class Client:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.connection = None
		self.response = None


	def connect(self):
		data = 'hello'
		message = struct.pack('>i', len(data)) + str.encode(data)

		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((self.host, self.port))

		self.connection.send(message)
		res = self.connection.recv(512)
		#print('1: '+ res[4:].decode('utf-8'))

		self.response = res[4:].decode('utf-8')


	def close(self):
		self.connection.close()

