#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009-2015 Joao Carlos Roseta Matos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Localization."""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# import builtins  # Python 3 compatibility
# import future  # Python 3 compatibility
# import io  # Python 3 compatibility
import locale


def sys_lang():
    """Get system language."""
    lang = locale.getdefaultlocale()
    # lang = 'EN'  # only for testing
    if 'pt_' in lang[0]:  # Portuguese
        return 'PT'
    else:  # English
        return 'EN'

LANG = sys_lang()

if LANG == 'PT':  # Portuguese
    ABOUT = 'Sobre'
    CHILD = 'Criança:'
    CONFIRM_EXIT = 'Tem a certeza que pretende sair?'
    DAYS_RANGE = 'O número de dias tem que estar entre 0 e '
    EXIT = 'Sair'
    FILE = 'Ficheiro'
    FILE_NOT_FOUND = 'Erro: ficheiro não encontrado - '
    HELP = 'Ajuda'
    LAST_UPDATE = 'Última atualização:'
    SET = 'Atribuir'
    UPDATE = 'Atualizar'
    VERSION = 'Versão'
    VERSION_WITH_SPACES = ' versão '
    WARNING = 'AVISO'
    WIN_TITLE = 'Dias de castigo'
    WRONG_ARG = 'Erro: argumento incorreto '
else:  # English
    ABOUT = 'About'
    CHILD = 'Child:'
    CONFIRM_EXIT = 'Are you sure you want to exit?'
    DAYS_RANGE = 'Number of days must be between 0 and '
    EXIT = 'Exit'
    FILE = 'File'
    FILE_NOT_FOUND = 'Error: file not found - '
    HELP = 'Help'
    LAST_UPDATE = 'Last update:'
    SET = 'Set'
    UPDATE = 'Update'
    VERSION = 'Version'
    VERSION_WITH_SPACES = ' version '
    WARNING = 'WARNING'
    WIN_TITLE = 'Days grounded'
    WRONG_ARG = 'Error: incorrect argument '


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
