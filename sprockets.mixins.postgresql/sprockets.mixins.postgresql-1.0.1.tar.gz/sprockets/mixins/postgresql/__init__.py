"""
PostgreSQL Client Mixins
========================

Sprockets mixins that automatically connects to PostgreSQL using
`sprockets.clients.postgresql <http://sprocketsclientspostgresql.rtfd.org>`_.

Handlers implementing one of the mixins should set an attribute called
``DBNAME`` that specifies the database name to connect to. The value of
``DBNAME`` will be passed into the creation of the
:py:class:`Session <sprockets.clients.postgresql.Session>` or
:py:class:`TornadoSession <sprockets.clients.postgresql.TornadoSession>`
object.

The Session classes wrap the Queries :py:class:`Session <queries.Session>` or
:py:class:`TornadoSession <queries.tornado_session.TornadoSession>` providing
environment variable based configuration.

The environment variables should be set using the ``DBNAME_[VARIABLE]`` format
where ``[VARIABLE]`` is one of  ``HOST``, ``PORT``, ``DBNAME``, ``USER``, and
``PASSWORD``.

"""
version_info = (1, 0, 1)
__version__ = '.'.join(str(v) for v in version_info)

from sprockets.clients import postgresql


class HandlerMixin(object):
    """A handler mixin for connecting to PostgreSQL. The mixin automatically
    creates the database session using the DBNAME attribute of the class as
    the database name for the
    :py:class:`Session <sprockets.clients.postgresql.Session>` object
    creation.

    Using the mixin, the name of the session attribute will be
    ``<dbname>_session``, automatically created when initializing the object.

    Example:

    .. code:: python

        from sprockets.mixins import postgresql
        from tornado import web


        class FooRequestHandler(postgresql.HandlerMixin,
                                web.RequestHandler,):

            DBNAME = 'foo'

            def get(self, *args, **kwargs):
                result = self.foo_session.query('SELECT * FROM bar')
                self.finish({'data': result.items()})

    """
    DBNAME = 'postgres'

    def initialize(self):
        setattr(self,
                '%s_session' % self.DBNAME,
                postgresql.Session(self.DBNAME))
        try:
            super(HandlerMixin, self).initialize()
        except AttributeError:
            pass


class AsyncHandlerMixin(object):
    """A asynchronous Tornado handler mixin for connecting to PostgreSQL. The
    mixin automatically creates the database session using the DBNAME attribute
    of the class as the database name for the
    :py:class:`TornadoSession <sprockets.clients.postgresql.TornadoSession>`
    object creation.

    Using the mixin, the name of the session attribute will be
    ``<dbname>_session``, automatically created when initializing the object.

    Example:

    .. code:: python

        from sprockets.mixins import postgresql
        from tornado import web


        class FooRequestHandler(postgresql.AsyncHandlerMixin,
                                web.RequestHandler):

            DBNAME = 'foo'

            @web.asynchronous
            def get(self, *args, **kwargs):
                result = yield self.foo_session.query('SELECT * FROM bar')
                self.finish({'data': result.items()})
                result.free()

    """
    DBNAME = 'postgres'

    def initialize(self):
        setattr(self,
                '%s_session' % self.DBNAME,
                postgresql.TornadoSession(self.DBNAME))
        try:
            super(AsyncHandlerMixin, self).initialize()
        except AttributeError:
            pass
