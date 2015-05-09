#!/usr/bin/env python
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
    'disable_existing_loggers': True,
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
            'format': str('%(asctime)s %(module)s:%(lineno)-4d ' +
                      '%(levelname)-8s %(message)s'),
            },
        },
    'loggers' : {
        'griffin': {
            'level':'DEBUG',
            'handlers':['console'],
            'propogate' : True,
            },
        },
    }
