#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from _utils import raw_data, save_raw_data
from atxt.vendors import tesseract
from atxt.log_conf import Logger
from atxt.utils import remove


log = Logger.log

__all__ = ['jpg', 'imagen']


def jpg(from_file, to_txt, opts):
    return imagen(from_file, to_txt, opts)


def imagen(from_file, to_txt, opts):
    outputpath = os.path.join(from_file.dirname, 'output.txt')
    log.info('tesseract is processing: {}'.format(from_file.path))
    tesseract(from_file.path, None, opts)
    text = ''
    try:
        text = raw_data(outputpath)
    except Exception, e:
        log.critical(e)
    remove(outputpath)
    return save_raw_data(to_txt.path, text)
