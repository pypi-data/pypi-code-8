from __future__ import absolute_import
import os
from setuptools import setup, find_packages

VERSION = '0.7'

BASEDIR = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASEDIR, 'README.rst')).read()

setup(
    name='fixturegen',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mako >= 1.0",
        "click >= 3.0",
        "sqlalchemy >= 0.6"
    ],
    entry_points={
        'console_scripts':
            ['fixturegen-sqlalchemy = fixturegen.cli:sqlalchemy'],
    },
    url='https://github.com/anton44eg/fixturegen',
    download_url='https://github.com/anton44eg/fixturegen/archive/{0}.tar.gz'
        .format(VERSION),
    license='MIT',
    author='Anton Simernia',
    author_email='anton.simernya@gmail.com',
    keywords=['fixture', 'sqlalchemy', 'testing'],
    description='Fixture generator for fixture module',
    long_description=README,
    package_data={
        'fixturegen': ['templates/*.mako'],
    },
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Topic :: Database',
    ],
    test_suite='test_fixturegen',
    setup_requires=[
        "flake8",
        "nose>=1.0",
        "coverage"
    ]
)
