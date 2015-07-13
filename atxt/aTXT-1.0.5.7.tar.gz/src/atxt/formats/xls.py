#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-07-13 02:48:24
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-13 02:48:54
import xlrd
import os

from _utils import save_raw_data
from xlsx import xlsx


def xls(from_file, to_txt, opts):
    return xlsx(from_file, to_txt, opts)
