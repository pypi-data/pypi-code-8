#!/usr/bin/env python

name = 'rolodexer'
long_name = 'rolodexer'
version = '0.1.1'
packages = [name]
description = "Parse rolodex data and output JSON"

keywords = [
    'JSON','CSV','rolodex','contact','database','parse'
]

long_description = """
    
    Rolodexer - parse comma-separated "rolodex" data files and output JSON.
    
"""


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Other Environment',
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Topic :: Database',
    'Topic :: Utilities',
]

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

if 'sdist' in sys.argv and 'upload' in sys.argv:
    """ CLEAN THIS MESS UP RIGHT NOW YOUNG MAN """
    import commands
    import os
    finder = "/usr/bin/find %s \( -name \*.pyc -or -name .DS_Store \) -delete"
    theplace = os.getcwd()
    if theplace not in (".", "/"):
        print("+ Deleting crapola from %s..." % theplace)
        print("$ %s" % finder % theplace)
        commands.getstatusoutput(finder % theplace)
        print("")

setup(

    name=long_name, version=version, description=description,
    long_description=long_description,
    download_url=('http://bitbucket.org/fish2000/%s/zipball/master' % long_name),

    author=u"Alexander Bohn",
    author_email='fish2000@gmail.com',
    url='http://bitbucket.org/fish2000/%s' % long_name,
    license='GPLv2',
    keywords=', '.join(keywords),
    platforms=['any'],
    
    include_package_data=True,
    
    packages=[]+packages,
    
    package_dir={
        'rolodexer': 'rolodexer',
    },
    
    entry_points={
        'console_scripts': [
            'rolodexer = rolodexer.cli:cli'
        ],
    },
    
    package_data={},
    install_requires=['phonenumbers', 'docopt'],

    classifiers=classifiers+[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy'],
)

