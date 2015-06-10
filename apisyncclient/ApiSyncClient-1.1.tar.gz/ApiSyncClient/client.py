import socket
import json
import sys
from .request import Request

class Client():
    def __init__(self, host, port, chunk_size=256):
        self.host = host
        self.port = port
        self.chunk_size = chunk_size

    def send(self, method, **kwargs):
        request = {
            'method': method,
            'parameters': kwargs
        }
        raw_request = json.dumps(request)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(raw_request.encode())

        raw_headers = s.recv(self.chunk_size)
        headers = json.loads(raw_headers.decode())
        s.send('ok'.encode())

        data = b''
        while sys.getsizeof(data) < headers.get('Content-Length', 0):
            data += s.recv(self.chunk_size)
        s.close()
        return data

    def __getattr__(self, item):
        return Request(self, [item])
