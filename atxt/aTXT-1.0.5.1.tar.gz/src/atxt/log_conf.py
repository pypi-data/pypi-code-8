#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

import logging


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()


@singleton
class Logger(object):

    def __init__(self, level=logging.INFO):
        LOG_LEVEL = level
        logging.root.setLevel(LOG_LEVEL)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)

        LOGFORMAT = "%(levelname)-1s | %(message)s ::%(filename)s:%(lineno)s"
        try:
            LOGFORMAT = "%(log_color)s%(levelname)-1s%(reset)s | %(log_color)s%(message)s%(reset)s ::%(filename)s:%(lineno)s"
            from colorlog import ColoredFormatter
            formatter = ColoredFormatter(LOGFORMAT)
            stream.setFormatter(formatter)
        except Exception:
            formatter = logging.Formatter(LOGFORMAT)
        self.log = logging.getLogger('root')
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)
