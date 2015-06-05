#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

from . import color

#호환 설정
from ... import terminal
terminal.color = color
