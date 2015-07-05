#!/usr/bin/env python

from setuptools import setup, find_packages
from pip.req import parse_requirements
install_reqs = parse_requirements('requirements.pip')

def get_version(filename):
    import re
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']

setupopts = dict(
    name="automate-rpc",
    version=get_version('automate_rpc/__init__.py'),
    packages=find_packages(),

    install_requires=[str(ir.req) for ir in install_reqs],

    author="Tuomas Airaksinen",
    author_email="tuomas.airaksinen@gmail.com",
    description="Remote Procedure Call Support for Automate",
    long_description="This Automate extension provides XmlRPC API for external application",
    license="GPL",
    keywords="automation, GPIO, Raspberry Pi, RPIO, traits",
    url="http://github.com/tuomas2/automate_webui",
    entry_points={'automate.extension': [
            'rpc = automate_rpc:extension_classes'
    ]},

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
