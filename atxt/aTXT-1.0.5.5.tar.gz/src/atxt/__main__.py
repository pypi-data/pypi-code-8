#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

from __future__ import print_function

import logging
import os
import sys

from check import check
from colorama import init as initColorama
from docopt import docopt
from formats import supported_formats
from funcy import map as fmap
from funcy import compose
from lib import aTXT
from log_conf import Logger
from use import __doc__ as usage
from workers import run_files, run_paths


initColorama()

log = Logger.log

__version__ = "1.0.5"


def main():
    opts = docopt(usage, version=__version__)
    opts = set_tfiles(opts)

    if opts['-v']:
        print(__version__)
        return

    if opts['-h']:
        print(usage)
        return

    opts['-i'] = opts.get('-i', True)
    if opts['--log']:
        try:
            opts = set_log(opts)
        except Exception, e:
            log.error('LOGPATH error, it is not a valid path:%s' % e)
            print(usage)
            return

    if opts['--check']:
        check()
        return

    if opts['-i']:
        log.info('Starting the graphical interface...')
        try:
            import gui
            gui.run()
            return
        except Exception, e:
            log.critical(e)
            return

    manager = aTXT()
    manager.options = opts

    res = None
    total, finished = 0, 0
    if manager.options['--file']:
        res = run_files(manager)
        if res and len(res) == 2:
            total += res[0]
            finished += res[1]
    # log.critical(manager.options['<path>'])
    if manager.options['--path']:
        res = run_paths(manager)
        if res and len(res) == 2:
            total += res[0]
            finished += res[1]

    log.info('{0} end of aTXT {0}'.format('-' * 15))
    log.info('files: %d\tfinished: %d', total, finished)

    if total == 0:
        log.warning('No files to proceed or something was wrong.')
        return
    return


def set_tfiles(opts):
    if not opts['--format']:
        opts['tfiles'] = opts.get('tfiles', supported_formats())
        return opts
    opts['tfiles'] = opts.get('tfiles', [])
    sformat = opts.get('--format', '')
    lformat = []
    if ',' in sformat:
        lformat = sformat.rsplit(',')
    elif ' ' in sformat:
        lformat = sformat.split()
    else:
        lformat = [sformat]
    lformat = fmap(str.strip, lformat)

    for ext in supported_formats():
        if ext in lformat:
            opts['tfiles'].append(ext)
    opts['tfiles'] = compose(list, set)(opts['tfiles'])
    return opts


def set_log(opts):
    log_path = os.path.abspath(opts['--log'])

    if not os.path.isfile(log_path):
        log_path = os.path.join(log_path, 'log.txt')

    log.info('log will be save in: %s' % log_path)
    opts['log_path'] = log_path
    f = open(log_path, 'wb')
    f.close()
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(levelname)-1s| %(message)s::%(filename)s:%(lineno)s")
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return opts


if __name__ == "__main__":
    main()
    sys.exit()
