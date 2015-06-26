
# -*- coding: utf-8 -*-

"""
Function composition is simple, just use funcomp.
Copyright (C) 2015, Bence Faludi (bence@ozmo.hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, <see http://www.gnu.org/licenses/>.
"""

from functools import reduce
from collections import Iterable, Callable

class NotCallable(TypeError):
    pass

class absorb(object):
    def __init__(self, func, use_original = False):
        if not isinstance(func, Callable):
            raise NotCallable('absorb got a `{}` object.' \
                .format( type(func).__name__ ))
        self.func = func
        self.use_original = use_original

    def __call__(self, value, *args, **kwargs):
        try:
            return self.func(value, *args, **kwargs)

        except:
            return None \
                if not self.use_original \
                else value

class Composition(object):
    def __init__(self, *functions):
        functions = list(functions)
        for func in functions:
            if not isinstance(func, Callable):
                raise NotCallable( \
                    "Composition is containing a `{}` object." \
                    .format( type(func).__name__ ))

        self.functions = functions

    def __call__(self, value = None):
        if not self.functions:
            return value

        return reduce(lambda value, func: func(value), self.functions, value)