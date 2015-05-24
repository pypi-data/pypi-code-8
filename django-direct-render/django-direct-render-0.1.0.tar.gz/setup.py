import os
from setuptools import setup

VERSION='0.1.0'

with open(os.path.join(os.path.dirname(__file__), 'readme.md')) as readme:
    README = readme.read()

description = 'A simple Django app that will render template directly for you'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-direct-render',
    version=VERSION,
    packages=['direct_render'],
    include_package_data=True,
    license='BSD License',  # example license
    description=description,
    long_description=README,
    author='Tim Hsu',
    author_email='tim.yellow@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
