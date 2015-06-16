# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Module doc string."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import csv
import sys
import re
import os
import uuid

# 3rd Party
from bashutils import bashutils

# -----------------------------------------------------------------------------


class AdKitBase(object):

    """Class doc string."""

    @staticmethod
    def get_data(path):
        """
        Helper to return correct path to our non-python package data files.
        """
        root = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(root, 'templates', path)

    @staticmethod
    def get_list_from_csv(csv_file):
        """
        Open and read a CSV into a list using the column headers as key names.
        """
        try:
            fileref = open(csv_file, 'rU')
            csv_f = list(csv.DictReader(fileref))
            fileref.close()
            return csv_f
        except BaseException as err:
            sys.exit(err)

    @staticmethod
    def get_size_from_filename(filepath):
        """
        Return string such as 300x250
        """
        # get filename
        basename = os.path.basename(filepath)

        pattern = re.compile(r'(\d{1,4}x\d{1,4})')
        match = pattern.search(basename)
        if match:
            return match.group()

        raise Exception('Unable to get size from filename: {0}'.format(basename))

    @staticmethod
    def zip_files(dirpath):
        """
        Zip a directory.
        """
        os.chdir(dirpath)
        filepath = '{0}{1}.zip'.format(dirpath, uuid.uuid4())

        # quote path in case of spaces
        cmd = 'zip -r "{0}" .'.format(filepath)
        return bashutils.exec_cmd(cmd)
