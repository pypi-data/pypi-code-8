import os
import sys

py_version = sys.version_info[:2]
if py_version < (2, 7):
    raise RuntimeError('ApiDaemon client requires Python 2.7 or later')

from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))

README = """ Client for ApiDaemon-service """
CHANGES = ''

CLASSIFIERS = [
    'Natural Language :: English',
    'Operating System :: POSIX',
    "Programming Language :: Python :: 2.7",
]

dist = setup(
    name='ApiSyncClient',
    version='1.0',
    license='MIT-license',
    url='https://github.com/tsyganov-ivan/ApiDaemon',
    description="Client for ApiDaemon-service",
    long_description=README,
    classifiers=CLASSIFIERS,
    author="Ivan Tsyganov",
    author_email="tsyganov.ivan@gmail.com",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
