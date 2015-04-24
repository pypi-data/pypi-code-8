#!/usr/bin/env python

from setuptools import *
import addcourse

setup(
    name='uwaterloo-addcourse',
    version=addcourse.__version__, 
    license=addcourse.__license__,
    maintainer=addcourse.__maintainer__,
    maintainer_email=addcourse.__email__,
    description=addcourse.__doc__,
    scripts=[addcourse.__file__],

    requires=[
        'beautifulsoup4',
    ],

    use_2to3=True,
)
