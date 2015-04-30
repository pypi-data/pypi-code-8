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
from crypt import crypt

from .utils import expand_char_set, random_str

crypt_chars = 'A-Za-z0-9./'

def pcrypt(pwd, salt=None, id='6'):
    """Wrapper for standard unix crypt(3) (with glibc extensions) with extra
    features:

    If salt is not given, it is chosen randomly.

    If salt is not in format ``$id$salt$`` and ``id`` parameter is not None,
    it is converted to the correct format.
    """
    chars = expand_char_set(crypt_chars)
    if salt is None:
        salt_len = 2 if id is None else 8
        salt = random_str(chars, salt_len)
    if id is not None and not salt.startswith('$'):
        salt = '${}${}$'.format(id, salt)
    return crypt(pwd, salt)

