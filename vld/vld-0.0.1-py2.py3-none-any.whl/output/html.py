#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


HTML_PREFIX = '''
<DOCTYPE! HTML>
<html>
  <head>
    <!--Load the AJAX API-->
      <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">

         // Load the Visualization API and the piechart package.
         google.load('visualization', '1.0', {'packages':['corechart']});

'''

HTML_SUFFIX = '''
'''
