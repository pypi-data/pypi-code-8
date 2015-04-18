try:
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
except ImportError:
    # Seems to be an python2 installation
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer

class TestTCPServer(TCPServer):
    allow_reuse_address = 1

class TestServer(SimpleHTTPRequestHandler):

    @classmethod
    def serve(self, route):
        def _serve(fn):
            if not hasattr(self, '_routes') or not self._routes:
                self._routes = {}
            self._routes[route] = fn
        return _serve

    @classmethod
    def res(self, res):
        self._res = res

    def run_func(self):
        try:
            length = self.headers.get('content-length')
            if length:
                self._res.append(self.rfile.read(int(length)))
            self._routes[self.path](self)
            return
        except KeyError:
            pass
        self.send_response(404)
        self.end_headers()
        return

    def do_GET(self):
        return self.run_func()

    def do_POST(self):
        return self.run_func()

    def do_DELETE(self):
        return self.run_func()

    def do_PATCH(self):
        return self.run_func()

if __name__ == '__main__':
    @TestServer.serve('/test')
    def mytest(obj):
        obj.send_response(200)
        obj.send_header('Content-Type', 'application/json; charset=utf-8')
        obj.end_headers()
        obj.wfile.write(b"{'Hello': 'World'}")

    res_list = []
    TestServer.res(res_list)
    httpd = TestTCPServer(('', 8080), TestServer)
    httpd.handle_request()
    for r in res_list:
        print("%s" % r)
