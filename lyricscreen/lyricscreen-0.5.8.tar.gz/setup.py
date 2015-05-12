#!/usr/bin/env python3

import re, ast, os

from distutils.core import setup

long_description = 'Add a fallback short description here'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

_version_re = re.compile(r'__version__\s*=\s*(.*)')
with open('lyricscreen/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
        name="lyricscreen",
        version=version,
        description="A lyrics management and display web app and server.",
        author="Daniel Flanagan",
        author_email="daniel@lytedev.io",
        url="https://github.com/lytedev/lyricscreen",
        license="MIT",
        long_description=long_description,

        packages=["lyricscreen"],
        package_data={'lyricscreen': ['http/*', 'http/**/*']},
        scripts=["scripts/lyricscreen"],
        requires=[
            "asyncio",
            "websockets",
            "jsonpickle"
        ],
    )

