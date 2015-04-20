import threading
from .bases import PlainRequest


class Connection(object):
    """ A class to handle communication with an accepted socket from an HttpListener.
        These will generally be run in their own thread and so have their own lifespan.
    """
    def __init__(self, parent, sock, addr):
        self.parent = parent
        self.socket = sock
        self.addr = addr
        self.keepalive = False
        self.worker_thread = None

    def send(self, response):
        msg = response.build_response()
        try:
            self.socket.sendall(msg)
            return True
        except BrokenPipeError as e:
            return False

    def start(self, handler):
        if self.worker_thread:
            return
        try:
            self.worker_thread = threading.Thread(target=handler, args=(self, ), daemon=True)
        except TypeError:
            self.worker_thread = threading.Thread(target=handler, args=(self, ))
            self.worker_thread.daemon = True
        self.worker_thread.start()

    def stop(self):
        self.close()

    def close(self):
        self.socket.close()

    def next(self):
        if not self.keepalive:
            print("Next: closing socket...")
            self.socket.close()
            self.socket = None
            return False
        return True

    def process(self):
        """ Try to read from the socket until we have found the end of the request. """
        request = PlainRequest(self.socket)
        if not request.valid:
            print(request.raw)
            return None
        return request
