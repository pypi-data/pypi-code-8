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
        "automate==0.9.1",
        "tornado==4.2"
        ],

    author="Tuomas Airaksinen",
    author_email="tuomas.airaksinen@gmail.com",
    description="WSGI Support for Automate",
    long_description="This extension provides Web server for WSGI-aware extensions, "
                     "such as Remote Procedure Call Support for Automate, Web User Interface for Automate. "
                     "It is of no use alone.",
    license="GPL",
    keywords="automation, GPIO, Raspberry Pi, RPIO, enaml, traits",
    url="http://github.com/tuomas2/automate_webui",
    entry_points={},

    classifiers=["Development Status :: 4 - Beta",
                 "Environment :: Console",
                 "Environment :: Web Environment",
                 "Intended Audience :: Education",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Information Technology",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 "Operating System :: Microsoft :: Windows",
                 "Operating System :: POSIX",
                 "Programming Language :: Python :: 2.7",
                 "Topic :: Scientific/Engineering",
                 "Topic :: Software Development",
                 "Topic :: Software Development :: Libraries"]
)

if __name__ == "__main__":
    setup(**setupopts)
