# -*- coding: utf8 -*-

'''
Copyright 2009 Denis Derman <denis.spir@gmail.com> (former developer)
Copyright 2011-2012 Peter Potrowl <peter017@gmail.com> (current developer)

This file is part of Pijnu.

Pijnu is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pijnu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with Pijnu.  If not, see <http://www.gnu.org/licenses/>.
'''


from setuptools import setup

long_description = """\
'pijnu' is
* a parsing language extended from PEG,
* a parser generator for grammars written using this language,
* a tool to help processing processing parse results.

'pijnu' is intended to be clear, easy, practical.
"""

setup(name="pijnu",
      version="20130124",
      author="Denis Derman",
      author_email="denis.spir@gmail.com",
      maintainer="Peter Potrowl",
      maintainer_email="peter.potrowl@gmail.com",
      url="http://www.github.com/peter17/pijnu",
      license="LGPL v3",
      platforms=["Any"],
      packages=["pijnu", "pijnu.generator", "pijnu.library"],
      scripts=[],
      description="text parsing & processing tool",
      long_description=long_description,
      classifiers=[
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Development Status :: 4 - Beta',
          'Topic :: Software Development',
          'Topic :: Text Processing',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          ]
      )
