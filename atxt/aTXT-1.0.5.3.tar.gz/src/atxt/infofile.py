#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto

import os
import tempfile as tmp

from encoding import encoding_path
from log_conf import Logger
import utils


log = Logger.log


class InfoFile(object):

    """
        .path
        .basename
        .name
        .extension
        .dirname

    """

    def __init__(self, file_path, check=False):
        if not file_path:
            raise IOError('file_path: %s' % file_path)

        log.debug('extracting metadata from file: %s' % file_path)
        self.path = os.path.abspath(encoding_path(file_path))
        if check:
            if not os.path.isfile(self.path):
                raise IOError('It is not a file or does not exist')
            if not os.access(self.path, os.R_OK):
                raise OSError('The file is not readable or missing')

        try:
            self.basename = os.path.basename(self.path)
            name = os.path.splitext(self.basename)[0]
            self.extension = utils.extract_ext(self.basename)
            self.name = name
            self.dirname = os.path.dirname(self.path)
        except Exception, e:
            log.error(e)

    def remove(self):
        utils.remove(self.path)
        # TODO remove entire object

    def size(self):
        return utils.size(self.path)

    def move(self, to_path=None):
        utils.move_to(self.path, to_path)

    def __repr__(self):
        return encoding_path(self.path)

    @property
    def temp(self):
        try:
            return self.temp_path
        except Exception, e:
            log.debug(e)
            return self.create_temp()

    def create_temp(self, value=None):
        self.temp_dir = value
        if not value or not os.path.exists(self.temp_dir):
            try:
                self.temp_dir = tmp.mkdtemp()
                log.debug('tempdir: %s' % self.temp_dir)
            except Exception, e:
                log.error(e)
                return
        utils.copy_to(self.path, self.temp_dir)

        self.temp_basename = self.basename
        self.temp_path = os.path.join(self.temp_dir, self.temp_basename)

        log.debug('temp path: %s' % self.temp_path)
        return self.temp_path

    def remove_temp(self):
        try:
            utils.remove_dir(self.temp_dir)
            del self.temp_basename
            del self.temp_path
            del self.temp_dir
        except AttributeError:
            log.warning('%s file has not temporal version' % self.basename)

    def __str__(self):
        return self.name + ('.' + self.extension) if self.extension else ''
