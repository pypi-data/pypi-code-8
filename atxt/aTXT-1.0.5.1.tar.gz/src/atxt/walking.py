#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

import os

from encoding import encoding_path
from log_conf import Logger
from utils import extract_ext


log = Logger.log

# from kitchen.text.converters import getwriter

# UTF8Writer = getwriter('utf8')
# sys.stdout = UTF8Writer(sys.stdout)

__all__ = ['walk', 'size_str', 'walk_size']


def _isdir(path_):
    path_ = path_.rstrip(os.path.sep)
    return os.path.isdir(path_)


def walk(top, topdown=True, tfiles=None, sdirs=None, level=0):
    """
    :param top: node root of the depth-first search on tree directory
    :param topdown: if yield results, to modify in any iteration
    :param tfiles: list of types of files allowed to show, p.e .pdf, .docx, .txt
    :param sdirs: don't search in these directory ( a full path system adress)
    :param level: max level of depth reached for search walklevel
    :return: a generator with values, top, root-path and dirs, nondirs
                    ( class from scandir library )
    """

    top = encoding_path(top)

    assert isinstance(level, int)
    tfiles = tfiles or ['*']
    assert isinstance(tfiles, list)

    sdirs = sdirs or []
    sdirs = [d for d in sdirs if _isdir(d)]
    try:
        import scandir
    except ImportError, e:
        log.critical('scandir library is missing, please install it:%s' % e)

    dirs = []
    nondirs = []
    symlinks = set()

    if os.access(top, os.R_OK):
        for entry in scandir.scandir(top):
            try:
                fpath = os.path.join(top, entry.name)
                if entry.name.startswith('.') or not os.access(fpath, os.R_OK):
                    continue
                if entry.is_dir() and not fpath in sdirs:
                    dirs.append(entry)
                elif "*" in tfiles:
                    nondirs.append(entry)
                else:
                    ext = extract_ext(entry.name)
                    if ext in tfiles:
                        nondirs.append(entry)

            except OSError, e:
                nondirs.append(entry)
                log.error(e)
            try:
                if entry.is_symlink():
                    symlinks.add(entry)
            except OSError:
                pass

    flinks = False

    yield top, dirs, nondirs

    if level > 0:
        for entry in dirs:
            if flinks or entry.name not in symlinks:
                npath = os.path.join(top, entry.name)
                if not os.access(npath, os.R_OK):
                    continue
                for x in walk(npath, topdown, tfiles, sdirs, level - 1):
                    yield x


def size_str(bs, precision=1):
    """
    http://code.activestate.com/recipes/577081-humanized-
    representation-of-a-number-of-bytes/
    """
    bs = long(bs)
    abbrevs = (
        (1 << 50L, 'PB'),
        (1 << 40L, 'TB'),
        (1 << 30L, 'GB'),
        (1 << 20L, 'MB'),
        (1 << 10L, 'kB'),
        (1, 'bytes')
    )
    if bs == 1:
        return '1 byte'
    factor, suffix = abbrevs[0]
    for factor, suffix in abbrevs:
        if bs >= factor:
            break
    return '%.*f %s' % (precision, bs / factor, suffix)


def walk_size(top='', tfiles=None, sdirs=None, level=0):
    count_files = 0
    total_size = 0
    try:
        for root, _, files in walk(top, sdirs=sdirs, level=level, tfiles=tfiles):
            for f in files:
                if os.access(f, os.R_OK):
                    filepath = os.path.join(root, f.name)
                    total_size += os.path.getsize(filepath)
                    count_files += 1
    except Exception, e:
        log.error(e)
    return [count_files, total_size]
