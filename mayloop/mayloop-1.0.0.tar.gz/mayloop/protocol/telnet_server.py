import os

from .line_message import LineMessage
from ..exc import StartError


class TelnetServer(LineMessage):
	def __init__(self, server):
		LineMessage.__init__(self)
		self._server = server
	

	def messageReceived(self, message):
		if message == b'stats':
			response = str(self._server._stats)

		elif message == b'pause':
			self._server.pause()
			response = 'server paused'

		elif message == b'resume':
			self._server.resume()
			response = 'server resumed'

		elif message == b'stop':
			self._server.stop()
			response = 'server stopped'

		elif message == b'start':
			try:
				self._server.hot_start()
				response = 'server started'
			except StartError as e:
				response = str(e)

		elif message == '':
			return

		else:
			response = 'bad command'

		self.sendMessage(response + os.linesep)


	def sendMessage(self, message):
		self.transport.write(str.encode(message))
