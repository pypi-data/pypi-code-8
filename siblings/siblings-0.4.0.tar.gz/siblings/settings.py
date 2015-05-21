import logging
import logging.config
from tornado.log import LogFormatter as TornadoLogFormatter
import tornado
import tornado.template
from tornado.options import define, options
import types
import os


# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("db", default=path(ROOT, "test", "TestDb.h5"), help="siblings hdf5 database file")
define("debug", default=False, help="debug mode")
tornado.options.parse_command_line()

STATIC_ROOT = path(ROOT, 'static')
TEMPLATE_ROOT = path(ROOT, 'templates')

# Deployment Configuration
class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    SOLO = "SOLO"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }

if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

settings = {}
settings['debug'] = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug
settings['static_path'] = STATIC_ROOT
try:
    cookie = os.environ['COOKIE_SECRET']
except KeyError:
    logging.warning("you haven't specified a COOKIE_SECRET in the environment")
    cookie = "Non-safe-cookie_secret"
settings['cookie_secret'] = cookie
settings['xsrf_cookies'] = False
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)

# Pulled from commonware.log we don't have to import that, which drags with
# it Django dependencies.
class RemoteAddressFormatter(logging.Formatter):
    """Formatter that makes sure REMOTE_ADDR is available."""

    def format(self, record):
        if ('%(REMOTE_ADDR)' in self._fmt
                and 'REMOTE_ADDR' not in record.__dict__):
            record.__dict__['REMOTE_ADDR'] = None
        return logging.Formatter.format(self, record)

class UTF8SafeFormatter(RemoteAddressFormatter):
    def __init__(self, fmt=None, datefmt=None, encoding='utf-8'):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.encoding = encoding

    def formatException(self, e):
        r = logging.Formatter.formatException(self, e)
        if type(r) in [types.StringType]:
            r = r.decode(self.encoding, 'replace') # Convert to unicode
        return r

    def format(self, record):
        t = RemoteAddressFormatter.format(self, record)
        if type(t) in [types.UnicodeType]:
            t = t.encode(self.encoding, 'replace')
        return t

if settings['debug']:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

base_fmt = ('%(name)s:%(levelname)s %(message)s:%(pathname)s:%(lineno)s')
LOGGERS = {
        'version': 1,
        'filters': {},
        'formatters': {
            'debug': {
                '()': UTF8SafeFormatter,
                'datefmt': '%H:%M:%s',
                'format': '%(asctime)s ' + base_fmt,
            },
            'prod': {
                '()': UTF8SafeFormatter,
                'datefmt': '%H:%M:%s',
                'format': '[%%(REMOTE_ADDR)s] %s' % (base_fmt),
            },
            'tornado': {
                '()': TornadoLogFormatter,
                'color': True
            },
        },
        'handlers': {
            'console': {
                '()': logging.StreamHandler,
                'formatter': 'tornado'
            },
            'null': {
                '()': logging.NullHandler,
            },
        },
        'loggers': {
            'siblings': {
                'handlers': ['console'],
                'level': LOG_LEVEL,
                'propagate': False
            }
        }
    }
#logging.config.dictConfig(LOGGERS)

if options.config:
    tornado.options.parse_config_file(options.config)