#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 13:09:59
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-30 12:50:38
import os
import chardet
import codecs

from atxt.log_conf import Logger
log = Logger.log

__all__ = ['raw_data', 'find_encoding', 'save_raw_data']


def raw_data(filepath, encoding=None):
    if filepath and os.path.exists(filepath):
        if not os.access(filepath, os.R_OK):
            log.warning('file has not read permission')
            return
        rawdata = None
        if not encoding:
            encoding = find_encoding(filepath)
        try:
            log.debug('trying to read file with encoding: %s' % encoding)
            f = codecs.open(filepath, 'r', encoding=encoding)
            rawdata = f.read()
            f.close()
        except Exception, e:
            log.critical(e)
            try:
                log.debug('trying to read without encoding:%s' % e)
                f = codecs.open(filepath, mode='r')
                rawdata = f.read()
                f.close()
            except Exception, ee:
                log.critical('(second try)')
                log.critical(ee)
        return rawdata


def find_encoding(filepath):
    if filepath:
        rawdata = codecs.open(filepath, mode="r").read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        log.debug('looking for the correct encoding: %s' % encoding)
        return encoding


def save_raw_data(filepath, text, encoding='utf-8'):
    log.debug('saving text data')
    if filepath:
        try:
            f = codecs.open(filepath, mode='w', encoding=encoding)
            if isinstance(text, list):
                for line in text:
                    line = line.replace('\n', os.linesep)
                    f.write(line + os.linesep)
            else:
                f.write(text)
            f.close()
            return filepath
        except Exception, e:
            log.critical(e)
            try:
                if encoding:
                    f = codecs.open(filepath, mode='w')
                    f.write(text)
                    f.close()
                else:
                    f = open(filepath, 'w')
                    f.write(text)
                return filepath
            except Exception, ee:
                log.critical(ee)
