#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from atxt.log_conf import Logger
from atxt.vendors import antiword
from atxt.check import check_os, check_office

from _utils import raw_data

log = Logger.log


def doc(from_file, to_txt, opts):
    try:
        res = antiword(from_file.path, to_txt.path)
        if not os.path.exists(to_txt.path):
            raise OSError('file does not exist.')
        return res
    except Exception, e:
        log.critical(e)
        if check_os == 'Windows' and check_office():
            return doc_win(from_file, to_txt)


def doc_win(from_file, to_txt):
    log.info('doc will be treat with microsoft office')
    from win32com import client
    msword = client.DispatchEx('Word.Application')
    msword.Visible = False
    try:
        # http://msdn.microsoft.com/en-us/library/bb216319%28office.12%29.aspx
        wb = msword.Documents.OpenNoRepairDialog(
            FileName=from_file.path,
            ConfirmConversions=False,
            ReadOnly=True,
            AddToRecentFiles=False,
            Revert=True,
            Visible=False,
            OpenAndRepair=True,
            NoEncodingDialog=True
        )
    except Exception, e:
        log.critical('msword failed:', e)
        return
    try:
        wb.SaveAs(to_txt.path, FileFormat=2)
        wb.Close()
        msword.Quit()
    except Exception, e:
        log.critical('msword failed to save file: ', e)
        return
    return to_txt.path
