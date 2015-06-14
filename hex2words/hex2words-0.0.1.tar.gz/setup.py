from setuptools import setup
from hex2words.version import (
    __version__, __license__, __url__,
    __program_name__, __short_description__,
    __main_author_name__, __main_author_email__
)


with open('README.rst') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')


setup(
    name=__program_name__,
    version=__version__,
    description=__short_description__,
    license=__license__,
    author=__main_author_name__,
    author_email=__main_author_email__,
    url=__url__,
    scripts=['bin/hex2words'],
    # Via PyPackage:
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Artistic Software',
        'Topic :: Security'
    ],
    packages=['hex2words',],
    long_description=long_description,
    keywords=['hexadecimal', 'fingerprint', 'gpg', 'pgp', 'pgp words'],
)
