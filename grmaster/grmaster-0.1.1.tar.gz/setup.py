# -*- coding: utf-8 -*-

"""Tool for dividing students into groups."""

#   grmaster - tool for dividing students into groups
#   Copyright (C) 2015  Lutov V. S. <vslutov@yandex.ru>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup, find_packages, Command

setup(name='grmaster',
      version='0.1.1',
      description=__doc__,
      maintainer='vslutov',
      maintainer_email='vslutov@yandex.ru',
      url='https://github.com/vslutov/grmaster',
      license='https://gnu.org/licenses/agpl.html',
      platforms=['any'],
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Console",
                   "Environment :: Web Environment",
                   "Intended Audience :: Education",
                   "License :: OSI Approved :: "
                   "GNU Affero General Public License v3 or later (AGPLv3+)",
                   "Natural Language :: Russian",
                   "Natural Language :: English",
                   "Operating System :: Unix",
                   "Operating System :: Microsoft :: Windows",
                   "Programming Language :: Python :: 3 :: Only",
                   "Topic :: Database",
                   "Topic :: Education",
                   "Topic :: Sociology",
                   "Topic :: Utilities"],
      install_requires=['flask',
                        'pytest'],
      packages=find_packages(),
      include_package_data=True,
      entry_points={'console_scripts': ['grmaster = grmaster.__main__:main']},
      )
