# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Raul Ramos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
-------------------------------------------------------------------------------
simpleEnum - A really really simple Python enum class
-------------------------------------------------------------------------------

example:

> from simpleEnum import Enum
> EWorkDays = Enum ("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY")
> print EDays.WEDNESDAY

This will print 2

> EPlatform = Enum (LINUX=1<<0, OSX=1<<1, WINDOWS=1<<2)
> print EPlatform.OSX

This will print 2
"""
__version__ = '0.0.6'

from collections import OrderedDict


class Enum:
    def __init__(self, *items, **flags):
        assert (len(items) > 0) or (len(flags) > 0), "Missing parameters"
        assert (len(items) > 0) != (len(flags) > 0), "Flags and no flags not allowed"  # NOQA
        assert len(items) == len(set(items)), "Duplicated item"
        assert len(flags) == len(set(flags)), "Duplicated flag"
        if len(items):
            self.odict = OrderedDict([(x, idx) for idx, x in enumerate(items)])
        else:
            self.odict = flags

    def __getattr__(self, _name):
        try:
            return self.odict[_name]
        except KeyError, e:
            raise ValueError(str(e))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[ %s ]" % ", ".join (["%s(%s)"%(x, y) for x, y in self.odict.items()])

    def tostr(self, _val):
        for k, v in self.odict.items():
            if v == _val:
                return k

        raise ValueError("%s not in enumeration" % _val)

