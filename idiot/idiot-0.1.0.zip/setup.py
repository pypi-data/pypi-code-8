from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='idiot',
    version='0.1.0',
    description='IDIOT API for Python',
    long_description=long_description,
    url='https://github.com/tenevdev/python-idiot',
    author='Tencho Tenev',
    author_email='tenev.dev@outlook.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='iot pi microcontroller api',
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests']
)