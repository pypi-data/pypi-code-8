#!/usr/bin/env python
# -*- coding: utf-8 -*-
from atxt.log_conf import Logger
from jpg import imagen


__all__ = ['png']
log = Logger.log


def png(from_file, to_txt, opts):
    try:
        return imagen(from_file, to_txt, opts)
    except Exception, e:
        log.critical(e)
