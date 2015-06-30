from .base import NuoDBDialect


# def print_list(*args):
# if args is None:
#         print "None list"
#     if args is not None:
#         for count, thing in enumerate(args):
#             print '{0}. {1}'.format(count, thing)
#
#
# def print_kwargs(**kwargs):
#     for key, value in kwargs.iteritems():
#         print "%s = %s" % (key, value)


class NuoDBDialect_pynuodb(NuoDBDialect):
    name = "nuodb"
    driver = 'pynuodb'

    @classmethod
    def dbapi(cls):
        return __import__('pynuodb')

    def initialize(self, connection):
        super(NuoDBDialect_pynuodb, self).initialize(connection)
        connection.execute('SELECT 1 FROM DUAL')

    def _get_server_version_info(self, connection):
        return connection.scalar("SELECT GETRELEASEVERSION() FROM DUAL")

    def create_connect_args(self, url):
        kwargs = url.translate_connect_args(username='user')
        if kwargs.get('port'):
            kwargs['host'] = "%s:%s" % (kwargs['host'], kwargs['port'])
            del kwargs['port']
        kwargs['options'] = dict(url.query)
        # if False: print_kwargs(**kwargs)
        return [], kwargs


dialect = NuoDBDialect_pynuodb
