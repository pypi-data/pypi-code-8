#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

import os
import shutil as sh

from encoding import encoding_path
from funcy import map, compose, filter
from log_conf import Logger


log = Logger.log


__all__ = ['make_dir', 'remove_dir', 'remove', 'move_to', 'copy_to',
           'size', 'extract_ext', 'union', 'readable', 'standardpath', 'parser_opts']


def make_dir(path):
    path = encoding_path(path)
    if not os.path.exists(path):
        if not os.access(path, os.W_OK):
            log.error('directory without permissions for write: %s' % path)
        try:
            log.debug('creating directory: %s' % path)
            os.makedirs(path)
        except OSError:
            pass


def remove_dir(path):
    if os.path.isdir(path) and os.path.exists(path):
        try:
            log.debug('removing entire folder: %s' % path)
            sh.rmtree(path)
            log.debug('directory removed: %s' % path)
        except IOError, e:
            if os.path.exists(path):
                log.warning('fail to remove directory: %s' % e)
            else:
                log.error(e)


def remove(filepath):
    filepath = encoding_path(filepath)
    if os.path.exists(filepath):
        if os.path.isfile(filepath):
            log.debug('removing file %s' % filepath)
            try:
                os.remove(filepath)
            except IOError, e:
                log.warning(e)
                raise e
        else:
            log.warning('remove file, %s is not a file' % filepath)


def move_to(filepath, to_path):
    filepath = encoding_path(filepath)
    to_path = encoding_path(to_path)
    if os.path.isfile(filepath):
        try:
            log.debug('moving from %s to %s' % (filepath, to_path))
            if not os.path.exists(to_path):
                make_dir(to_path)
            sh.copy2(filepath, to_path)
        except Exception, e:
            log.warning(e)
            raise e


def copy_to(filepath, to_path):
    filepath = encoding_path(filepath)
    to_path = encoding_path(to_path)
    try:
        log.debug('copying %s to %s' % (filepath, to_path))
        sh.copy2(filepath, to_path)
    except IOError, e:
        log.error(e)
        raise e


def size(filepath):
    filepath = encoding_path(filepath)
    if os.access(filepath, os.R_OK) and os.path.isfile(filepath):
        try:
            size = os.path.getsize(filepath)
            return size
        except Exception, e:
            log.warning(e)


def extract_ext(filepath):
    filepath = encoding_path(filepath)
    ext = os.path.splitext(filepath)[1].lower()
    return ext[1:] if ext.startswith('.') else ext


def union(A):
    assert isinstance(A, list)
    return list(set(A))


def readable(path):
    return os.path.exists(path) and os.access(path, os.R_OK)


def standardpath(path):
    return compose(os.path.abspath, encoding_path)(path)


def parser_opts(opts):
    assert isinstance(opts, dict)
    opts['--from'] = encoding_path(opts.get('--from', ''))
    if os.path.isdir(opts['--from']):
        opts['--from'] = os.path.abspath(opts['--from'])

    opts['<source>'] = union(opts.get('<source>', []))
    opts['<file>'] = union(opts.get('<file>', []))
    opts['<path>'] = union(opts.get('<path>', []))

    assert isinstance(opts['<source>'], list)
    assert isinstance(opts['<file>'], list)
    assert isinstance(opts['<file>'], list)

    opts['<source>'] = map(standardpath, opts['<source>'])
    opts['<path>'] = map(standardpath, opts['<path>'])
    opts['<file>'] = map(standardpath, opts['<file>'])

    for path in opts['<source>']:
        if os.path.isdir(path):
            opts['<path>'].append(path)
        elif os.path.isfile(path):
            opts['<file>'].append(path)
        else:
            if os.path.isdir(opts['--from']):
                path = os.path.join(opts['--from'], path)
                if os.path.isfile(path):
                    opts['<file>'].append(path)

    opts['<file>'] = filter(readable, opts['<file>'])
    opts['<path>'] = filter(readable, opts['<path>'])
    opts['--file'] = (len(opts['<file>']) > 0)
    opts['--path'] = (len(opts['<path>']) > 0)

    opts['--depth'] = int(opts['--depth'])
    return opts.copy()
