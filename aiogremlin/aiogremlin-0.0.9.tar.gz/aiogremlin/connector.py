from urllib.parse import urlparse

import aiohttp


class BaseConnector(object):
    """Base connector class.

    :param conn_timeout: (optional) Connect timeout.
    :param keepalive_timeout: (optional) Keep-alive timeout.
    :param bool force_close: Set to True to force close and do reconnect
        after each request (and between redirects).
    :param loop: Optional event loop.
    """

    _closed = True  # prevent AttributeError in __del__ if ctor was failed
    _source_traceback = None

    def __init__(self, *, conn_timeout=None, force_close=False, limit=None,
                 connector=None, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._closed = False
        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))
        self._conns = {}
        self._acquired = defaultdict(list)
        self._conn_timeout = conn_timeout
        self._cleanup_handle = None
        self._force_close = force_close
        self._limit = limit
        self._waiters = defaultdict(list)
        self._loop = loop
        if connector is None:
            connector = aiohttp.TCPConnector(force_close=force_close)
        self._connector
        self._session = aiohttp.ClientSession()

    @property
    def force_close(self):
        """Ultimately close connection on releasing if True."""
        return self._force_close

    @property
    def limit(self):
        """The limit for simultaneous connections to the same endpoint.

        Endpoints are the same if they are have equal
        (host, port, is_ssl) triple.

        If limit is None the connector has no limit (default).
        """
        return self._limit

    def _cleanup(self):
        """Cleanup unused transports."""
        if self._cleanup_handle:
            self._cleanup_handle.cancel()
            self._cleanup_handle = None

        now = self._loop.time()

        connections = {}
        timeout = self._keepalive_timeout

        for key, conns in self._conns.items():
            alive = []

            for transport, proto, t0 in conns:
                if transport is not None:
                    if proto and not proto.is_connected():
                        transport = None
                    else:
                        delta = t0 + self._keepalive_timeout - now
                        if delta < 0:
                            transport.close()
                            transport = None
                        elif delta < timeout:
                            timeout = delta

                if transport is not None:
                    alive.append((transport, proto, t0))
            if alive:
                connections[key] = alive

        if connections:
            self._cleanup_handle = self._loop.call_at(
                ceil(now + timeout), self._cleanup)

        self._conns = connections

    def _start_cleanup_task(self):
        if self._cleanup_handle is None:
            now = self._loop.time()
            self._cleanup_handle = self._loop.call_at(
                ceil(now + self._keepalive_timeout), self._cleanup)

    def close(self):
        """Close all opened transports."""
        if self._closed:
            return
        self._closed = True

        try:
            if hasattr(self._loop, 'is_closed'):
                if self._loop.is_closed():
                    return

            for key, data in self._conns.items():
                for transport, proto, t0 in data:
                    transport.close()

            for transport in chain(*self._acquired.values()):
                transport.close()

            if self._cleanup_handle:
                self._cleanup_handle.cancel()

        finally:
            self._conns.clear()
            self._acquired.clear()
            self._cleanup_handle = None

    @property
    def closed(self):
        """Is connector closed.

        A readonly property.
        """
        return self._closed

    @asyncio.coroutine
    def ws_connect(self, url):
        """Get from pool or create new connection."""
        parsed = urlparse(url)
        host = parsed.hostname
        port = parsed.port
        ssl = parsed.scheme
        key = (host, port, ssl)

        # use short-circuit
        if self._limit is not None:
            while len(self._acquired[key]) >= self._limit:
                fut = asyncio.Future(loop=self._loop)
                self._waiters[key].append(fut)
                yield from fut

        connection = self._get(key)
        if transport is None:
            try:
                if self._conn_timeout:
                    transport, proto = yield from asyncio.wait_for(
                        self._create_connection(req),
                        self._conn_timeout, loop=self._loop)
                else:
                    transport, proto = yield from self._create_connection(req)
            except asyncio.TimeoutError as exc:
                raise ClientTimeoutError(
                    'Connection timeout to host %s:%s ssl:%s' % key) from exc
            except OSError as exc:
                raise ClientOSError(
                    'Cannot connect to host %s:%s ssl:%s' % key) from exc

        self._acquired[key].append(transport)
        conn = Connection(self, key, req, transport, proto, self._loop)
        return conn

    def _get(self, key):
        conns = self._conns.get(key)
        t1 = self._loop.time()
        while conns:
            connection = conns.pop()
            if not connection.closed():
                return connection
        return None

    def _release(self, key, req, transport, protocol, *, should_close=False):
        if self._closed:
            # acquired connection is already released on connector closing
            return

        acquired = self._acquired[key]
        try:
            acquired.remove(transport)
        except ValueError:  # pragma: no cover
            # this may be result of undetermenistic order of objects
            # finalization due garbage collection.
            pass
        else:
            if self._limit is not None and len(acquired) < self._limit:
                waiters = self._waiters[key]
                while waiters:
                    waiter = waiters.pop(0)
                    if not waiter.done():
                        waiter.set_result(None)
                        break

        resp = req.response

        if not should_close:
            if resp is not None:
                if resp.message is None:
                    should_close = True
                else:
                    should_close = resp.message.should_close

            if self._force_close:
                should_close = True

        reader = protocol.reader
        if should_close or (reader.output and not reader.output.at_eof()):
            conns = self._conns.get(key)
            if conns is not None and len(conns) == 0:
                # Issue #253: An empty array will eventually be
                # removed by cleanup, but it's better to pop straight
                # away, because cleanup might not get called (e.g. if
                # keepalive is False).
                self._conns.pop(key, None)

            transport.close()
        else:
            conns = self._conns.get(key)
            if conns is None:
                conns = self._conns[key] = []
            conns.append((transport, protocol, self._loop.time()))
            reader.unset_parser()

            self._start_cleanup_task()

    @asyncio.coroutine
    def _create_connection(self, req):
        raise NotImplementedError()
