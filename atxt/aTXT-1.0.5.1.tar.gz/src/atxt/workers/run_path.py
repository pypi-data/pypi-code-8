#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-26 20:07:48
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-30 11:07:29
from __future__ import print_function
import os

from atxt.log_conf import Logger
log = Logger.log


from atxt.formats import supported_formats
import atxt.walking as wk
from atxt.utils import make_dir
from atxt.lib import aTXT
from atxt.encoding import encoding_path

__all__ = ['run_paths', 'run_one_path']


def run_paths(manager, thread=None):
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
        opts['tfiles'] = set(supported_formats[:]) & set(opts['tfiles'])
        opts['tfiles'] = list(opts['tfiles'])

    manager.options = opts
    log.debug(manager.options)
    total, finished = 0, 0
    if thread:
        thread._cursor_end.emit(True)
    for path in opts['<path>']:
        res = run_one_path(manager, path, thread)
        if thread:
            thread._cursor_end.emit(True)
        if res:
            total += res[0]
            finished += res[1]
        else:
            log.warning('errors with path: %s' % path)
    return total, finished


def run_one_path(manager, path=None, thread=None):
    assert isinstance(manager, aTXT)
    opts = manager.options
    if not path:
        if opts['--path']:  # the path will be always stored on <path>
            return run_paths(manager)
        else:
            log.critical('--path is not on')
            return
    log.debug('working over: %s' % path)
    assert isinstance(path, str) or isinstance(path, unicode)
    if not os.path.isdir(path):
        log.error('%s is not a valid path for --path option' % path)
        return
    # the part below can be omitted for a second time (tfiles->opts)
    if 'tfiles' not in opts:
        log.critical('there is not tfiles key. Grave.')
        tfiles = set(supported_formats[:])
        if '<format>' in opts and opts['<format>']:
            tfiles = set()
            for f in opts['<format>']:
                f = f[1:] if f.startswith('.') else f
                f = f.lower()
                if f in supported_formats:
                    tfiles.add(f)
        opts['tfiles'] = list(tfiles)
    log.debug('searching for: %s' % opts['tfiles'])
    # manager.word()
    total = 0
    finished = 0
    for _root, _, _files in wk.walk(path,
                                    level=opts['--depth'],
                                    tfiles=opts['tfiles']):
        if not _files:
            continue
        log.debug('path=%s' % _root)
        for f in _files:
            total += 1
            log.debug('-' * 50)
            log.debug('file: %s' % f.name)
            file_path = os.path.join(_root, f.name)
            new_path = None
            try:
                new_path = manager.convert_to_txt(filepath=file_path)
                if not new_path:
                    log.error('unsucessful conversion: %s' % file_path)
                    if thread:
                        thread._cursor_end.emit(True)
            except Exception, e:
                log.critical(e)
                continue

            log.info('successful conversion: %s' % file_path)
            finished += 1
            if thread:
                thread._cursor_end.emit(True)

    return total, finished
