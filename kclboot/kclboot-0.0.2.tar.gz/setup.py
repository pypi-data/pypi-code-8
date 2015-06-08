from setuptools import setup, find_packages
from os import path
from kclboot import PACKAGE_VERSION

setup(
    name='kclboot',
    version=PACKAGE_VERSION,
    description='Unofficial AWS Kinesis Client Library Bootstrapper',
    url='https://github.com/nivardus/kclboot',
    author='Bennett Goble',
    author_email='bennettgoble@gmail.com',
    license='MIT',
    download_url='https://github.com/nivardus/kclboot/tarball/0.0.1',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='aws amazon kinesis',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kclboot=kclboot.command:main'
        ]
    }
)
