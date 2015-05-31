#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import logging
import ConfigParser

import utils

_log = logging.getLogger(__name__)


class VoiceCom(object):
    def __init__(self):
        utils.setup_logging()
        _log.info('Initializing system.')

        plugin_path = utils.expand_dir('plugins')
        if not utils.os.path.isdir(plugin_path):
            utils.os.mkdir(plugin_path)

        self.cfg_path = utils.expand_dir('voicecom.conf')
        self.cfg = ConfigParser.SafeConfigParser()
        self.cfg.read(self.cfg_path)

        with open(self.cfg_path, 'w') as f:
            self.cfg.write(f)

    def run(self):
        _log.info('All good.')


def main():
    try:
        VoiceCom().run()
    except:
        _log.critical('System failure.', exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
