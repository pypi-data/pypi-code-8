__author__ = 'scarroll'

from distutils.core import setup

setup(
    name='pygov',
    version='0.1',
    package_dir={'pygov': 'src'},
    packages=['pygov',],
    license='The MIT License (MIT)',
    long_description=open('README.txt').read(),
)