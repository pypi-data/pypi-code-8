"""
This service implements a fictitious processor so we can perform online
transactions:

- holds
- ...

and offline submissions:

- capture
- credit
- ...

on funding instruments:

- credit card
- bank account
- ...

and simulate their settlement. It also does:

- merchant provisioning

All of this is implemented by ``domain``. The remainder is **cruft** for
exposing ``domain`` in different ways:

- Terminal commands via ``commands``
- HTTP via ``http``
- SFTP via ``sftp```

"""
__version__ = '0.1.1'

__all__ = [
    'http',
    'sftp',
    'commands',
    'config',
    'db',
    'domain',
    'init',
]


import logging

import coid
import newrelic.agent
import ohmr


tracer = ohmr.Tracer(coid.Id(prefix='OHM-'))


from . import config
from . import form
from .form import Form
from . import mime
from . import db
from . import domain
from . import commands
from . import http
from . import sftp


logger = logging.getLogger(__name__)


def init(conf_file=None):
    if conf_file:
        logger.info('loading config from "%s"', conf_file)
        execfile(conf_file, {'config': config})
    if config.NEWRELIC['config_file']:
        newrelic.agent.initialize(**config.NEWRELIC)
    db.init(config)
    domain.init(config)
    http.init(config)
    sftp.init(config)


class VersionLogFilter(logging.Filter):

    version = None

    def __init__(self, default='-'):
        super(VersionLogFilter, self).__init__()
        self.default = default

    def filter(self, record):
        record.version = __version__
        return True


class TraceIdLogFilter(logging.Filter):

    def __init__(self, default='-'):
        super(TraceIdLogFilter, self).__init__()
        self.default = default

    def filter(self, record):
        record.trace_id = tracer.id
        return True
