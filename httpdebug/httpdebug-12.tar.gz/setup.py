# coding=utf-8
"""
httpdebug
-
author  : rabshakeh (erik@a8.nl)
project : httpdebug
created : 19-05-15 / 16:41
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

from setuptools import setup
setup(name='httpdebug',
      version='12',
      description='Curl based http downloader with debug information',
      url='https://github.com/erikdejonge/httpdebug',
      author='Erik de Jonge',
      author_email='erik@a8.nl',
      license='GPL',
      entry_points={
          'console_scripts': [
              'httpdebug=httpdebug:main',
          ],
      },
      packages=['httpdebug'],
      zip_safe=True,
      install_requires=['cmdssh', 'consoleprinter', 'docopt'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Development Status :: 4 - Beta ",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: POSIX",
          "Environment :: MacOS X",
          "Topic :: System",
          "Topic :: Software Development :: Debuggers",
          "Topic :: Internet :: WWW/HTTP"
      ])
