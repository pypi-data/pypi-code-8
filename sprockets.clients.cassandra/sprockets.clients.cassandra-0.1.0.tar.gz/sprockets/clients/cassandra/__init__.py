"""
clients.cassandra
=================

Base functionality for accessing/modifying data in Cassandra.

"""
import os
import socket

from cassandra.cluster import Cluster
from tornado.concurrent import Future
from tornado.ioloop import IOLoop

try:
    from urllib.parse import urlsplit
except:
    from urlparse import urlsplit

version_info = (0, 1, 0)
__version__ = '.'.join(str(v) for v in version_info)

DEFAULT_URI = 'cassandra://localhost:9042'
DEFAULT_PORT = 9042


class CassandraConnection(object):
    """Maintain a connection to a Cassandra cluster.

    The Sprockets Cassandra client handles provides the glue
    needed to join the Tornado async I/O module with the native
    python async I/O used in the Cassandra driver. The
    constructor of the function will grab the current handle
    to the underlying Tornado I/O loop so that a Tornado future
    result can be returned to the host application.

    Configuration parameters for the module are obtained from
    environment variables. Currently, the only variable is
    ``CASSANDRA_URI``, which takes the format "cassandra://hostname".
    If not located, the hostname defaults to localhost.

    .. note::

        The hostname in the ``CASSANDRA_URI`` will be resolved
        to a list of IP addresses that will be passed to the
        Cassandra driver as the contact points.

    """

    def __init__(self, ioloop=None):
        self._config = self._get_cassandra_config()
        self._cluster = Cluster(contact_points=self._config['contact_points'],
                                port=self._config['port'])
        self._session = self._cluster.connect()
        self._ioloop = IOLoop.current()

    def _get_cassandra_config(self):
        """Retrieve a dict containing Cassandra client config params."""
        parts = urlsplit(os.environ.get('CASSANDRA_URI', DEFAULT_URI))
        if parts.scheme != 'cassandra':
            raise RuntimeError(
                'CASSANDRA_URI scheme is not "cassandra://"!')

        _, _, ip_addresses = socket.gethostbyname_ex(parts.hostname)
        if not ip_addresses:
            raise RuntimeError('Unable to find Cassandra in DNS!')

        return {
            'contact_points': ip_addresses,
            'port': parts.port or DEFAULT_PORT,
        }

    def set_keyspace(self, keyspace):
        """Set the keyspace used by the connection."""
        self._session.set_keyspace(keyspace)

    def shutdown(self):
        """Shutdown the connection to the Cassandra cluster."""
        self._cluster.shutdown()
        self._session = None
        self._cluster = None

    def execute(self, query, *args, **kwargs):
        """Asynchronously execute the specified CQL query.

        The execute command also takes optional parameters and trace
        keyword arguments. See cassandra-python documentation for
        definition of those parameters.
        """

        tornado_future = Future()
        cassandra_future = self._session.execute_async(
            query, *args, **kwargs)
        self._ioloop.add_callback(
            self._callback, cassandra_future, tornado_future)
        return tornado_future

    def _callback(self, cassandra_future, tornado_future):
        """Cassandra async I/O loop callback handler."""
        try:
            result = cassandra_future.result()
        except Exception as exc:
            return tornado_future.set_exception(exc)
        tornado_future.set_result(result)
