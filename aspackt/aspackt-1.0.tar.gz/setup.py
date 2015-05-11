from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='aspackt',
    version='1.0',
    description='Arrange rectangles while approximating an aspect ratio',
    url='https://github.com/jdodds/aspackt',
    author='Jeremiah Dodds',
    author_email='jeremiah.dodds@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='rectangle box packing',
    py_modules=['aspackt'],
)
