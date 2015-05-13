#!/usr/bin/env python3

import re, ast, os, pypandoc

from setuptools import setup, find_packages

# Build our reStructuredText version of the readme
output = pypandoc.convert('readme.md', 'rst')
f = open('readme.txt','w+')
f.write(output)
f.close()

# Load our readme as the long_description
long_description = 'Add a fallback short description here'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

# Get our version information
_version_re = re.compile(r'__version__\s*=\s*(.*)')
with open('lyricscreen/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
        name="lyricscreen",
        version=version,

        description="A lyrics management and display web app and server.",
        long_description=long_description,

        url="https://github.com/lytedev/lyricscreen",

        author='Daniel "lytedev" Flanagan',
        author_email="daniel@lytedev.io",

        license="MIT",

        classifiers=[
            'Development Status :: 2 - Pre-Alpha',

            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Information Technology',
            'Intended Audience :: Religion', # Primary use is displaying worship lyrics in a church environment
            'Intended Audience :: System Administrators',

            'Topic :: Communications',
            'Topic :: Communications :: Conferencing',
            'Topic :: Internet',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Multimedia :: Graphics :: Presentation',
            'Topic :: Multimedia :: Graphics :: Viewers',
            'Topic :: Religion',

            'License :: OSI Approved :: MIT License',

            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
        ],

        keywords='lyrics lyric display presentation project projector',

        packages=["lyricscreen"],
        package_data={'lyricscreen': [
            'http/*.*',
            'http/build/*.*',
            'http/sass/*.*',
            'http/css/*.*',
            'http/fonts/*',
            'http/js/*.*',
            'http/css/maps/*.*',
            'http/sass/fontawesome/*.*',
        ]},

        requires=[
            "asyncio",
            "websockets",
            "jsonpickle"
        ],

        entry_points={
            'console_scripts': [
                'lyricscreen=lyricscreen:main',
            ],
        }
    )

