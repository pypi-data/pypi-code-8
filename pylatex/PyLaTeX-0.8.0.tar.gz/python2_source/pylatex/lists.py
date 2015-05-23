# -*- coding: utf-8 -*-
u"""
    pylatex.lists
    ~~~~~~~

    This module implements the class that deals with latex List objects
    specifically Enumerate and Itemize.

    :copyright: (c) 2015 by Sean McLemon.
    :license: MIT, see License for more details.
"""

from __future__ import absolute_import
from .base_classes import BaseLaTeXNamedContainer


class List(BaseLaTeXNamedContainer):

    u"""A class that represents a list."""

    def __init__(self, list_spec=None, data=None, pos=None, **kwargs):
        u"""
            :param list_spec:
            :param list_type:
            :param data:
            :param pos:

            :type list_spec: str
            :type list_type: str
            :type data: list
            :type pos: list
        """
        super(List, self).__init__(data=data, options=pos, argument=list_spec, **kwargs)

    def _item(self, label=None):
        u""" Begin an item block. """
        if label:
            return ur'\item[' + label + u'] '

        return ur'\item '

    def add_item(self, s):
        u""" Adds an item to the list.

            :param s:

            :type s: string
        """
        self.append(self._item())
        self.append(s)


class Enumerate(List):

    u""" A class that represents an enumerate list """


class Itemize(List):

    u""" A class that represents an itemize list """


class Description(List):

    u""" A class that represents a description list """

    def add_item(self, label, s):
        u""" Adds an item to the list.

            :param label:
            :param s:

            :type label: string
            :type s: string
        """
        self.append(self._item(label))
        self.append(s)
