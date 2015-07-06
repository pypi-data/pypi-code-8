"""
setup.py for pip upload
"""
from setuptools import setup
from setuptools import find_packages

setup(
    name='bos-python-sdk',
    version='0.8.4',
    keywords = ('bos', 'sdk'),
    description='BOS-Python-SDK',
    license='Free',
    author='boss-rd',
    author_email='boss-rd@baidu.com',
    url='http://bce.baidu.com/Product/BOS.html',
    platforms = 'any',
    zip_safe = False,
    packages = find_packages('bce-python-sdk-0.8.4'),
    package_dir = {'':'bce-python-sdk-0.8.4'}
)
