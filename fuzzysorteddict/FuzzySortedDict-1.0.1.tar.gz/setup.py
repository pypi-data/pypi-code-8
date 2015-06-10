from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='FuzzySortedDict',
    version='1.0.1',
    description='A sorted dictionary with nearest-key lookup',
    long_description=long_description,
    url='https://github.com/ncsuarc/FuzzySortedDict',
    author='NC State Aerial Robotics Club',
    author_email='contact@aerialroboticsclub.com',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='dictionary',
    packages=['FuzzySortedDict'],
    install_requires=['blist'],
)
