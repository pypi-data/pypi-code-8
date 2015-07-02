# -*- coding: utf-8 -

import codecs
import io
import os

from setuptools import setup

with io.open(os.path.join(os.path.dirname(__file__), 'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'bernhard_cletus',
    version = '0.2.6',
    description = 'Python client for Riemann to test sending metrics with double instead of float. Do not use!',
    long_description = long_description,
    author = 'Cletus',
    author_email = 'Helljunkz@gmail.com',
    #license = 'ASF2.0',
    #url = 'http://github.com/banjiewen/bernhard.git',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: Log Analysis',
        'Topic :: Utilities',
        'Topic :: System :: Networking :: Monitoring'
    ],
    zip_safe = False,
    packages = ['bernhard_cletus'],
    include_package_data = True,
    install_requires=['protobuf >= 2.4']
)
