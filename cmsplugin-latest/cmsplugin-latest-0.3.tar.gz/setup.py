#!/usr/bin/env python

from distutils.core import setup

####### Used for compatability with python 2.2.3 ######
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
########################################################

with open('README.rst') as file:
    long_description = file.read()
    file.close()

setup(
    # Required information
    name='cmsplugin-latest',
    version='0.3',         # major.minor[.patch[.sub]]
    url='https://www.gitorious.org/cmsplugin-latest',
    
    # Switch out
    author='Jordan Hewitt',          # or user maintainer
    author_email='jordannh@sent.com',    # or use maintainer_email
    maintainer='',
    maintainer_email='',
    
    # optional
    description = "Show the latest updates from various models",
    long_description=long_description,
    download_url='',
    classifiers=['Topic :: Internet :: WWW/HTTP :: WSGI :: Application', ],
    platforms=['', ''],
    license='GPLv3',
    
    data_files = ['README.rst',],
    packages = ['cmsplugin_latest', ],
)
