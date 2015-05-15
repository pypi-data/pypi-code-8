#!/usr/bin/env python

from setuptools import setup
import cmpy


setup(
    name='cmpy',
    packages=['cmpy'],
    version=cmpy.__version__,
    license=cmpy.__license__,
    description=cmpy.__description__,
    author=cmpy.__author__,
    author_email=cmpy.__email__,
    url='https://github.com/edaniszewski/cmpy',
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



