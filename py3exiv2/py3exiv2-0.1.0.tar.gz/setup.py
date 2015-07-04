#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import glob
import subprocess

from setuptools import setup, find_packages, Extension
from setuptools.command.install import install as _install

from codecs import open
from os import path

def get_libboost_name():
    """Returns the name of the lib libboost_python 3

    """
    # libboost libs are provided without .pc files, so we can't use pkg-config
    places = ('/usr/lib/', '/usr/local/lib/', '/usr/')
    for place in places:
        cmd = ['find', place, '-name', 'libboost_python*']
        rep = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        if not rep:
            continue

        # rep is type bytes
        libs = rep.decode(sys.getfilesystemencoding()).split('\n')
        for l in libs:
            _, l = os.path.split(l)
            if '.so' in l:
                l = l.split('.so')[0]
                # Assume there's no longer python2.3 in the wild
                if '3' in l[2:]:
                    return l.replace('libboost', 'lboost')

def make_build_dir():
    """Create or clean the build dir.

    """
    if not os.path.isdir('build'):
        os.mkdir('build')

    else:
        for f in ('build/exiv2wrapper.so', 'exiv2wrapper_python',
                  'build/libexiv2python.so'):
            try:
                os.unlink(f)
            except:
                pass

def write_build_file(dct):
    """Write the script build.sh

    """
    dct['wrp'] = 'exiv2wrapper'
    dct['wrpy'] = 'exiv2wrapper_python'
    dct['flags'] = '-c -fPIC'
    txt = """#!/bin/sh

g++ -o build/%(wrp)s.os %(flags)s -I%(py)s src/%(wrp)s.cpp
g++ -o build/%(wrpy)s.os %(flags)s -I%(py)s src/%(wrpy)s.cpp
g++ -o build/libexiv2python.so -shared build/%(wrp)s.os build/%(wrpy)s.os -%(boost)s -lexiv2

echo "install libexiv2python.so to %(dist)s"
cp build/libexiv2python.so %(dist)s/libexiv2python.so
test -d %(pyexiv)s || mkdir -p %(pyexiv)s
cp src/pyexiv2/__init__.py %(pyexiv)s/__init__.py
cp src/pyexiv2/exif.py %(pyexiv)s/exif.py
cp src/pyexiv2/iptc.py %(pyexiv)s/iptc.py
cp src/pyexiv2/metadata.py %(pyexiv)s/metadata.py
cp src/pyexiv2/preview.py %(pyexiv)s/preview.py
cp src/pyexiv2/utils.py %(pyexiv)s/utils.py
cp src/pyexiv2/xmp.py %(pyexiv)s/xmp.py
""" % dct

    with open('build.sh', 'w') as outf:
        outf.write(txt)

    os.system("chmod +x build.sh")

def main(arg):
    import os, sys, subprocess
    from distutils.sysconfig import get_python_inc, get_python_lib
    dct = {}
    dct['boost'] = get_libboost_name()
    if dct['boost'] is None:
        raise OSError("Can't find libboost_python-3")
        sys.exit()

    dct['py'] = get_python_inc()
    dct['dist'] = get_python_lib()
    dct['pyexiv'] = dct['dist'] + '/pyexiv2'
    make_build_dir()
    write_build_file(dct)
    subprocess.call('./build.sh')

class install(_install):
    def run(self):
        _install.run(self)
        self.execute(main, (self.install_lib,),
                     msg="Build the Python wrapper")

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py3exiv2',
    version='0.1.0',
    description='A Python3 binding to the library exiv2',
    long_description=long_description,
    url='https://launchpad.net/py3exiv2',
    author='Vincent Vande Vyvre',
    author_email='vincent.vandevyvre@oqapy.eu',
    license='GPL-3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='exiv2 pyexiv2 EXIF IPTC XMP image metadata',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    package_data={'':['src/*.cpp', 'src/*.hpp',]},
    cmdclass={'install': install}
)

