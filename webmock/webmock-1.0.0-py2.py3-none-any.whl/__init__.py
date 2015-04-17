from wsgiref import simple_server
from ._version import get_versions

import threading
import logging

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

log = logging.getLogger('webmock')


class StoppableWSGIServer(simple_server.WSGIServer):

    stopped = False

    def serve_forever(self):
        while not self.stopped:
            self.handle_request()


class LoggingWSGIRequestHandler(simple_server.WSGIRequestHandler):

    def log_message(self, format, *args):
        log.debug(format % args)


class MockServer(object):

    quit_path = '/$!mock_server/quit'

    def __init__(self, app):
        self.app = app
        self._server = None

    def _middleware(self, environ, start_response):
        if environ['PATH_INFO'] == self.quit_path:
            self._server.stopped = True
            start_response('200 OK', [])
            return []
        return self.app(environ, start_response)

    def __enter__(self):
        assert not self._server, "server already started"

        self._server = simple_server.make_server(
                '127.0.0.1', 0, self._middleware,
                server_class=StoppableWSGIServer,
                handler_class=LoggingWSGIRequestHandler)

        self._thread = threading.Thread(
                name='mock_server',
                target=self._server.serve_forever)
        self._thread.daemon = True
        self._thread.start()

        return self._server.server_port

    start = __enter__

    def __exit__(self, *exc_info):
        assert self._server, "server not running"

        # send the quit signal
        urlopen('http://127.0.0.1:%d%s' % (self._server.server_port,
                                           self.quit_path))
        self._thread.join()
        self._server.server_close()
        self._server = None

    stop = __exit__

    def __call__(self, fn):
        def replacement(*args, **kwargs):
            port = self.start()
            try:
                fn(port, *args, **kwargs)
            finally:
                self.stop()
        return replacement

mock_server = MockServer

__version__ = get_versions()['version']
del get_versions
