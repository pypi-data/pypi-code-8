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

"""Setup utils library."""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import time
import zipfile as zip

import appinfo


def sleep(seconds=5):
    """Pause for specified time."""
    time.sleep(seconds)


def app_name():
    """Write application name to text file."""
    with open('app_name.txt', 'w') as file_:
        file_.write(appinfo.APP_NAME)


def app_ver():
    """Write application version to text file if equal to ChangeLog.rst."""
    with open('ChangeLog.rst') as file_:
        changelog_app_ver = file_.readline().split()[0]
    if changelog_app_ver == appinfo.APP_VERSION:
        with open('app_ver.txt', 'w') as file_:
            file_.write(appinfo.APP_VERSION)
    else:
        print('ChangeLog.rst and appinfo.py are not in sync.')


def app_type():
    """Write application type (application or module) to text file."""
    with open('app_type.txt', 'w') as file_:
        file_.write(appinfo.APP_TYPE)


def py_ver():
    """Write Python version to text file."""
    with open('py_ver.txt', 'w') as file_:
        file_.write(str(sys.version_info.major) + '.' +
                    str(sys.version_info.minor))


def remove_copyright():
    """Remove Copyright from README.rst."""
    with open('../README.rst') as file_:
        text = file_.readlines()

    new_text = ''

    for line in text:
        if 'Copyright ' in line:
            pass
        else:
            new_text += line

    with open('../README.rst', 'w') as file_:
        file_.writelines(new_text)


def prep_rst2pdf():
    """Remove parts of rST to create a better pdf."""
    with open('index.ori') as file_:
        text = file_.readlines()

    new_text = ''

    for line in text:
        if 'Contents:' in line:
            pass
        elif 'Indices and tables' in line:
            break
        else:
            new_text += line

    with open('index.rst', 'w') as file_:
        file_.writelines(new_text)

    with open('../README.rst') as file_:
        text = file_.readlines()

    new_text = ''

    for line in text:
        if '.. image:: ' in line or '    :target: ' in line:
            pass
        else:
            new_text += line

    with open('../README.rst', 'w') as file_:
        file_.writelines(new_text)


def create_doc_zip():
    """Create doc.zip to publish in PyPI."""
    doc_path = appinfo.APP_NAME + '/doc'
    with zip.ZipFile('pythonhosted.org/doc.zip', 'w') as archive:
        for root, dirs, files in os.walk(doc_path):
            for file_ in files:
                if not '.pdf' in file_:
                    pathname = os.path.join(root, file_)
                    filename = pathname.replace(doc_path + os.sep, '')
                    archive.write(pathname, filename)


if __name__ == '__main__':
    eval(sys.argv[1])
