"""
setup.py for pip upload
"""
from setuptools import setup
from setuptools import find_packages

setup(
    name='bce-python-sdk',
    version='0.8.4',
    keywords = ('bce', 'sdk'),
    description='BCE-Python-SDK for BCE',
    license='Free',
    author='boss-rd',
    author_email='boss-rd@baidu.com',
    url='http://bce.baidu.com',
    platforms = 'any',
    zip_safe = False,
    packages = find_packages('bce-python-sdk-0.8.4'),
    package_dir = {'':'bce-python-sdk-0.8.4'}
)
