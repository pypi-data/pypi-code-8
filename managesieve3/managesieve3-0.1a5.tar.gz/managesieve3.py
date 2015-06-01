#######################################################################
# managesieve3 is a python2 and python3 implementation an RFC-5804
#  client to remotely manage sieve scripts.
#
# Copyright 2015 True Blade Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Notes:
#  See https://pypi.python.org/pypi/managesieve for a python2 only
# module that provides basically the same functionality.
########################################################################

import re as _re
import ssl as _ssl
import socket as _socket
import base64 as _base64
import logging as _logging
import itertools as _itertools

__all__ = ['Managesieve', 'BaseException', 'ServerResponseNo', 'ServerResponseBye', 'ServerProtocolError']

# get the logger we're going to use
_logger = _logging.getLogger(__name__)

_RES_OK  = b'OK'
_RES_NO  = b'NO'
_RES_BYE = b'BYTE'

_CRLF = b'\r\n'

########################################################################
# exceptions

class BaseException(Exception):
    pass


class _ServerResponseBase(BaseException):
    def __init__(self, name, code, text, results):
        self.name = name.decode('ascii')
        self.code = None if code is None else code.decode('ascii').split('/')
        self.text = text
        self.results = results

    def __str__(self):
        return '{}(name={!r}, code={!r}, text={!r}, results={!r})'.format(self.__class__.__name__, self.name, self.code, self.text, self.results)


# the server returned a 'NO' response
class ServerResponseNo(_ServerResponseBase):
    pass


# the server returned a 'BYE' response
class ServerResponseBye(_ServerResponseBase):
    pass


# a protocol error: unexpected result from server server returned a 'BYE' response
class ServerProtocolError(BaseException):
    pass

#
########################################################################

########################################################################
# helper routines

# turns into an RFC-5840 "string", which is still bytes
def _stringify(bytes):
    return b'"' + bytes + b'"'


def _literal(bytes):
    # an RFC-5840 literal. can contain arbitrary bytes, since it's prefixed with the length
    return b''.join([b'{', str(len(bytes)).encode('ascii'), b'+}', _CRLF, bytes, _CRLF])


def _strip_crlf(line):
    if line[-2:] != _CRLF:
        raise ValueError('string expected to end with CR/LF')
    return line[:-2]

#
########################################################################

# various regexes
_re_oknobye = _re.compile(br'(?P<type>' + _RES_OK + b'|' + _RES_NO + b'|' + _RES_BYE + br')( \((?P<code>.*)\))?( (?P<rest>.*))?$')
_re_quote = _re.compile(br'"(?P<string>[^"]*)"( (?P<rest>.*))?$')
_re_atom  = _re.compile(br'(?P<atom>[^ ]+)( (?P<rest>.*))?$')
_re_literal = _re.compile(br'{(?P<length>\d+)}$')
_re_capability = _re.compile(br'"(?P<name>[^"]*)"( "(?P<value>[^"]*)")?$')

########################################################################
# routines to parse the responses

def _parse_simple(type, code, text, results):
    # we don't care about anything that's returned. we know it's OK
    return None


def _parse_capability(type, code, text, results):
    # parse each capability
    mechs = None
    implementation = None
    starttls = None

    caps = {}
    for name_value in results:
        # name_value must be length 1 or 2
        if len(name_value) == 1:
            name, value = name_value[0], None
        else:
            name, value = name_value

        caps[name.upper()] = value

    return caps


def _parse_authenticate(type, code, text, results):
    return None


def _parse_listscripts(type, code, text, results):
    result = set()
    default = None
    for r in results:
        # must be length 1 or 2
        if len(r) == 1:
            name, flag = r[0], None
        else:
            name, flag = r
        name = name.decode('utf-8')
        if flag is not None:
            if flag != b'ACTIVE':
                raise ValueError('unknown script flag %s' % flag)
            if default:
                raise ValueError('ACTIVE specified multiple times')
            default = name
        result.add(name)
    return result, default


def _parse_getscript(type, code, text, results):
    return results[0].decode('utf-8')

#
########################################################################

class Managesieve(object):
    # note we're not using 'brw': we read via the file, but write directly to the socket
    #  this is to prevent buffering the writes, which has an issue once TLS is running
    _filemode = 'br'

    def __init__(self, host=None, port=None):
        if host is None:
            host = 'localhost'
        if port is None:
            port = 4190

        _logger.info('connecting to %s:%s', host, port)
        self._sock = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        self._sock.connect((host, port))
        self._file = self._sock.makefile(self._filemode)

        # read the initial greeting, as if CAPABILITY had been executed
        self._capabilities = self._read_response_capability()


    # the supported commands, in RFC-5804 order

    def cmd_authenticate(self, auth_type, options=None):
        return self._command(b'AUTHENTICATE',
                             _parse_authenticate,
                             args=[_stringify(auth_type)],
                             options=options)


    def cmd_starttls(self, keyfile=None, certfile=None):
        self._command(b'STARTTLS', _parse_simple)
        self._sock = _ssl.wrap_socket(self._sock, keyfile=keyfile, certfile=certfile)
        self._file = self._sock.makefile(self._filemode)

        # now under TLS, read the capability result
        self._capabilities = self._read_response_capability()


    def cmd_logout(self):
        # forget our capabilities
        self._capabilities = None
        return self._command(b'LOGOUT',
                             _parse_simple)


    def cmd_capability(self):
        return self._command(b'CAPABILITY',
                             _parse_capability)


    def cmd_havespace(self, name, size):
        try:
            self._command(b'HAVESPACE',
                          _parse_simple,
                          args=[_stringify(name.encode('utf-8')),
                                str(size).encode('ascii')])
            return True, None, None
        except ServerResponseNo as ex:
            return False, ex.code, ex.text


    def cmd_putscript(self, name, contents):
        _stringify(name.encode('utf-8'))
        return self._command(b'PUTSCRIPT',
                             _parse_simple,
                             args=[_stringify(name.encode('utf-8')),
                                   _literal(contents.encode('utf-8'))])


    def cmd_listscripts(self):
        # returns a tuple: (scripts, active)
        # scripts is a set of script names that exist
        # active is either the name of the active script, or None if no active script exists
        return self._command(b'LISTSCRIPTS',
                             _parse_listscripts)


    def cmd_setactive(self, name):
        if name is None:
            name = ''
        return self._command(b'SETACTIVE',
                             _parse_simple,
                             args=[_stringify(name.encode('utf-8'))])


    def cmd_getscript(self, name):
        return self._command(b'GETSCRIPT',
                             _parse_getscript,
                             args=[_stringify(name.encode('utf-8'))])


    def cmd_deletescript(self, name):
        return self._command(b'DELETESCRIPT',
                             _parse_simple,
                             args=[_stringify(name.encode('utf-8'))])


    def cmd_renamescript(self, oldname, newname):
        return self._command(b'RENAMESCRIPT',
                             _parse_simple,
                             args=[_stringify(oldname.encode('utf-8')),
                                   _stringify(newname.encode('utf-8'))])


    def cmd_checkscript(self, contents):
        try:
            self._command(b'CHECKSCRIPT',
                          _parse_simple,
                          args=[_literal(contents.encode('utf-8'))])
            return True, None, None
        except ServerResponseNo as ex:
            return False, ex.code, ex.text


    def cmd_noop(self):
        return self._command(b'NOOP',
                             _parse_simple)


    def login_plain(self, username, authuser, password):
        # encode as UTF-8, then join with \0, then base64
        data = _base64.b64encode(b'\0'.join(s.encode('utf-8') for s in [username, authuser, password]))
        return self.cmd_authenticate(b'PLAIN', options=[data])


    def _command(self, name, parser, args=None, options=None):
        _logger.info('executing command %r', name)
        cmd = b' '.join(_itertools.chain([name], [] if args is None else args)) + _CRLF
        _logger.debug('C: %r', cmd)
        self._sock.send(cmd)
        #self._file.flush()
        if options:
            for o in options:
                cmd = _literal(o)
                _logger.debug('C: %r', cmd)
                self._sock.send(cmd)

        # get the response
        return self._read_response(name, parser)


    def _read_response_capability(self):
        return self._read_response(b'capability', _parse_capability)


    def _string_or_literal(self, line):
        # check for a literal. if so, read more
        # line is a bytes object
        m = _re_literal.match(line)
        if m:
            length = int(m.group('length'))

            # read 'length' bytes, then expect a cr/lf
            return _strip_crlf(self._file.read(length+2))
        else:
            # not a literal, just return the line without quotes
            # this odd construct is needed to get the first and list chars of the bytes object
            #  in both python2 and python3
            if not (line[0:1] == b'"' and line[len(line)-1:len(line)] == b'"'):
                raise ServerProtocolError('expecting string to have quotes, not {!r}'.format(line))
            return line[1:-1]


    def _read_response(self, name, parser):
        # read lines until we have a OK/NO/BYE
        results = []
        while True:
            line = self._readline()

            # check for ok/no/bye
            m = _re_oknobye.match(line)
            if m:
                # an ok/no/bye, parse and return
                type, code, text = m.group('type', 'code', 'rest')
                type = type.upper()
                if text is not None:
                    text = self._string_or_literal(text).decode('utf-8')

                _logger.info('response %s: %r %r %r %r', name, type, code, text, results)

                result = parser(type, code, text, results)
                _logger.debug('parsed response %s: %r', name, result)

                if type != _RES_OK:
                    if type == _RES_NO:
                        raise ServerResponseNo(name, code, text, results)
                    if type == _RES_BYE:
                        raise ServerResponseBye(name, code, text, results)
                    raise ServerProtocolError()

                return result

            # check for a literal
            m = _re_literal.match(line)
            if m:
                length = int(m.group('length'))

                # read 'length' bytes, then expect a cr/lf
                results.append(_strip_crlf(self._file.read(length+2)))
                continue

            # check for a list of quoted strings or atoms
            l = []
            while True:
                # the order is important here: check from quoted strings, them atoms
                m = _re_quote.match(line)
                if m:
                    l.append(m.group('string'))
                else:
                    m = _re_atom.match(line)
                    if m:
                        l.append(m.group('atom'))
                    else:
                        raise ValueError('invalid server response')
                line = m.group('rest')
                if line is None:
                    break
            results.append(l)


    def _readline(self):
        # read a line, but strip off the cr/lf
        # also, check for EOF
        line = self._file.readline()
        _logger.debug('S: %s', repr(line))
        if not line:
            raise IOError('readline: EOF')
        return _strip_crlf(line)
