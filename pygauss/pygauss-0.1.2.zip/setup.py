# -*- coding: utf-8 -*-
"""
Created on Thu May 07 14:34:45 2015

@author: chris
"""
#!/usr/bin/env python

from distutils.core import setup

import os
def readme(img_path):
    if os.path.exists('README.rst'):
        descript = open('README.rst').read()
        descript = descript.replace('image:: ', 
                                    'image:: {0}raw/master/'.format(img_path))
        return descript
    return ''

setup(name='pygauss',
      version='0.1.2',
      description='PYthon GAUSSian DFT output analysis',
      long_description=readme('https://github.com/chrisjsewell/PyGauss/'),
      author='Chris Sewell',
      author_email='chrisj_sewell@hotmail.com',
      url='https://github.com/chrisjsewell/PyGauss',
      platforms = ["Any."],
      packages=['pygauss', 
                'pygauss.cclib_patch','pygauss.cclib_patch.parser', 
                'pygauss.chemlab_patch',
                'pygauss.chemlab_patch.graphics', 
                'pygauss.chemlab_patch.graphics.renderers',
                'pygauss.chemlab_patch.io','pygauss.chemlab_patch.io.handlers',
                'pygauss.chemview_patch',
                'pygauss.test_data'],
      package_data={'': ['*.rst', '*.txt'],
                    'pygauss.test_data': ['*.log', '*.com']}
                
     )