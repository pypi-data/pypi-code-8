import logging.config
import os

LOGLEVEL = os.environ.get('LOGLEVEL', 'info')
LOGFILE = os.environ.get('LOGFILE', '/var/log/zymbit.log')


def config_logging(logfile=None, loglevel=None):
    logging.config.dictConfig(get_logging_config(logfile, loglevel))


def get_logging_config(logfile=None, loglevel=None):
    logfile = logfile or LOGFILE
    loglevel = (loglevel or LOGLEVEL).upper()

    return {
        'version': 1,
        'disable_existing_loggers': True,

        'formatters': {
            'default': {
                'format': '%(levelname)s %(asctime)s %(name)s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },

        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': loglevel,
                'stream': 'ext://sys.stdout',
                'formatter': 'default',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': logfile,
                'maxBytes': 1024 * 100,
                'backupCount': 2,
            },
            'null': {
                'class': 'logging.NullHandler',
                'level': 'DEBUG',
            },
        },

        'loggers': {
            '': {
                'handlers': ['console'],
                'propagate': True,
                'level': loglevel,
            },
            'filer': {
                'handlers': ['console', 'file'],
                'propagate': False,
                'level': loglevel,
            },
            'requests': {
                'handlers': ['null'],
                'propagate': False,
                'level': 'ERROR',
            },
        },
    }
