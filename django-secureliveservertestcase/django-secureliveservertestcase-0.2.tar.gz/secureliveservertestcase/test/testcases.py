import os
import socket
import threading
import ssl

from OpenSSL import crypto

from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIServer
from django.db import connections
from django.test.testcases import _MediaFilesHandler, _StaticFilesHandler
from django.test.testcases import QuietWSGIRequestHandler, TransactionTestCase


def generate_ssl_pair():
    FILE_KEY = '/tmp/localserver.key'
    FILE_CRT = '/tmp/localserver.crt'

    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, 1024)

    cert = crypto.X509()
    cert.get_subject().C = "GB"
    cert.get_subject().ST = "State"
    cert.get_subject().L = "Locality"
    cert.get_subject().O = "Organization"
    cert.get_subject().OU = "OrganizationUnit"
    cert.get_subject().CN = '127.0.0.1'
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(pkey)
    cert.sign(pkey, 'sha1')

    open(FILE_KEY, 'wb').write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
    open(FILE_CRT, 'wb').write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    return (FILE_KEY, FILE_CRT)


class SecureWSGIRequestHandler(QuietWSGIRequestHandler):
    def get_environ(self):
        env = super(SecureWSGIRequestHandler, self).get_environ()
        env['HTTPS'] = 'on'
        return env


class LiveServerThread(threading.Thread):
    """
    Thread for running a live http server while the tests are running.
    """

    def __init__(self, host, possible_ports, static_handler, connections_override=None,
                 use_ssl=False):
        self.host = host
        self.port = None
        self.possible_ports = possible_ports
        self.is_ready = threading.Event()
        self.error = None
        self.static_handler = static_handler
        self.connections_override = connections_override
        if use_ssl:
            self.key, self.certificate = generate_ssl_pair()
        self.use_ssl = use_ssl
        super(LiveServerThread, self).__init__()

    def run(self):
        """
        Sets up the live server and databases, and then loops over handling
        http requests.
        """
        if self.connections_override:
            # Override this thread's database connections with the ones
            # provided by the main thread.
            for alias, conn in self.connections_override.items():
                connections[alias] = conn
        try:
            # Create the handler for serving static and media files
            handler = self.static_handler(_MediaFilesHandler(WSGIHandler()))

            # Go through the list of possible ports, hoping that we can find
            # one that is free to use for the WSGI server.
            for index, port in enumerate(self.possible_ports):
                try:

                    if self.use_ssl:            
                        self.httpd = WSGIServer(
                            (self.host, port), SecureWSGIRequestHandler)
                        self.httpd.socket = self.wrap_socket(self.httpd.socket)
                    else:
                        self.httpd = WSGIServer(
                            (self.host, port), QuietWSGIRequestHandler)

                except socket.error as e:
                    if (index + 1 < len(self.possible_ports) and
                            e.errno == errno.EADDRINUSE):
                        # This port is already in use, so we go on and try with
                        # the next one in the list.
                        continue
                    else:
                        # Either none of the given ports are free or the error
                        # is something else than "Address already in use". So
                        # we let that error bubble up to the main thread.
                        raise
                else:
                    # A free port was found.
                    self.port = port
                    break

            self.httpd.set_app(handler)
            self.is_ready.set()
            self.httpd.serve_forever()
        except Exception as e:
            self.error = e
            self.is_ready.set()

    def wrap_socket(self, socket):
        return ssl.wrap_socket(self.httpd.socket, certfile=self.certificate,
                               keyfile=self.key, server_side=True,
                               ssl_version=ssl.PROTOCOL_TLSv1,
                               cert_reqs=ssl.CERT_NONE)

    def terminate(self):
        if hasattr(self, 'httpd'):
            # Stop the WSGI server
            self.httpd.shutdown()
            self.httpd.server_close()

        if self.use_ssl:
            os.remove(self.certificate)
            os.remove(self.key)


class SecureLiveServerTestCase(TransactionTestCase):
    """
    Does basically the same as TransactionTestCase but also launches a live
    http server in a separate thread so that the tests may use another testing
    framework, such as Selenium for example, instead of the built-in dummy
    client.
    Note that it inherits from TransactionTestCase instead of TestCase because
    the threads do not share the same transactions (unless if using in-memory
    sqlite) and each thread needs to commit all their transactions so that the
    other thread can see the changes.
    """

    static_handler = _StaticFilesHandler

    @property
    def live_server_url(self):
        return 'http://%s:%s' % (
            self.server_thread.host, self.server_thread.port)

    @property
    def live_server_url_ssl(self):
        return 'https://%s:%s' % (
            self.server_thread.host, self.server_thread_ssl.port)

    @classmethod
    def setUpClass(cls):
        super(SecureLiveServerTestCase, cls).setUpClass()
        cls.server_thread = cls.setUpServer(False)
        cls.server_thread_ssl = cls.setUpServer(True)

    @classmethod
    def setUpServer(cls, use_ssl):
        connections_override = {}
        for conn in connections.all():
            # If using in-memory sqlite databases, pass the connections to
            # the server thread.
            if conn.vendor == 'sqlite' and conn.is_in_memory_db(conn.settings_dict['NAME']):
                # Explicitly enable thread-shareability for this connection
                conn.allow_thread_sharing = True
                connections_override[conn.alias] = conn

        # Launch the live server's thread
        if use_ssl:
            specified_address = os.environ.get(
                'DJANGO_LIVE_TEST_SERVER_ADDRESS', 'localhost:8082')
        else:
            specified_address = os.environ.get(
                'DJANGO_LIVE_TEST_SERVER_ADDRESS', 'localhost:8081')

        # The specified ports may be of the form '8000-8010,8080,9200-9300'
        # i.e. a comma-separated list of ports or ranges of ports, so we break
        # it down into a detailed list of all possible ports.
        possible_ports = []
        try:
            host, port_ranges = specified_address.split(':')
            for port_range in port_ranges.split(','):
                # A port range can be of either form: '8000' or '8000-8010'.
                extremes = list(map(int, port_range.split('-')))
                assert len(extremes) in [1, 2]
                if len(extremes) == 1:
                    # Port range of the form '8000'
                    possible_ports.append(extremes[0])
                else:
                    # Port range of the form '8000-8010'
                    for port in range(extremes[0], extremes[1] + 1):
                        possible_ports.append(port)
        except Exception:
            msg = 'Invalid address ("%s") for live server.' % specified_address
            six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg), sys.exc_info()[2])
        server_thread = LiveServerThread(host, possible_ports,
                                             cls.static_handler,
                                             connections_override=connections_override,
                                             use_ssl=use_ssl)
        server_thread.daemon = True
        server_thread.start()

        # Wait for the live server to be ready
        server_thread.is_ready.wait()
        if server_thread.error:
            # Clean up behind ourselves, since tearDownClass won't get called in
            # case of errors.
            cls._tearDownClassInternal()
            raise server_thread.error

        return server_thread

    @classmethod
    def _tearDownClassInternal(cls):
        # There may not be a 'server_thread' attribute if setUpClass() for some
        # reasons has raised an exception.
        if hasattr(cls, 'server_thread'):
            # Terminate the live server's thread
            cls.server_thread.terminate()
            cls.server_thread.join()

        if hasattr(cls, 'server_thread_ssl'):
            cls.server_thread_ssl.terminate()
            cls.server_thread_ssl.join()

        # Restore sqlite in-memory database connections' non-shareability
        for conn in connections.all():
            if conn.vendor == 'sqlite' and conn.is_in_memory_db(conn.settings_dict['NAME']):
                conn.allow_thread_sharing = False

    @classmethod
    def tearDownClass(cls):
        cls._tearDownClassInternal()
        super(SecureLiveServerTestCase, cls).tearDownClass()

