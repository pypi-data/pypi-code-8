#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""dknorway - Models to hold Fylke, Kommune and PostSted + import script of file from Bring (Posten).
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Topic :: Software Development :: Libraries
"""

import setuptools
from distutils.core import setup, Command


version = '0.1.0'


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='dknorway',
    version=version,
    url="https://github.com/datakortet/dknorway",
    maintainer="Bjorn Pettersen",
    maintainer_email="bp@datakortet.no",
    requires=[],
    install_requires=[
        'Django',
        'South'
    ],
    description=__doc__.strip(),
    classifiers=[line for line in classifiers.split('\n') if line],
    long_description=open('README.rst').read(),
    cmdclass={'test': PyTest},
    packages=['dknorway'],
    zip_safe=False,
)
