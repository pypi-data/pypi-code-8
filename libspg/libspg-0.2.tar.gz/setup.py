"""
Setup script for libspg
"""

from setuptools import setup

__title__ = 'libspg'
__summary__ = 'Python library for interacting with Brazil NPAC SPG'
__url__ = 'http://bitbucket.org/asenci/libspg'

__version__ = '0.2'

__author__ = 'Andre Sencioles Vitorio Oliveira'
__email__ = 'andre@bcp.net.br'

__license__ = 'ISC License'


setup(
    name=__title__,
    description=__summary__,
    long_description=open('README.rst').read(),
    url=__url__,

    author=__author__,
    author_email=__email__,
    license=__license__,

    version=__version__,

    packages=['libspg'],
    test_suite='tests',

    platforms='any',
    keywords=['BDO', 'LNP', 'NPAC', 'SOA', 'SPG'],
    classifiers=[
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    install_requires=['lxml']
)
