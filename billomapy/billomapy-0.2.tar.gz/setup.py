from setuptools import setup, find_packages

setup(
    name='billomapy',
    version='0.2',
    install_requires=['requests==2.7.0'],
    packages=find_packages(),
    url='https://github.com/bykof/billomapy',
    license='Apache License 2.0',
    author='mbykovski',
    author_email='mbykovski@seibert-media.net',
    description='A Python library for http://www.billomat.com/'
)
