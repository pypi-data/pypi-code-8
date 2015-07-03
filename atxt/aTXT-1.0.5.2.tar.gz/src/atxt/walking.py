#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

import os
import re

from encoding import encoding_path
from log_conf import Logger
from scandir import islink
from scandir import scandir

from os.path import islink
from utils import extract_ext

log = Logger.log

__all__ = ['walk', 'size_str', 'walk_size']

def walk(top, level=None, regex=None):
    """A modification of scandir.walk for perform
    a topdown search with level of depth and regex precompiled
    """
    dirs = []
    nondirs = []

    if isinstance(regex, str):
        regex = re.compile(regex)

    try:
        scandir_it = scandir(top)
    except Exception:
        return

    while True:
        try:
            try:
                entry = next(scandir_it)
            except StopIteration:
                break
        except Exception:
            return

        try:
            is_dir = entry.is_dir()
        except OSError:
            is_dir = False

        if is_dir:
            dirs.append(entry)
        else:
            if regex is not None and hasattr(regex, 'match'):
                if regex.match(entry.name):
                    nondirs.append(entry)
            else:
                nondirs.append(entry)

    yield top, dirs, nondirs
    if level is not None:
        assert isinstance(level, int)
        if not level > 0:
            return

    for d in dirs:
        name = d.name
        new_path = os.path.join(top, name)
        if islink(new_path):
            continue
        if isinstance(level, int):
            level -= 1
        for entry in walk(new_path, level, regex):
            yield entry


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


def walk_size(top='', level=None, regex=None):
    count_files = 0
    total_size = 0
    try:
        for root, _, files in walk(top, level=level, regex=regex):
            for f in files:
                # if os.access(f, os.R_OK):
                filepath = os.path.join(root, f.name)
                try:
                    total_size += os.path.getsize(filepath)
                    count_files += 1
                except Exception:
                    continue
    except Exception, e:
        log.error(e)
    return [count_files, total_size]
