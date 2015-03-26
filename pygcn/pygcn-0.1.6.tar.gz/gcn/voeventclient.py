# Copyright (C) 2014  Leo Singer
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Anonymous VOEvent client for receiving GCNs in XML format, implementing the
VOEvent Transport Protocol <http://www.ivoa.net/documents/VOEventTransport>.
"""
__author__ = "Leo Singer <leo.singer@ligo.org>"


import socket
import struct
import time
# Prefer lxml.etree over xml.etree (it's faster)
try:
    import lxml.etree
    import io
    def parse_from_string(text):
        return lxml.etree.parse(io.BytesIO(text)).getroot()
    from lxml.etree import XMLSyntaxError
except ImportError:
    import xml.etree.cElementTree
    parse_from_string = xml.etree.cElementTree.fromstring
    try:
        from xml.etree.cElementTree import ParseError as XMLSyntaxError
    except ImportError: # Python 2.6 raises a different exception
        from xml.parsers.expat import ExpatError as XMLSyntaxError
import logging
import datetime
import base64


# Buffer for storing message size
_size_struct = struct.Struct("!I")
_size_len = _size_struct.size


def _get_now_iso8601():
    """Get current date-time in ISO 8601 format."""
    return datetime.datetime.now().isoformat()


def _open_socket(host, port, iamalive_timeout, max_reconnect_timeout, log):
    """Establish a connection. Wait 1 second after the first failed attempt.
    Double the timeout after each failed attempt thereafter, until the
    timeout reaches MAX_RECONNECT_TIMEOUT. Return the new, connected socket."""
    reconnect_timeout = 1
    while True:
        try:
            # Open socket
            sock = socket.socket()
            try:
                sock.settimeout(iamalive_timeout)
                log.debug("opened socket")

                # Connect to host
                sock.connect((host, port))
                log.info("connected to %s:%d", host, port)
            except socket.error:
                try:
                    sock.close()
                except socket.error:
                    log.exception("could not close socket")
                else:
                    log.info("closed socket")
                raise
        except socket.error:
            if reconnect_timeout < max_reconnect_timeout:
                reconnect_timeout <<= 1
            log.exception("could not connect to %s:%d, will retry in %d seconds", host, port, reconnect_timeout)
            time.sleep(reconnect_timeout)
        else:
            return sock


# memoryview was introduced in Python 2.7. If memoryview is not defined,
# fall back to an implementation that concatenates read-only buffers.
try:
    bytes
except NameError:
    bytes = buffer
try:
    memoryview

    def _recvall(sock, n):
        """Read exactly n bytes from a socket and return as a buffer."""
        ba = bytearray(n)
        mv = memoryview(ba)
        timeout = sock.gettimeout()
        start = time.clock()

        while n > 0:
            if time.clock() - start > timeout:
                raise socket.timeout(
                    'timed out while trying to read {0} bytes'.format(n))
            nreceived = sock.recv_into(mv, n)

            # According to the POSIX specification
            # http://pubs.opengroup.org/onlinepubs/009695399/functions/recv.html
            # "If no messages are available to be received and the peer has
            # performed an orderly shutdown, recv() shall return 0."
            if nreceived == 0:
                raise socket.error('connection closed by peer')

            n -= nreceived
            mv = mv[nreceived:]
        return bytes(ba)
except NameError:
    def _recvall(sock, n):
        """Read exactly n bytes from a socket and return as a buffer."""
        data = bytearray()
        timeout = sock.gettimeout()
        start = time.clock()

        while n > 0:
            if time.clock() - start > timeout:
                raise socket.timeout(
                    'timed out while trying to read {0} bytes'.format(n))
            newdata = sock.recv(n)

            # According to the POSIX specification
            # http://pubs.opengroup.org/onlinepubs/009695399/functions/recv.html
            # "If no messages are available to be received and the peer has
            # performed an orderly shutdown, recv() shall return 0."
            if len(newdata) == 0:
                raise socket.error('connection closed by peer')

            n -= len(newdata)
            data += newdata
        return bytes(data)


def _recv_packet(sock):
    """Read a length-prefixed VOEvent Transport Protocol packet and return the
    payload."""
    # Receive and unpack size of payload to follow
    payload_len, = _size_struct.unpack_from(_recvall(sock, 4))

    # Receive payload
    return _recvall(sock, payload_len)


def _send_packet(sock, payload):
    """Send an array of bytes as a length-prefixed VOEvent Transport Protocol
    packet."""
    # Send size of payload to follow
    sock.sendall(_size_struct.pack(len(payload)))

    # Send payload
    sock.sendall(payload)


def _form_response(role, origin, response, timestamp):
    """Form a VOEvent Transport Protocol packet suitable for sending an `ack`
    or `iamalive` response."""
    return ('''<?xml version='1.0' encoding='UTF-8'?><trn:Transport role="'''
        + role + '''" version="1.0" xmlns:trn="http://telescope-networks.org/schema/Transport/v1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://telescope-networks.org/schema/Transport/v1.1 http://telescope-networks.org/schema/Transport-v1.1.xsd"><Origin>'''
        + origin + '''</Origin><Response>''' + response
        + '''</Response><TimeStamp>''' + timestamp
        + '''</TimeStamp></trn:Transport>''').encode('UTF-8')


def _ingest_packet(sock, ivorn, handler, log):
    """Ingest one VOEvent Transport Protocol packet and act on it, first sending
    the appropriate response and then calling the handler if the payload is a
    VOEvent."""
    # Receive payload
    payload = _recv_packet(sock)
    log.debug("received packet of %d bytes", len(payload))
    log.debug("payload is:\n%s", payload)

    # Parse payload and act on it
    try:
        root = parse_from_string(payload)
    except XMLSyntaxError:
        log.exception("failed to parse XML, base64-encoded payload is:\n%s",
            base64.b64encode(payload))
        raise
    else:
        if root.tag == "{http://telescope-networks.org/schema/Transport/v1.1}Transport":
            if "role" not in root.attrib:
                log.error("receieved transport message without a role")
            elif root.attrib["role"] == "iamalive":
                log.debug("received iamalive message")
                _send_packet(sock, _form_response("iamalive", root.find("Origin").text, ivorn, _get_now_iso8601()))
                log.debug("sent iamalive response")
            else:
                log.error("received transport message with unrecognized role: %s", root.attrib["role"])
        elif root.tag in ("{http://www.ivoa.net/xml/VOEvent/v1.1}VOEvent", "{http://www.ivoa.net/xml/VOEvent/v2.0}VOEvent"):
            log.info("received VOEvent")
            if 'ivorn' not in root.attrib:
                log.error("received voevent message without ivorn")
            else:
                _send_packet(sock, _form_response("ack", root.attrib["ivorn"], ivorn, _get_now_iso8601()))
                log.debug("sent receipt response")
                if handler is not None:
                    try:
                        handler(payload, root)
                    except:
                        log.exception("exception in payload handler")
        else:
            log.error("received XML document with unrecognized root tag: %s", root.tag)


def listen(host="68.169.57.253", port=8099, ivorn="ivo://python_voeventclient/anonymous", iamalive_timeout=150, max_reconnect_timeout=1024, handler=None, log=None):
    """Connect to a VOEvent Transport Protocol server on the given `host` and
    `port`, then listen for VOEvents until interrupted (i.e., by a keyboard
    interrupt, `SIGINTR`, or `SIGTERM`).

    In response packets, this client is identified by `ivorn`.

    If `iamalive_timeout` seconds elapse without any packets from the server,
    it is assumed that the connection has been dropped; the client closes the
    connection and attempts to re-open it, retrying with an exponential backoff
    up to a maximum timeout of `max_reconnect_timeout` seconds.

    If `handler` is provided, it should be a callable that takes two arguments,
    the raw VOEvent payload and the ElementTree root object of the XML
    document. The `handler` callable will be invoked once for each incoming
    VOEvent. See also `gcn.handlers` for some example handlers.

    If `log` is provided, it should be an instance of `logging.Logger` and is
    used for reporting the client's status. If `log` is not provided, a default
    logger will be used.

    Note that this function does not return."""
    if log is None:
        log = logging.getLogger('gcn.listen')

    while True:
        sock = _open_socket(host, port, iamalive_timeout, max_reconnect_timeout, log)

        try:
            while True:
                _ingest_packet(sock, ivorn, handler, log)
        except socket.timeout:
            log.warn("timed out")
        except socket.error:
            log.exception("socket error")
        except XMLSyntaxError:
            log.warn("XML syntax error")
        finally:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except socket.error:
                log.exception("could not shut down socket")

            try:
                sock.close()
            except socket.error:
                log.exception("could not close socket")
            else:
                log.info("closed socket")


def serve(payloads, host='127.0.0.1', port=8099, retransmit_timeout=0, log=None):
    """Rudimentary GCN server, for testing purposes. Serves just one connection
    at a time, and repeats the same payloads in order, repeating, for each
    connection."""
    if log is None:
        log = logging.getLogger('gcn.serve')

    sock = socket.socket()
    try:
        sock.bind((host, port))
        log.info("bound to %s:%d", host, port)
        sock.listen(0)
        while True:
            conn, addr = sock.accept()
            log.info("connected to %s:%d", addr, port)
            try:
                i = 0
                while True:
                    _send_packet(conn, payloads[i])
                    i += 1
                    i %= len(payloads)
                    time.sleep(retransmit_timeout)
            except socket.error:
                log.exception('error communicating with peer')
            finally:
                try:
                    conn.shutdown(socket.SHUT_RDWR)
                except socket.error:
                    log.exception("could not shut down socket")

                try:
                    conn.close()
                except socket.error:
                    log.exception("could not close socket")
                else:
                    log.info("closed socket")
    finally:
        sock.close()
