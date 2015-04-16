import socket
import json
from .request import Request

class Client():
    def __init__(self, host, port, size=1048576):
        self.host = host
        self.port = port
        self.size = size

    def send(self, method, **kwargs):
        request = {
            'method': method,
            'parameters': kwargs
        }
        message = json.dumps(request)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(message.encode())
        data = s.recv(self.size)
        s.close()
        return data

    def __getattr__(self, item):
        return Request(self, [item])
