#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from atxt.log_conf import Logger
log = Logger.log

import subprocess as sub

from atxt.check import path_pdftotext as bpdftotext
from atxt.check import path_pdftopng as bpdftopng
from atxt.check import path_pdffonts as bpdffonts
from atxt.check import path_tesseract as btesseract
from atxt.check import path_antiword as bantiword

from funcy import map


def pdftotext(filepath, txtpath):
    if not bpdftotext():
        raise ImportError('pdftotex is missing. --check command')
    f = file(txtpath, 'wb')
    cmd = [bpdftotext(), filepath, '-']
    try:
        output = sub.call(cmd, stdout=f)
    except Exception, e:
        log.critical(e)
    f.close()
    if output == 0:
        log.debug('Everything ok.')
        return txtpath
    elif output == 1:
        raise IOError('Error opening a PDF file: %s.' % filepath)
    elif output == 2:
        raise IOError('Error opening the output file.: %s.' % txtpath)
    elif output == 3:
        raise IOError('Error related to PDF permissions.')
    else:
        raise IOError('Unkwown Error.')


def pdffonts(filepath):
    if not bpdffonts():
        raise ImportError('pdftotex is missing. --check command')
    cmd = [bpdffonts(), filepath]
    return sub.check_output(cmd)


def need_ocr(filepath):
    output = pdffonts(filepath)
    log.info(output)
    assert isinstance(output, unicode) or isinstance(output, str)
    if output.count('yes') or output.count('Type') or output.count('no'):
        log.info('ORC is not necessary with: %s' % filepath)
        return False
    return True


def pdftopng(filepath, to_path=None):
    if not bpdftopng():
        raise ImportError('pdftopng is missing. --check command')
    if not to_path:
        to_path = os.path.dirname(filepath)
    cmd = [bpdftopng(), filepath, to_path]
    sub.call(cmd)


def tesseract(filepath, txtpath=None, opts=None):
    if not btesseract():
        raise ImportError('tesseract is missing. --check command')
    if not txtpath:
        txtpath = os.path.join(os.path.dirname(filepath), 'output')
    if not opts:
        opts = {'-l': 'spa'}
    cmd = [btesseract(), filepath, txtpath, '-l', opts.get('-l', 'spa')]
    cmd = map(str, cmd)
    try:
        sub.call(cmd)
    except Exception, e:
        log.critical(e)


def antiword(filepath, txtpath):
    if not bantiword():
        raise ImportError('antiword is missing')
    cmd = [bantiword(), filepath]
    f = file(txtpath, 'wb')
    try:
        sub.call(cmd, stdout=f)
    except Exception, e:
        log.critical(e)
        f.close()
        return
    f.close()
    return txtpath
