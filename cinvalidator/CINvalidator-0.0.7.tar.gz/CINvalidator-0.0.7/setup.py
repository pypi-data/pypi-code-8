from setuptools import setup, find_packages
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CINvalidator',
    version='0.0.7',
    keywords=('Validator', 'Citizen Identification Number'),
    url='https://github.com/imlonghao/CIN-validator',
    license='Apache License 2.0',
    author='imlonghao',
    author_email='shield@fastmail.com',
    description='China Citizen Identification Number Validator',
    long_description=long_description,
    packages=find_packages(),
    platforms='any'
)
