import sys
import os

try:
    from setuptools import setup
except ImportError:
    print("Distribute is required for install:")
    print("    http://python-distribute.org/distribute_setup.py")
    sys.exit(1)

from eveparser import __version__


description = ("A Python library to help parse various things that are "
               "copy/pastable from the Eve Online UI.")

if os.path.exists('README.rst'):
    f = open('README.rst')
    try:
        long_description = f.read()
    finally:
        f.close()
else:
    long_description = description

setup(
    name='eveparser',
    version=__version__,
    description=description,
    long_description=long_description,
    author='Richard Schwab',
    author_email='richard@rep.pm',
    url='https://github.com/Nothing4You/eveparser',
    packages=['eveparser', 'eveparser.parsers'],
    license='MIT',
    zip_safe=False,
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        ],
    bugtrack_url='https://github.com/Nothing4You/eveparser/issues',
)
