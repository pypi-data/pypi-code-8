import asyncio
import json
from .request import Request

class Client:
    def __init__(self, host, port, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.host = host
        self.port = port

    @asyncio.coroutine
    def send(self, method, **kwargs):
        request = {
            'method': method,
            'parameters': kwargs
        }
        message = json.dumps(request)
        reader, writer = yield from asyncio.open_connection(
            self.host, self.port, loop=self.loop)
        writer.write(message.encode())
        yield from writer.drain()
        data = yield from reader.read(1048576)
        writer.close()
        return json.loads(data.decode())

    def __getattr__(self, item):
        return Request(self, [item])
