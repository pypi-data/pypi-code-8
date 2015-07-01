
from mayloop.protocol.fixed_length_message import FixedLengthMessage
from mayloop.imported.twisted.internet_protocol import Protocol

class TestServer(FixedLengthMessage):
	def messageReceived(self, message):
		self.sendMessage('just a test response')


class DumpData(Protocol):
	def dataReceived(self, data):
		print(data)


class ReturnFixedMessage(FixedLengthMessage):
	message = None

	def messageReceived(self, message):
		self.sendMessage(self.message)

