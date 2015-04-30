#
# PWUtils - tools for manipulating passwords
# Copyright (C) 2015  Michal Belica <devel@beli.sk>
#
# This file is part of PWUtils.
#
# PWUtils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PWUtils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PWUtils.  If not, see <http://www.gnu.org/licenses/>.
#
import random

"""
Support functions for pwutils.
"""

rand_eng = random.SystemRandom()

def expand_char_set(chars):
    """Returns chars with (from)-(to) sequences expanded. To include a literal
    minus (-), place it at the end. E.g.:

    >>> expand_char_set('a-z.-')
    'abcdefghijklmnopqrstuvwxyz.-'
    """
    while True:
        i = chars.find('-')
        if i == -1 or i == len(chars)-1:
            break
        str_to_expand = chars[i-1:i+2]
        ord_from = ord(str_to_expand[0])
        ord_to = ord(str_to_expand[2])
        seq = ''.join([chr(i) for i in range(ord_from, ord_to+1)])
        chars = chars.replace(str_to_expand, seq, 1)
    return chars

def random_str(chars, length, length_to=None):
    """Returns ``length`` long sequence of random picks from chars.
    If ``length_to`` is defined, random length between ``length`` and
    ``length_to`` is chosen.
    """
    if length_to is not None:
        length = rand_eng.randint(length, length_to)
    return ''.join((rand_eng.choice(chars) for i in range(length)))

