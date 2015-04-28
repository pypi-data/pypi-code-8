#!/usr/bin/env python


"""
Setup script for str2type
"""


import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as f:
    readme = f.read().strip()


with open('LICENSE.txt') as f:
    license_content = f.read().strip()


version = None
author = None
email = None
source = None
with open(os.path.join('str2type', '__init__.py')) as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__author__'):
            author = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__email__'):
            email = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__source__'):
            source = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif None not in (version, author, email, source):
            break


setup(
    name='str2type',
    version=version,
    author=author,
    author_email=email,
    description="Convert a string representation of an int, float, None, True, False, or "
                "JSON to its native type.  For None, True, and False, case is irrelevant.",
    long_description=readme,
    url=source,
    license=license_content,
    packages=['str2type'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    include_package_data=True,
    zip_safe=True,
    keywords='python string to type string2type str2type'
)
