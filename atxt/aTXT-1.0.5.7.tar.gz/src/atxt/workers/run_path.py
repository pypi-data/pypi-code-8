#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-26 20:07:48
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-06 14:57:51
from __future__ import print_function
import os

from atxt.log_conf import Logger
log = Logger.log


from atxt.formats import supported_formats
from atxt.walking import walk
from atxt.utils import make_dir, extract_ext
from atxt.lib import aTXT
from atxt.encoding import encoding_path

__all__ = ['run_paths', 'run_one_path']


def run_paths(manager, total_=0, finished_=0):
    assert isinstance(manager, aTXT)
    opts = manager.options
    if not opts['--path'] or not opts['<path>']:
        log.debug('nothing for path')
        return
    log.debug('<path>: %s' % opts['<path>'])
    if opts['--depth'] < 0:
        opts['--depth'] = 0
    log.debug('--depth: %s' % opts['--depth'])
    opts['--to'] = opts['--to'] or opts['--from']
    opts['--to'] = encoding_path(opts['--to'])
    if opts['--to'] == 'TXT':
        opts['--to'] = os.path.join(opts['--from'], opts['--to'])
        make_dir(opts['--to'])

    if 'tfiles' in opts and opts['tfiles']:
        opts['tfiles'] = set(supported_formats()) & set(opts['tfiles'])
        opts['tfiles'] = list(opts['tfiles'])

    manager.options = opts
    log.debug(manager.options)
    total, finished = total_, finished_
    for path in opts['<path>']:
        res = run_one_path(manager, path, total)
        if res:
            total += res[0]
            finished += res[1]
        else:
            log.warning('errors with path: %s' % path)
    return total, finished


def set_formats(opts):
    if 'tfiles' in opts:
        return opts
    log.critical('there is not tfiles key. Grave.')
    tfiles = set(supported_formats())
    if '<format>' in opts and opts['<format>']:
        tfiles = set()
        for f in opts['<format>']:
            f = f[1:] if f.startswith('.') else f
            f = f.lower()
            if f in supported_formats():
                tfiles.add(f)
    opts['tfiles'] = list(tfiles)

def run_one_path(manager, path=None, total_=0):
    assert isinstance(manager, aTXT)
    opts = manager.options
    if not path:
        # the path will be always stored on <path>
        if opts.get('--path', None):
            return run_paths(manager)
        log.critical('--path is not on')
        return

    log.debug('working over: %s' % path)
    assert isinstance(path, str) or isinstance(path, unicode)
    if not os.path.isdir(path):
        log.error('%s is not a valid path for --path option' % path)
        return
    opts = set_formats(opts)
    log.debug('searching for: %s' % opts['tfiles'])
    total, finished = 0,0
    # from random import randint
    # a = randint(1, 100)
    for r, _, files in walk(path, level=opts['--depth']):
        if not files:
            continue
        log.debug('path=%s' % r)
        # log.critical(a)
        for f in files:
            if extract_ext(f.name) not in opts['tfiles']:
                continue
            total += 1
            log.debug('-' * 50)
            new_path = None
            new_path = manager.convert_to_txt(filepath=f.path)
            if new_path:
                try:
                    log.info("{c:3d} | [OK] | {p}".format(c=total_+total, p=f.path))
                except Exception:
                    log.info("{c:3d} | [OK] ".format(c=total_+total))
                    log.info(f.path)
                finished += 1
            else:
                try:
                    log.info("{c:3d} | [FAIL] | {p}".format(c=total_+total, p=f.path))
                except Exception:
                    log.info("{c:3d} | [FAIL] ".format(c=total_+total))
                    log.info(f.path)

    return total, finished
