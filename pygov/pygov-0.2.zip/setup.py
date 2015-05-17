__author__ = 'scarroll'

from distutils.core import setup

setup(
    name='pygov',
    version='0.2',
    package_dir={'pygov': 'src'},
    packages=['pygov',],
    license='The MIT License (MIT)',
    description='pygov enables easy access to the US Government''s data APIs (http://api.data.gov/docs/).',
    long_description=open('README.rst').read(),
)