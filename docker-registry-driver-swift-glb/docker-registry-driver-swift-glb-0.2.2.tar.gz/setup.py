#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import setuptools
except ImportError:
    import distutils.core as setuptools


__author__ = 'Wagner Souza'
__copyright__ = 'Copyright 2015'
__credits__ = []

__license__ = 'Apache 2.0'
__version__ = '0.2.2'
__maintainer__ = 'Wagner Souza'
__email__ = 'wagnersza@gmail.com'
__status__ = 'Production'

__title__ = 'docker-registry-driver-swift-glb'
__build__ = 0x000000

__url__ = 'https://github.com/wagnersza/docker-registry-driver-swift-glb'
__description__ = 'Docker registry swift driver'
d = 'https://github.com/wagnersza/docker-registry-driver-swift-glb/archive/master.zip'

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    maintainer=__maintainer__,
    maintainer_email=__email__,
    url=__url__,
    description=__description__,
    download_url=d,
    long_description=open('./README.md').read(),
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 # 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 # 'Programming Language :: Python :: 3.2',
                 # 'Programming Language :: Python :: 3.3',
                 # 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Operating System :: OS Independent',
                 'Topic :: Utilities',
                 'License :: OSI Approved :: Apache Software License'],
    platforms=['Independent'],
    license=open('./LICENSE').read(),
    namespace_packages=['docker_registry', 'docker_registry.drivers'],
    packages=['docker_registry', 'docker_registry.drivers'],
    install_requires=open('./requirements.txt').read(),
    zip_safe=True,
    tests_require=open('./tests/requirements.txt').read(),
    test_suite='nose.collector'
)
