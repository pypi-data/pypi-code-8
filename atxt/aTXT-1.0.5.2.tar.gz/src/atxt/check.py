#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
from __future__ import print_function

import os

from distutils.spawn import find_executable
from log_conf import Logger
from osinfo import osinfo

import subprocess as sub

log = Logger.log

vendors = os.path.dirname(os.path.abspath(__file__))
vendors = os.path.join(vendors, 'vendors')


def check_os():
    info = osinfo.OSInfo()
    return info.system


def check_office():
    system = check_os()
    if system != 'Windows':
        return False
    try:
        from win32com import client
        msword = client.DispatchEx('Word.Application')
        msword.Visible = False
        msword.Quit()
        log.debug('Successful Dispatching of Word.Application')
    except Exception, e:
        log.warning(e)
    return False


def path_program(name, path=None):
    system = check_os()
    if not path:
        path = vendors
        if system == 'Windows':
            name = name + '.exe' if not name.endswith('.exe') else name
            path = os.path.join(vendors, system)
        else:
            path = os.path.join(vendors, 'Unix')
    p = find_executable(name)
    return p if p else find_executable(name, path=path)


def path_pdftotext():
    return path_program('pdftotext')


def path_pdftopng():
    return path_program('pdftopng')


def path_pdffonts():
    return path_program('pdffonts')


def path_tesseract():
    return path_program('tesseract')


def path_antiword():
    set_antiword()
    if check_os() != 'Windows':
        return path_program('antiword')
    path = os.path.join('C:\\', 'antiword\\')
    if os.path.exists(path) and find_executable('antiword.exe', path=path):
        return find_executable('antiword.exe', path=path)
    path = os.path.join(vendors, 'Windows', 'antiword')
    return find_executable('antiword.exe', path=path)


def set_antiword():
    if check_os() == 'Windows':
        p = os.path.join('C:\\', 'antiword\\')
        path_anti = p
        if 'PATH' in os.environ.keys():
            if os.environ['PATH'].find('antiword') < 0:
                cmd = ['setx', 'PATH', '{path}{anti}'.format(
                    path=os.environ['PATH'], anti=path_anti)]
                try:
                    sub.call(cmd)
                    log.info('antiword was added to PATH variable')
                except Exception, e:
                    log.warning(e)

        if 'HOME' not in os.environ.keys():
            home = os.path.expanduser('~')

            cmd = ['setx', 'HOME', home]
            try:
                sub.call(cmd)
                log.info('HOME was added as new environ variable')
            except Exception, e:
                log.warning(e)


def check():
    p = path_pdftotext()
    if p:
        log.debug('successful pdftotext: %s' % p)
    else:
        log.warning(
            'pdftotext is missing. It could not be able to treat some pdf files.')

    p = path_pdftopng()
    if p:
        log.debug('successful pdftopng: %s' % p)
    else:
        log.warning(
            'pdftopng is missing. (ORC will not be available for pdf files.)')

    p = path_pdffonts()
    if p:
        log.debug('successful pdffonts: %s' % p)
    else:
        log.warning(
            'pdffonts is missing. (ORC will not be available)')
    p = path_tesseract()
    if p:
        log.debug('successful ocr: %s' % p)
    else:
        log.warning(
            'tesseract is missing. OCR recognition will no be available.')

    p = path_antiword()
    if p:
        log.debug('successful antiword: %s' % p)
    else:
        log.warning('antiword is missing. .DOC will not be available.')

    if not check_office() and check_os == 'Windows':
        log.warning(
            'PyWin32 or Microsoft Office Suite is not installed or not available.')
