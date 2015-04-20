import mimetypes
import re
import socket
from datetime import datetime
from os import path

try:
    from urllib import unquote
except:
    from urllib.parse import unquote


DEFAULT_MSGS = {
    200: 'OK',
    206: 'Partial Content',
    301: 'Moved permanently',
    307: 'Moved temporarily',
    404: 'Not found',
    500: 'Server error',
    501: 'Method not implemented'
}


class PlainHttpBase(object):
    CONN_CLOSE = 1
    CONN_KEEPALIVE = 2
    EOL = b"\r\n"
    HEADER_RE = re.compile("^([A-Za-z\-]+):[ ]+(.*)")

    def __init__(self, sock=None, data=None):
        self.headers = {}
        self.version = 0
        self.content = None
        self.conn_type = self.CONN_CLOSE
        self.raw = None

        if sock:
            self.from_socket(sock)
        elif data:
            self.from_data(data)

    def from_socket(self, sock):
        """ Read data from a socket and parse it as an HTTP response.
            Returns True if a response was read, False if there was an error
            or incomplete response.
        """
        bytes_read = b''
        while True:
            (ck, r) = self._read_from_socket(sock, 1024)
            if not ck or len(r) == 0:
                break
            bytes_read += r
            if self.EOL + self.EOL in bytes_read:
                break

        if len(bytes_read) == 0:
            print("zero bytes read...")
            return False

        self.raw = bytes_read
        hdrs, remainder = bytes_read.split(self.EOL + self.EOL, 1)
        if len(hdrs) == 0:
            return False

        hdrs = hdrs.decode()
        if not self._parse_headers(hdrs):
            return False

        self._connection_type()
        self._range()
        return self._complete(remainder, sock)

    def from_data(self, data):
        hdrs, remainder = data.split(self.EOL + self.EOL, 1)
        if len(hdrs) == 0:
            return False
        self._parse_headers(hdrs)
        self._connection_type()
        self._range()
        return self._complete(remainder)

    def __setitem__(self, key, val):
        self.headers[key] = val

    def get(self, key, default=None):
        poss = self[key]
        if poss:
            return poss
        return default

    def __getitem__(self, key):
        for k,v in self.headers.items():
            if key.lower() == k.lower():
                return v
        return None

    # These MUST be defined in the child class.
    def _first_header(self, line):
        raise NotImplementedError

    # Internal functions.
    def _parse_headers(self, hdrs):
        """ Split and parse headers. This expects a string not bytes. """
        lines = hdrs.split("\r\n")
        if not self._first_header(lines.pop(0)):
            return False

        for line in lines:
            ck = self.HEADER_RE.match(line)
            if ck:
                self.headers[ck.group(1)] = ck.group(2).strip()
        return True

    def _complete(self, existing, sock=None):
        cl = self['content-length']
        if cl is None:
            # todo - add other methods here...
            return True
        cl = int(cl)
#        print("content-length = ", cl)
        if cl < 1:
            return True
        if cl <= len(existing):
            self.content = existing[:cl]
            return True

        if sock is None:
            return False

        rqd = cl - len(existing)
        while True:
            (ck, r) = self._read_from_socket(sock, rqd)
            if not ck or len(r) == 0:
                break
            existing += r
            rqd = cl - len(existing)
            if rqd == 0:
                break
        self.content = existing

        return True

    def _connection_type(self):
        if self.version >= 11:
            self.conn_type = self.CONN_KEEPALIVE
        conn = self.headers.get('connection')
        if conn is None:
            return
        if conn.lower() == 'close':
            self.conn_type = self.CONN_CLOSE
        elif conn.lower() == 'keep-alive':
            self.conn_type = self.CONN_KEEPALIVE

    def _range(self):
        rr = self.headers.get('range')
        if rr is None or not rr.startswith('bytes='):
            return
        a,b = rr[6:].split('-')
        if b == '':
            b = '-1'
        self.ranges.append((int(a),int(b)))

    def _read_from_socket(self, sock, rqd=1024):
        """ Read data from socket. Return a tuple of True or False with any
            data read.
        """
        while True:
            try:
                r = sock.recv(rqd)
                if len(r):
                    return True, r
            except socket.error as e:
                break
        return False, b''


class PlainRequest(PlainHttpBase):
    CMD_RE = re.compile("^([A-Z]+)[ ]+([\/A-Za-z0-9\.\-_\&%]+)[ ]+HTTP\/([0-9]\.[0-9])")

    def __init__(self, sock):
        PlainHttpBase.__init__(self)
        self.verb = ''
        self.url = ''
        self.sock = sock
        self.valid = self.from_socket(sock)

    def __bytes__(self):
        return b"{0} {1} from {2}".format(self.verb, self.url, self.sock)

    def _first_header(self, line):
        ck = self.CMD_RE.match(line)
        if not ck:
            return False
        self.verb = ck.group(1)
        self.url = unquote(ck.group(2))
        self.version = int(ck.group(3)[0]) * 10 + int(ck.group(3)[2])
        return True


class PlainResponse(PlainHttpBase):
    STATUS_RE = re.compile("^HTTP/([0-9]\.[0-9])[ ]+([0-9]{3})[ ]+(.*)")

    def __init__(self, code=0, msg=None, socket=None):
        PlainHttpBase.__init__(self)
        self.code = code
        self.msg = msg
        self.version = 0
        if socket:
            self.from_socket(socket)

    def _first_header(self, line):
        """ HTTP/1.1 200 OK """
        ck = self.STATUS_RE.match(line)
        if not ck:
            return False
        self.code = int(ck.group(2))
        self.msg = ck.group(3)
        self.version = int(ck.group(1)[0]) * 10 + int(ck.group(1)[2])
        return True

    def add_standard(self):
        self.headers['Date'] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.headers['Accept-Ranges'] = 'bytes'
        self.headers['Server'] = 'Jinni/0.1.0'
        self.headers['Connection'] = 'Keep-Alive'

    def set_content(self, content, ctype=None):
        self.content = content
        # todo - handle encoding!
        self.headers['Content-Length'] = len(self.content)
        if ctype:
            self.headers['Content-Type'] = ctype

    def content_from_file(self, filename):
        ct, enc = mimetypes.guess_type(path.basename(filename))
        with open(filename, 'rb') as fh:
            self.headers['Content-Type'] = ct.lower()
            self.content = fh.read()
            self.headers['Content-Length'] = len(self.content)

    def build_response(self):
        if self.msg is None:
            self.msg = DEFAULT_MSGS.get(self.code, 'Add description here')
        # Add a zero byte length if we have no content
        if self.content is None or len(self.content) == 0:
            self.headers['Content-Length'] = 0

        lines = ["HTTP/1.1 {0} {1}".format(self.code, self.msg)]
        for k,v in self.headers.items():
            lines.append("{0}: {1}".format(k,v))
        resp = self.EOL.join([l.encode('utf-8') for l in lines]) + self.EOL + self.EOL
        if self.content:
            if isinstance(self.content, str):
                try:
                    resp += self.content.encode('utf-8')
                except UnicodeDecodeError:
                    resp += self.content
            else:
                resp += self.content
        return resp
