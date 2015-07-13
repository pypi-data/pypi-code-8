#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
from atxt.check import check_os
from kitchen.text.converters import to_unicode
from log_conf import Logger

log = Logger.log

def encoding_path(s):
    s = s.strip()
    if check_os() == 'Windows':
        return to_unicode(s, 'utf-8')
    s = to_unicode(s)
    try:
        return s.encode('utf-8', 'replace')
    except Exception, e:
        log.warning(e)
    return s
