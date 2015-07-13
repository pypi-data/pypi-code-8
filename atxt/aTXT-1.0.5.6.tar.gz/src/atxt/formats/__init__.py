#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 18:23:55
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-07 03:40:47

import os
import re

from atxt.infofile import InfoFile
from atxt.log_conf import Logger

from atxt.walking import walk

log = Logger.log

basedir_ = os.path.dirname(os.path.abspath(__file__))
__all__ = ['convert', 'supported_formats']


def supported_formats():
    formats = []
    regex = re.compile(r'[^(_|\.)+]\w+\.py$')
    for root, dirs, files in walk(basedir_, regex=regex):
        for f in files:
            extension = os.path.splitext(f.name)[0].lower()
            if extension.startswith('o'):
                formats.append(extension[1:])
            try:
                s = 'from {ext} import {ext}'.format(ext=extension)
                exec s
                if not extension.startswith('o'):
                    formats.append(extension)
            except Exception, e:
                log.warning('supported_formats(): %s' % e)
                log.warning('%s is not supported' % extension)
    return formats

for extension in supported_formats():
    try:
        if extension in ['csv', 'docx']:
            extension = 'o' + extension
        s = 'from {ext} import {ext}'.format(ext=extension)
        exec s
    except Exception, e:
        log.warning('%s is not supported' % extension)


def convert(from_file, to_txt, opts):
    if not isinstance(from_file, InfoFile):
        log.critical('the file should be instanced with InfoFile')
    bot = lambda x: x  # dummy def before a real definition based on format
    if from_file.extension in ['csv', 'docx']:
        exec 'bot = o{}'.format(from_file.extension)
    else:
        exec 'bot = %s' % from_file.extension

    log.debug('calling bot = %s' % bot.__name__)
    try:
        return bot(from_file, to_txt, opts)
    except Exception, e:
        log.critical('from formats/__init__.py:')
        log.critical(e)
