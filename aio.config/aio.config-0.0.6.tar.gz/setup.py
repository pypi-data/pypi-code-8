"""
aio.config
"""
import os
import sys
from setuptools import setup, find_packages

version = "0.0.6"

install_requires = ['setuptools', 'aio.core']

if sys.version_info < (3, 4):
    install_requires += ['asyncio']

tests_require = install_requires + ['aio.testing']

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = read("README.rst")

setup(
    name='aio.config',
    version=version,
    description="Aio configuration utilities",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='',
    author='Ryan Northey',
    author_email='ryan@3ca.org.uk',
    url='http://github.com/phlax/aio.config',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['aio'],
    include_package_data=True,
    package_data={'': ['tests/resources/*.conf', 'tests/resources/sub/etc/*.conf', '*.rst']},    
    zip_safe=False,
    tests_require=tests_require,
    test_suite="aio.config.tests",
    install_requires=install_requires,
    entry_points="""
    # -*- Entry points: -*-
    """)
