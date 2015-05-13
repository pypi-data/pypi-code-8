from __future__ import absolute_import

import logging.config

from kombu import Queue
from celery import Celery

import djcron_agent

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'redis://localhost/0'
CELERY_RESULT_BACKEND = 'redis://localhost/0'

CELERY_TIMEZONE = 'Europe/Madrid'
CELERY_ENABLE_UTC = True


DJCRON_BASE = 'cron'
DJCRON_ADMIN_QUEUE = '{base}.admin'.format(base=DJCRON_BASE)
DJCRON_ADMIN_ROUTING_KEY = '{base}.admin'.format(base=DJCRON_BASE)
DJCRON_AGENT_QUEUE = '{base}.agent'.format(base=DJCRON_BASE)
DJCRON_AGENT_ROUTING_KEY = '{base}.agent'.format(base=DJCRON_BASE)

CELERY_DEFAULT_EXCHANGE = '{base}.any'.format(base=DJCRON_BASE)
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'

CELERY_DEFAULT_QUEUE = DJCRON_ADMIN_QUEUE
CELERY_DEFAULT_ROUTING_KEY = DJCRON_ADMIN_ROUTING_KEY

CELERY_QUEUES = (
    Queue(DJCRON_ADMIN_QUEUE,
          routing_key='{key}.#'.format(key=DJCRON_ADMIN_ROUTING_KEY)),
    Queue(DJCRON_AGENT_QUEUE,
          routing_key='{key}.#'.format(key=DJCRON_AGENT_ROUTING_KEY)),
)

CELERY_ROUTES = (
    {'djcron_agent': {
        'routing_key': DJCRON_ADMIN_ROUTING_KEY,
        'queue': DJCRON_ADMIN_QUEUE,
    }},
)

app = Celery('djcron')

app.autodiscover_tasks((djcron_agent, ))


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "complete": {
            "format": "%(levelname)s:%(asctime)s:%(module)s %(message)s"
        },
        "simple": {
            "format": "%(levelname)s:%(asctime)s: %(message)s"
        },
        "null": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "djcron_agent": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        }
    }
}

logging.config.dictConfig(LOGGING)

# To run a celery worker:
#    celery worker--config=settings_agent --autoreload -q djcron
