#!/usr/bin/env python

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) 

import logging
import logging.config

from logutils.colorize import ColorizingStreamHandler

class ColorHandler(ColorizingStreamHandler):
    def __init__(self, *args, **kwargs):
        super(ColorHandler, self).__init__(*args, **kwargs)
        self.level_map = {
            # Provide you custom coloring information here
            logging.DEBUG: (None, 'blue', False),
            logging.INFO: (None, 'green', False),
            logging.WARNING: (None, 'yellow', False),
            logging.ERROR: (None, 'red', False),
            logging.CRITICAL: ('red', 'white', True),
        }

LOGGING = {
    'version':1,
    'disable_existing_loggers': False,
    'handlers':{
        'console': {
            '()':ColorHandler,
            'info':'white',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },
    },
    'formatters': {
        'detailed': {
            'format': str('%(levelname)-s ' +
                       '%(filename)s:%(lineno)-4d ' +
                       '%(funcName)-20s' +
                      '%(message)s'),
        },
    },
    'loggers' : {
        'goblin': {
            'level':'DEBUG',
            'handlers':['console'],
            'propogate' : True,
        },
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('goblin')
logger.debug("Logger is set up!")
