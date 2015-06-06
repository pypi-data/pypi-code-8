from setuptools import setup
import shutil, os
VERSION = '1.0.1'
SDIST = 'ma.mongo-' + VERSION

os.mkdir(SDIST)
shutil.copyfile('setup.mongo.py', SDIST +'/setup.py')

setup(
    name='ma.mongo',
    version = VERSION,
    description='MongoDB utilities',
    author='Fredrik Haard',
    author_email='fredrik@metallapan.se',
    packages=['ma.mongo']
)
