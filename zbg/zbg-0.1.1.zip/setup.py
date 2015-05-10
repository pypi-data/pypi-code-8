''' zbg: A python library for zbg encodings.

zbg is a general-purpose library for serialization and deserialization 
with zbg encoding. It is a very simple format supporting nested 
containers and arbitrary binary blobs, with a slightly more efficient
implementation of 256-bit and 512-bit objects, intended to be used with
cryptographic hashes and keys.
'''

# Global dependencies
import subprocess

# Bootstrap setuptools
import ez_setup
# Dunno why I need this but I think I do?
# try:
#     del pkg_resources, setuptools
# except NameError:
#     pass
# Carry on then. This seems to have issues with bad versions of setuptools
ez_setup.use_setuptools(version='2.0')

# Import global dependencies required for setup.py
from setuptools import setup, find_packages

metadata = dict(
    name = 'zbg',
    version = '0.1.1',
    description = 'A python library for zbg encodings.',
    long_description = 'zbg is a general-purpose library for '
                       'serialization and deserialization with zbg '
                       'encoding. It is a very simple format '
                       'supporting nested containers and arbitrary '
                       'binary blobs, with a slightly more efficient '
                       'implementation of 256-bit and 512-bit objects, '
                       'intended to be used with cryptographic hashes '
                       'and keys.',
    url = 'https://github.com/Muterra/py_zbg',
    author = 'Nick Badger',
    author_email = 'badg@muterra.io',
    license = 'GNU LGPL v2.1',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries'
        ],
    keywords = 'zbg serialization muterra eic encoding decoding',
    packages = find_packages(),
    install_requires = [],
    package_data = {}
    )

if __name__ == '__main__':
    # Call setup.
    setup(**metadata)