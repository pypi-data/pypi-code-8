#import ez_setup
#ez_setup.use_setuptools()

from setuptools import setup, find_packages


exec(open('tree_sisters/version.py').read()) # loads __version__

setup(name='tree_sisters',
      version=__version__,
      author='$AUTHOR',
    description='',
    long_description=open('README.rst').read(),
    license='see LICENSE.txt',
    keywords="",
    install_requires=['tree2tax'],
    packages= find_packages(exclude='docs'))
