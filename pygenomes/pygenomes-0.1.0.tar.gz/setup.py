#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys

from setuptools import setup

__version__ = "0.1.0"
__license__ = "MIT"
__author__ = "FEI YUAN"
__contact__ = "fyuan4@uh.edu"
__date__ = "2015-07-07"


setupCommand = sys.argv[-1]


# try converting README from ReST to HTML, if Docutils is installed
# (else issue a warning)

if setupCommand in ("sdist", "build"):
    toolName = "rst2html.py"
    res = os.path.join(os.path.dirname(sys.executable), toolName)
    if os.path.exists(res):
        cmd = "%s '%s' '%s'" % (res, "README.txt", "README.html")
        print "running command %s" % cmd
        cmd = os.system(cmd)
    else:
        res = os.path.join('/usr/local/bin/', toolName)
        if os.path.exists(res):
            cmd = "%s '%s' '%s'" % (res, "README.txt", "README.html")
            print "running command %s" % cmd
            cmd = os.system(cmd)
        else:
            print "Warning: No '%s' found. 'README.{txt|html}'" % toolName,
            print "might be out of synch."


# description for Distutils to do its business

long_description = """\
`pygenomes` (formally named `pygenomes`) is a Python module and also a command-
line tool for downloading genome data from UCSC ftp site. 

Using this tool you can easily check available taxa or available groups of 
taxa by simply typing the name of the tool or add ``-g`` flag with a group 
name. 

Download genome or chromosome data with this tool also very simple. You can 
download data by using commom name, scientific name, or even specific assembly 
name (e.g. ``human``, ``Homo sapiens``, ``hg38``). 

If there is available data in the ftp site, you also can downlaod data via 
interactive mode, which will allow you to choose specific genome assembly.To 
do this, you only need to assign a True value for assembly, then according to 
the available list prompted to you simply input the interested assembly.


Features
--------

- Install a Python module named ``pygenomes.py``
- Install a Python command-line script named ``pygenomes``
- Easily check available taxa and genomes in commend-line
- Simply download genomes via comman, scientific, or assembly name
- Using interactive mode, simply download specific assembly genome
- Easily download genome and chromosome in specific file format
- Pure Python module and without any third-party dependence


Examples
--------

You can use `pygenomes` as a Python module e.g. like in the following
interactive Python session (the function's signature might still change 
a bit in the future)::

    >>> from pygenomes import genomes
    >>>
    # prints out available taxa in group of mammals
    >>> genomes(gname=[group_name])                    # i.e. ['mammals']
    # download human reference genome (hg19) in .2bit format
    >>> genomes(taxa=[taxa])                           # i.e. ['human']
    # interactive mode, ask for inputing and downloading specific assembly
    >>> genomes(taxa=[taxa], assembly=[assembly])      # i.e. ['cow'], ['1']
    # try to download chromosome data, per fa.gz file per chromosome
    >>> genomes(taxa=[taxa], chrs=[format])            # i.e. ['cow'], ['1']

In addition there is a script named ``pygenomes``, which can be used 
more easily from the system command-line like this (you can see many 
more examples when typing ``pygenomes -h`` on the command-line)::

    $ pygenomes -g -1                 # prints out all available taxa

    $ pygenomes -g mammal             # prints out all available taxa in group 
                                        of mammal
    $ pygenomes -t yeast              # download yeast reference genome in 
                                        .2bit format
    $ pygenomes -t yeast -a 1         # interactive mode, ask for inputing and 
                                        downloading specific assembly
    $ pygenomes -t cow -f fa.gz       # try to download cow reference genome 
                                        in fa.gz format
    $ pygenomes -t dog -a 1 -o /tmp   # interactive mode, ask for inputing, 
                                        file will be stored in /tmp
    $ pygenomes -t cat -c 1           # download cat chromosome data, per 
                                        chromosome per fa.gz file
"""


classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Topic :: Utilities",
]

baseURL = "https://github.com/TinyNecessaryTools/Biology"

setup(
    name = "pygenomes",
    version = __version__,
    description = "a command-line tool for downloading genome data from UCSC ftp site.",
    long_description = long_description,
    author = __author__,
    author_email = __contact__,
    maintainer = __author__,
    maintainer_email = __contact__,
    license = __license__,
    platforms = ["Posix", "Windows"],
    keywords = ["genome", "download", "ucsc", 'bioinformatic', 'biology'],
    url = baseURL,
    download_url = baseURL + "/pygenomes/dist/pygenomes-%s.tar.gz" % __version__,
    py_modules = ["pygenomes"],
    # scripts = ["pygenomes"],
    entry_points = {
        "console_scripts" : ["pygenomes = pygenomes:main"]
    },
    classifiers = classifiers,
    zip_safe = False,

    # for setuptools, only
    install_requires = [],
)
