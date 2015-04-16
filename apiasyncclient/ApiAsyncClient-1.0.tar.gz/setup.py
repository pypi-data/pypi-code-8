import os
import sys

py_version = sys.version_info[:2]
if py_version < (3, 4):
    raise RuntimeError('ApiDaemon AsyncClient requires Python 3.4 or later')

from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))

README = """ Async client for ApiDaemon-service """
CHANGES = ''

CLASSIFIERS = [
    'Natural Language :: English',
    'Operating System :: POSIX',
    "Programming Language :: Python :: 3.4",
]

dist = setup(
    name='ApiAsyncClient',
    version='1.0',
    license='MIT-license',
    url='https://github.com/tsyganov-ivan/ApiDaemon',
    description="Async client for ApiDaemon-service",
    long_description=README,
    classifiers=CLASSIFIERS,
    author="Ivan Tsyganov",
    author_email="tsyganov.ivan@gmail.com",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
