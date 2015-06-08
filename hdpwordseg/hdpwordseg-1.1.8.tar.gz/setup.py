#!/usr/bin/env pypy
#-*- coding: utf-8 -*-

from distutils.core import setup

import hdp.hdpwordseg

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["examples/*.cfg", "examples/*.txt"]

setup(name = "hdpwordseg",
    version = hdp.hdpwordseg.version(),
    description = 'HDP Word Segmentor',
    author = "Prachya Boonkwan",
    author_email = "kaamanita@gmail.com",
    url = "https://bitbucket.org/kaamanita/hdpwordseg",

    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['hdp'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...

    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'hdp' : files },

    #'runner' is in the root.
    scripts = ["hdpwordseg"],

    long_description = 'Word segmentation module based on Hierarchical \
    Dirichlet Processes (Goldwater\'s PhD thesis, 2007; \
    Mochihashi et al., ACL 2009). This implementation is developed \
    by Prachya Boonkwan, National Electronics and Computer Technology \
    Center (NECTEC), Thailand. (C) April 2015. All right reserved.',
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #Cf. https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities'
    ]     
) 
