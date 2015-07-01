#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 01:52:42
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-30 12:48:55
import codecs
import os

from _utils import raw_data, save_raw_data
from atxt.log_conf import Logger
from atxt.utils import remove
from atxt.vendors import (
    pdftopng,
    pdftotext,
    tesseract,
    need_ocr
)
import atxt.walking as wk
from pdfminer import layout, pdfinterp, converter, pdfpage


log = Logger.log


def pdf_miner(from_file, to_txt):
    log.debug('trying with pdfminer')
    pdf = codecs.open(from_file.path, mode='rb')
    output = codecs.open(to_txt.path, mode='wb')
    try:
        resourceman = pdfinterp.PDFResourceManager()
        device = converter.TextConverter(
            resourceman, output, laparams=layout.LAParams())
        interpreter = pdfinterp.PDFPageInterpreter(resourceman, device)
        for page in pdfpage.PDFPage.get_pages(pdf):
            interpreter.process_page(page)
        output.close()
        device.close()
        pdf.close()
    except Exception, e:
        log.critical(e)
        return
    return to_txt.path


def pdf(from_file, to_txt, opts):
    opts['--ocr'] = opts.get('--ocr', False)
    ocr = need_ocr(from_file.path)
    if opts['--ocr']:
        log.info('Extraction with OCR technology')
        if not ocr:
            log.info('it could be more better if you do not use OCR')
        try:
            return pdf_ocr(from_file, to_txt, opts)
        except Exception, e:
            log.critical(e)
    log.info('Extraction with Xpdf technology')
    if ocr:
        log.warning('it would be better if you try to use OCR options')
    try:
        return pdftotext(from_file.path, to_txt.path)
    except Exception, e:
        log.critical(e)
    return pdf_miner(from_file, to_txt)


def pdf_ocr(from_file, to_txt, opts):
    pdftopng(from_file.path, to_txt.path)
    text = ''
    outputpath = os.path.join(to_txt.dirname, 'output.txt')
    for root, _, files in wk.walk(to_txt.dirname, tfiles=['png']):
        for f in files:
            if (f.name).startswith(to_txt.basename):
                filepath = os.path.join(root, f.name)
                log.info('tesseract is processing: {}'.format(filepath))
                tesseract(filepath, None, opts)
                try:
                    raw = raw_data(outputpath)
                    text = text + '\n' + raw
                except Exception, e:
                    log.critical(e)
                remove(os.path.join(root, f.name))
    remove(outputpath)
    return save_raw_data(to_txt.path, text)
