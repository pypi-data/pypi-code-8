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
import sys
import argparse

from .pcrypt import pcrypt
from .pwgen import pwgen
from .defs import __version__, app_name, app_description, app_name_desc


def pcrypt_cmd():
    parser = argparse.ArgumentParser(description=app_name_desc)
    parser.add_argument('--pwd', '-p', default=None,
            help='password (read from stdin if not given)')
    parser.add_argument('--salt', '-s', default=None,
            help='salt (generate random if not given)')
    parser.add_argument('--id', '-i', default='6',
            help='algorithm ID used when generating salt (see crypt(3)), '
            '0 for standard DES (default: %(default)s)')
    parser.add_argument('--version', action='version',
            version='{} {}'.format(app_name, __version__))
    args = parser.parse_args()

    if args.pwd is None:
        pwd = sys.stdin.readline().rstrip("\n")
    else:
        pwd = args.pwd
    id = args.id if args.id != '0' else None
    cp = pcrypt(pwd, args.salt, id)
    if cp is None:
        print('crypt() returned no data', file=sys.stderr)
        return 1
    else:
        print(cp)


def pwgen_cmd():
    parser = argparse.ArgumentParser(description=app_name_desc)
    parser.add_argument('--charset', '-c', default='A-Za-z0-9',
            help='character set (default: %(default)s)')
    parser.add_argument('--length', '-l', default=10, type=int,
            help='password length (default: %(default)s)')
    parser.add_argument('--maxlength', '-m', default=None, type=int,
            help='if given, length will be chosen randomly between length and maxlength')
    parser.add_argument('--version', action='version',
            version='{} {}'.format(app_name, __version__))
    args = parser.parse_args()

    print(pwgen(args.charset, args.length, args.maxlength))

