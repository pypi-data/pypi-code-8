#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-26 20:07:21
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-06 14:57:17
from __future__ import print_function

from collections import defaultdict
import os

from atxt.formats import supported_formats
from atxt.lib import aTXT
from atxt.log_conf import Logger
from atxt.utils import extract_ext
from atxt.encoding import encoding_path


log = Logger.log


__all__ = ['run_files', 'run_one_file']


def run_files(manager, total=0, finished=0):
    assert isinstance(manager, aTXT)
    opts = manager.options
    log.debug('with option --file')
    # collect the extension of files
    tfiles = set()
    files = defaultdict(list)
    for file_path in set(opts['<file>']):
        if not os.path.isabs(file_path) and '--from' in opts:
            file_path = os.path.join(opts['--from'], file_path)
        if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
            log.info('file is missing or it is not readable')
            continue
        ext = extract_ext(file_path)
        if ext in supported_formats():
            tfiles.add(ext)
            files[ext].append(file_path)
        else:
            log.warning('%s ignored (%s is not supported yet)' %
                        (file_path, ext))

    to_path = opts['--to']  # where you want to save txt files
    if to_path:
        if not os.path.isdir(opts['--to']):
            log.error('%s is not a valid path for --to option' %
                      opts['--to'])
            return
    for ext in supported_formats():
        for file_path in files[ext]:
            total += 1
            new_path = None
            try:
                new_path = manager.convert_to_txt(filepath=file_path)
            except Exception, e:
                log.critical('convert_to_txt: %s' % e)
            file_path = encoding_path(file_path)
            if new_path:
                log.info("{c:2d} | [OK] | {p}".format(c=total, p=file_path))
                finished += 1
            else:
                log.info("{c:2d} | [FAIL] | {p}".format(c=total, p=file_path))
    return total, finished


def run_one_file(manager, filepath=None, cache=False):
    assert isinstance(manager, aTXT)
    opts = manager.options
    assert '<file>' in opts
    assert '--file' in opts
    if filepath:
        if cache:
            opts['<file>'].append(filepath)
        else:
            opts['<file>'] = [filepath]
    opts['--file'] = True
    manager.options = opts
    return run_files(manager)
