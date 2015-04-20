from _socket import SHUT_RD
import threading
import socket
import select

from .connection import Connection


class JinniThreadPool(object):
    def __init__(self, fn, max_threads=10):
        self.fn = fn
        self.max_threads = max_threads
        self.threads = []

    def start_thread(self, *args, **kwargs):
        if len(self.threads) >= self.max_threads:
            return False
        t = JinniThread(self, self.fn, *args, **kwargs)
        t.start()
        return True

    def register(self, thd):
        if thd.name in self.threads:
            print("ERR: duplicate thread register???")
        self.threads.append(thd.name)
        print(self.threads)

    def unregister(self, thd):
        if not thd.name in self.threads:
            print("ERR: can't remove a thread not registered")
        self.threads.remove(thd.name)
        print(self.threads)


class JinniThread(threading.Thread):
    def __init__(self, parent, fn, *args, **kwargs):
        self.parent = parent
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        threading.Thread.__init__(self)

    def run(self):
        self.parent.register(self)
        self.fn(*self.args, **self.kwargs)
        self.parent.unregister(self)


class HttpListener(object):
    """ Very simple, threaded, listener class intended to act as a front end for
        various http based servers.
    """
    def __init__(self, host='', port=8080, connection_handler=None):
        self.host = host
        self.port = port
        self.backlog = 5
        self.socket = None
        self.handler = connection_handler
        self.running = False
        self.accept_thread = None
        self.connections = []

    def start(self):
        if not self.socket:
            self._make_socket()
#        print("HTTP 1.1 Listener started on ", self.host, ":", self.port)
        self.running = True
        self.accept_thread = threading.Thread(target=self._accept_loop)
        self.accept_thread.start()

    def stop(self):
        print("HttpListener: stop!")
#        self.running = False

        self.socket.shutdown(SHUT_RD)
        for c in self.connections:
            c.stop()

        self.socket.close()
#        print("socket has been closed...")
        if self.running:
            self.running = False
            try:
                self.accept_thread.join()
            except KeyboardInterrupt as e:
                pass
        print("Accept Thread has stopped...")

    def _make_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)

    def _accept_loop(self):
#        print("accept_thread: ", self)
        threads = 0
        while self.running:
            r, w, e = select.select([self.socket], [], [self.socket])
            if e:
                break
            if not r:
                continue

            try:
                ns = self.socket.accept()
                conn = Connection(self, *ns)
                self.connections.append(conn)
                conn.start(self.handler)
            except socket.timeout as e:
                continue
            except OSError as e:
                break
            except socket.error:
                break

#        print("Accept thread exiting...")
        self.running = False
