# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

# -----------------------------------------------------------------------------

# Standard
import csv
import sys
import re
import os

# -----------------------------------------------------------------------------


class AdKitBase(object):

    def get_data(self, path):
        """
        Helper to return correct path to our non-python package data files.
        """
        root = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(root, 'templates', path)

    def get_list_from_csv(self):
        """
        Open and read a CSV into a list using the column headers as key names.
        """
        try:
            f = open(self.input_file, 'rU')
            csv_f = list(csv.DictReader(f))
            f.close()
            return csv_f
        except BaseException, e:
            #log_error(e)
            sys.exit(e)

    def get_size_from_filename(self, filepath):
        """
        Return string such as 300x250
        """
        p = re.compile(r'(\d{1,4}x\d{1,4})')
        m = p.search(filepath)
        if m:
            return m.group()

        raise Exception("Unable to get size from filename!")
