#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging

import utils

_log = logging.getLogger(__name__)


def main():
    utils.setup_logging()
    _log.info('Testing logging...')

if __name__ == '__main__':
    main()
