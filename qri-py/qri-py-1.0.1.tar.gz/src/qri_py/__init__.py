import socket
import logging

import msgpack


class QriPython:

    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
        self.sock = None

        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((self.host, self.port))
            return self.sock

        except socket.error, msg:
            logging.error("[QRI-PY] Server {0}:{1} unreachable: {2}".format(
                self.host, self.port, msg
            ))
            return None

    def close(self):
        return self.sock.close()

    def reconnect(self):
        self.close()
        return self.connect()

    def send(self, peer=None, checksum=None, message=None):
        packed_data = msgpack.packb([peer, checksum, message])

        try:
            return self.sock.send(packed_data)
        except socket.error:
            sock = self.reconnect()
            if not sock:
                return None

            try:
                return sock.send(packed_data)
            except socket.error, msg:
                logging.error("[QRI-PY] Error occurred during sending: {0}".format(msg))
                return None
