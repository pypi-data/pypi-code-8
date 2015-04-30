#!/usr/bin/env python3
from setuptools import setup, find_packages
from codecs import open # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get version number
defs = {}
with open(path.join(here, 'src/pwutils/defs.py')) as f:
    exec(f.read(), defs)

setup(
    name='pwutils',
    version=defs['__version__'],
    description=defs['app_description'],
    long_description=long_description,
    url='https://github.com/beli-sk/pwutils',
    author="Michal Belica",
    author_email="devel@beli.sk",
    license="GPL-3",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        ],
    keywords=['password'],
    zip_safe=True,
    package_dir={'': 'src'},
    packages=['pwutils'],
    entry_points={
        'console_scripts': [
            'pcrypt = pwutils:pcrypt_cmd',
            'pwgen = pwutils:pwgen_cmd',
            ],
        },
    )

