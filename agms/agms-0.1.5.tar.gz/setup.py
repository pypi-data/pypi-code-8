import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = []

if sys.version_info < (2, 6):
    warnings.warn(
        'Python 2.5 is no longer officially supported by Agms. '
        'If you have any questions, please file an issue on Github or '
        'contact us at developer@agms.com.',
        DeprecationWarning)
    install_requires.append('requests >= 0.8.8, < 0.10.1')
    install_requires.append('ssl')
else:
    install_requires.append('requests >= 2.5.3')
    install_requires.append('pyopenssl')
    install_requires.append('ndg-httpsclient')
    install_requires.append('pyasn1')

# Don't import agms module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agms'))

setup(
    name='agms',
    cmdclass={'build_py': build_py},
    version='0.1.5',
    description='Agms Python Library',
    long_description='Agms Python Library for Payment Gateway',
    author='Maanas Royy',
    author_email='maanas@agms.com',
    url='https://github.com/agmscode/agms_python',
    packages=['agms', 'agms.exception', 'agms.request', 'agms.response', 'agms.util', 'agms.test'],
    package_data={'agms': []},
    install_requires=install_requires,
    test_suite='agms.test.all',
    use_2to3=True,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])