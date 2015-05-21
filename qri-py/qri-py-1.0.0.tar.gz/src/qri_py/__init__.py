import socket
import logging

import msgpack


class QriPython:

    def __init__(self, host=None, port=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((host, port))
        except socket.error, msg:
            logging.error("[QRI-PY] Server {0}:{1} unreachable: {2}".format(host, port, msg))

    def send(self, peer=None, checksum=None, message=None):
        packed_data = msgpack.packb([peer, checksum, message])

        try:
            self.sock.send(packed_data)
        except socket.error, msg:
            logging.error("[QRI-PY] Error occurred during sending: {0}".format(msg))

    def close(self):
        self.sock.close()
