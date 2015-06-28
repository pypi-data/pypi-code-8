from tornado import gen
from tornado.tcpclient import TCPClient


class Pool(object):
    def __init__(self, ip, port):
        self._streams = set()
        self.ip = ip
        self.port = port

    @gen.coroutine
    def get_stream(self):
        try:
            stream = self._streams.pop()
        except KeyError:
            print('Not available stream. create new one')
            tcp_client = TCPClient()
            stream = yield tcp_client.connect(self.ip, self.port)
            self._streams.add(stream)
        raise gen.Return(stream)

    def release_stream(self, stream):
        self._streams.add(stream)


class Stream(object):
    def __init__(self, pool, _stream):
        self.pool = pool
        self._stream = _stream

    def __getattr__(self, item):
        return getattr(self._stream, item)

    def close(self):
        self.pool.release_stream(self._stream)

