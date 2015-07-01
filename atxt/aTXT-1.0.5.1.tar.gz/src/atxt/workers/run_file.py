#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-26 20:07:21
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-30 11:07:19
from __future__ import print_function

from collections import defaultdict
import os

from atxt.formats import supported_formats
from atxt.lib import aTXT
from atxt.log_conf import Logger
from atxt.utils import extract_ext


log = Logger.log


__all__ = ['run_files', 'run_one_file']


def run_files(manager, thread=None):
    assert isinstance(manager, aTXT)
    opts = manager.options
    log.debug('with option --file')
    # collect the extension of files
    tfiles = set()
    files = defaultdict(list)
    for file_path in set(opts['<file>']):
        log.debug('-> %s' % file_path)
        if not os.path.isabs(file_path) and '--from' in opts:
            file_path = os.path.join(opts['--from'], file_path)
        if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
            log.info('file is missing or it is not readable')
            # if file_path correspond to a folder path,(user omitted --path flag)
            # it should be process with run_paths(manager) --path=True
            # and before that: manager.opts.update({'<path>': [file_path]})
            continue
        ext = extract_ext(file_path)
        if ext in supported_formats:
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
    total = sum(len(v) for _, v in files.items())
    #  manager.word()
    successful_files = defaultdict(str)
    for ext in supported_formats:
        for file_path in files[ext]:
            new_path = None
            try:
                new_path = manager.convert_to_txt(filepath=file_path)
            except Exception, e:
                log.critical('convert_to_txt: %s' % e)
            if new_path:
                successful_files[file_path] = new_path
                log.info('successful conversion for: %s' % file_path)
            else:
                log.error('unsucessful conversion: %s' % file_path)
            if thread:
                thread._cursor_end.emit(True)
    finished = len(successful_files)
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
