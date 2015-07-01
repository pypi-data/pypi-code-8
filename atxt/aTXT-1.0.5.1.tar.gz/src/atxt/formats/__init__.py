#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-15 18:23:55
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-30 11:02:07

import os
import re

from atxt.infofile import InfoFile
from atxt.log_conf import Logger


log = Logger.log

basedir_ = os.path.dirname(os.path.abspath(__file__))
__all__ = ['convert', 'supported_formats']

supported_formats = []

regex = re.compile(r'[^(_|\.)+]\w+\.py$')
for root, dirs, files in os.walk(basedir_):
    files.sort()
    for f in files:
        if regex.match(f):
            extension = os.path.splitext(f)[0].lower()
            if extension.startswith('o'):
                log.info('{} is supported'.format(extension[1:]))
                supported_formats.append(extension[1:])
            try:
                s = 'from {ext} import {ext}'.format(ext=extension)
                exec s
                if not extension.startswith('o'):
                    log.info('%s is supported' % extension)
                    supported_formats.append(extension)
            except Exception, e:
                log.warning(e)
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
    return bot(from_file, to_txt, opts)
