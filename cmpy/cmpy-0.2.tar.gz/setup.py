#!/usr/bin/env python

from setuptools import setup
import os
import cmpy


if os.path.exists('README.md'):
    description_long = open('README.md').read()
else:
    description_long = """ A simple utility for detecting differences in directories and files. """


setup(
    name='cmpy',
    packages=['cmpy'],
    version=cmpy.__version__,
    license=cmpy.__license__,
    description=cmpy.__description__,
    long_description=description_long,
    author=cmpy.__author__,
    author_email=cmpy.__email__,
    url='https://github.com/edaniszewski/cmpy',
    download_url='https://github.com/edaniszewski/cmpy/releases/tag/0.2',
    keywords=['file compare', 'directory compare', 'compare', 'comparison'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
)



