""" Simple constant management library

pyconsts, simple constant management library
Copyright (C)2015 Pierre Jaury

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Except for configuration-based constants that should be managed in
configuration files, one often has to declare module-specific constants when
writing code. For instance: one might plan on coding multiple choice values,
naming monkey-patched attributes or dynamic database fields.

Dictionaries are the most straightforward implementation. Object-like syntax is
however best suited for code readability and one should make sure these
constants are in fact constant (not modified during the course of the program).

Enum are also quite useful at achieving this goal, yet they lack the
immutability and their syntax is more suited for enumerating attributes than
storing constant values.
"""


class ConstObject(object):
    """ Immutable object.

    No constant should be modified:
    >>> CONSTS = ConstObject()
    >>> CONSTS.x = 1
    Traceback (most recent call last):
      ...
    SyntaxError: Cannot modify a constant object
    """

    def __setattr__(self, key, value):
        raise SyntaxError("Cannot modify a constant object")


def array(source):
    """ Builds an object from a dictionary.
    """
    return type("const", (ConstObject,), source)()


def index(*keys):
    """ Numeric index with constant keys.

    A constant index is built based on string keys, conventions dictate
    those keys should be uppercase:
    >>> CONSTS = index("FIRST", "SECOND", "THIRD")

    Keys may then be accessed, values are integers:
    >>> CONSTS.FIRST
    0
    >>> CONSTS.SECOND
    1
    >>> type(CONSTS.FIRST) is int
    True
    """
    return array({key: index for index, key in enumerate(keys)})


def text(pattern, *keys):
    """ Text constants with distinctive values.

    >>> CONSTS = text("test%s", "FIRST", "SECOND", "THIRD")
    >>> CONSTS.FIRST
    'testFIRST'
    >>> CONSTS.SECOND
    'testSECOND'
    """
    return array({key: pattern % key for key in keys})


if __name__ == "__main__":
    import doctest
    doctest.testmod()
