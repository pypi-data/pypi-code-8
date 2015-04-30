#!/usr/bin/env python
'''PyLibChorus -- Python Chorus API Library'''

import logging
from pylibchorus.chorus_api import get
from pylibchorus.chorus_api import post
from pylibchorus.chorus_api import put
from pylibchorus.chorus_api import delete

LOG = logging.getLogger(__name__)

#pylint: disable=R0903
class ChorusSession(object):
    '''Chorus User Session Object'''

    def __init__(self, config):
        self.config = config
        self.sid = ''
        self.cookies = {}

    def __enter__(self):
        '''create session and return sid and cookies'''

        LOG.debug("Opening Chorus Session")
        data = {
            'username': self.config.get('alpine', 'username'),
            'password': self.config.get('alpine', 'password'),
        }
        code, json = post('/sessions', self, data)

        if code != 201:
            raise RuntimeError("Chorus Session Login Failed")

        self.sid = json['response']['session_id']
        return self

    def __exit__(self, _type, _value, _traceback):
        '''Close chorus session'''
        LOG.debug("Closing Chorus Session")
        delete('/sessions', self)
