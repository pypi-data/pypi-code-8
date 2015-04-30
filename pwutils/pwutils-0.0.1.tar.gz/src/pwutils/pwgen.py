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
from .utils import expand_char_set, random_str

def pwgen(chars, length, length_to=None):
    chars = expand_char_set(chars)
    return random_str(chars, length, length_to)

