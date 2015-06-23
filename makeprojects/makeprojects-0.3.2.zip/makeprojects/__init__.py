#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013-2015 by Rebecca Ann Heineman becky@burgerbecky.com

# It is released under an MIT Open Source license. Please see LICENSE
# for license details. Yes, you can use it in a
# commercial title without paying anything, just give me a credit.
# Please? It's not like I'm asking you for money!

#
# Description data
#

__all__ = [
	'__version__',
	'__author__',
	'__title__',
	'__summary__',
	'__uri__',
	'__email__',
	'__license__',
	'__copyright__'
]

__version__ = '0.3.2'
__author__ = 'Rebecca Ann Heineman <becky@burgerbecky.com>'
__title__ = 'makeprojects'
__summary__ = 'IDE project generator for Visual Studio, XCode, etc...'
__uri__ = 'http://burgerbecky.com'
__email__ = 'becky@burgerbecky.com'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2013-2015 Rebecca Ann Heineman'

#
# Backwards compatability
#

try:
	sorted
except NameError:
	# for python < 2.4 compatibility:
	def sorted(iterable, reverse=False):
		result = list(iterable)
		result.sort()
		if reverse:
			result.reverse()
		return result
