from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def read(f):
    return open(path.join(here, f), encoding='utf-8').read().strip()

requires = [
    'pyramid',
    'nose',
    'webtest',
]

tests_require = []

setup(
    name='djed.testing',
    version='0.1',
    description='Base unit test case for Pyramid',
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
    classifiers=[
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
    ],
    author='Djed developers',
    author_email='djedproject@googlegroups.com',
    url='https://github.com/djedproject/djed.testing',
    license='ISC License (ISCL)',
    keywords='web pyramid pylons djed',
    packages=['djed'],
    include_package_data=True,
    install_requires=requires,
    extras_require={
        'testing': tests_require,
    },
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
        ],
    },
)
