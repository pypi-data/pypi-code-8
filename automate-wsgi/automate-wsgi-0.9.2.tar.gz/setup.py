#!/usr/bin/env python

from setuptools import setup, find_packages

def get_version(filename):
    import re
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']

setupopts = dict(
    name="automate-wsgi",
    version=get_version('automate_wsgi/__init__.py'),
    packages=find_packages(),

    install_requires=[
        "automate>=0.9.2,<0.10",
        "tornado==4.2"
        ],

    author="Tuomas Airaksinen",
    author_email="tuomas.airaksinen@gmail.com",
    description="WSGI Support for Automate",
    long_description=open('README.rst').read(),
    download_url='https://pypi.python.org/pypi/automate-wsgi',
    platforms = ['any'],
    license="GPL",
    keywords="automation, GPIO, Raspberry Pi, RPIO, enaml, traits",
    url="http://github.com/tuomas2/automate-wsgi",
    entry_points={},

    classifiers=["Development Status :: 4 - Beta",
                 "Environment :: Console",
                 "Framework :: Django :: 1.8",
                 "Environment :: Web Environment",
                 "Intended Audience :: Education",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Information Technology",
                 "Intended Audience :: End Users/Desktop",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 "Operating System :: Microsoft :: Windows",
                 "Operating System :: POSIX",
                 "Operating System :: POSIX :: Linux",
                 "Programming Language :: Python :: 2.7",
                 "Topic :: Scientific/Engineering",
                 "Topic :: Software Development",
                 "Topic :: Software Development :: Libraries"]
)

if __name__ == "__main__":
    setup(**setupopts)
