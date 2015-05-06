from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sar-tool',
    version='1.0.1',
    description='Search and replace tool that outputs a diff compatible with patch',
    long_description=long_description,
    url='https://github.com/naufraghi/sar',
    author='Matteo Bertini',
    author_email='matteo@naufraghi.net',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Systems Administration',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities'
    ],
    keywords='sed grep awk diff patch',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'sar=sar:main',
        ],
    },
)
