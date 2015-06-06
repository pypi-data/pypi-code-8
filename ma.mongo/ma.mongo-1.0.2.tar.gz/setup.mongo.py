from setuptools import setup
import shutil, os
VERSION = '1.0.2'
SDIST = 'ma.mongo-' + VERSION

try:
    os.mkdir(SDIST)
    shutil.copyfile('setup.mongo.py', SDIST +'/setup.py')
except:
    pass

setup(
    name='ma.mongo',
    version = VERSION,
    description='MongoDB utilities',
    author='Fredrik Haard',
    author_email='fredrik@metallapan.se',
    packages=['ma.mongo']
)
