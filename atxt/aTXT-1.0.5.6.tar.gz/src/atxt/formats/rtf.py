#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-07-12 18:21:31
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-12 18:25:52

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter
from _utils import save_raw_data


def rtf(from_file, to_txt, opts):
    doc = Rtf15Reader.read(open(from_file.path, "rb"))
    text = PlaintextWriter.write(doc).getvalue()
    return save_raw_data(to_txt.path, text)
