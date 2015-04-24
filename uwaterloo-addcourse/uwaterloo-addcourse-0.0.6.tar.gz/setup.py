#!/usr/bin/env python

from setuptools import *

script = __import__('addcourse')

setup(
    name='uwaterloo-addcourse',
    version=script.__version__, 
    license=script.__license__,
    maintainer=script.__maintainer__,
    maintainer_email=script.__email__,
    description=script.__doc__,
    scripts=['addcourse.py'],

    install_requires=[
        'beautifulsoup4',
    ],
)
