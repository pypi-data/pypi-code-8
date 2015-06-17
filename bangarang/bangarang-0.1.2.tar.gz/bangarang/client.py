import requests
import socket
import struct
from bangarang import event

class Client(object):
	host = ""
	ingest_port = 0
	api_port = 5556
	encoding = "json"

	def __init__(self, host, ingest_port, api_port=8081, encoding="json"):
		self.host = host
		self.ingest_port = ingest_port
		self.api_port = api_port
		self.encoding = encoding

	def encode_event(self, e):
		"""encode an event given the client's encoding"""
		if self.encoding is "json":
			return e.json()
		return ""

	def hosts(self):
		"""get all known hosts to the bangarang instance"""
		endpoint = "/api/stats/hosts"
		return requests.get(self.gen_api_url(endpoint)).json()

	def services(self):
		"""get all known services to the bangarang instance"""
		endpoint = "/api/stats/services"
		return requests.get(self.gen_api_url(endpoint)).json()

	def gen_api_url(self, endpoint=""):
		return "http://{}:{}{}".format(self.host, self.api_port, endpoint)



class HttpClient(Client):	
	endpoint = "/ingest"

	def send(self, e):
		encoded = self.encode_event(e)
		response = requests.post("http://{}:{}{}".format(self.host, self.ingest_port, self.endpoint),data=encoded, headers=self.headers())
		return response

	def headers(self):
		return {
			
		}

class TcpClient(Client):
	conn = None

	def __init__(self, host, ingest_port, api_port=8081, encoding="json"):
		super().__init__(host,ingest_port, api_port,encoding)

		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.conn.connect((self.host, self.ingest_port))

	def send(self, e):
		encoded = self.encode_event(e).encode("utf-8")

		# prepend the length of the upcomming message
		length = struct.pack("Q", len(encoded))
		encoded = length + encoded

		# write the encoded event
		self.conn.send(encoded)
