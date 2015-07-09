#!/usr/bin/env python

from distutils.core import setup

setup(name='SmartDrive',
    version='1.2',
    description='OpenElectrons SmartDrive library',
    author='openelectrons.com',
    author_email='contact@openelectrons.com',
    url='http://www.openelectrons.com/index.php?module=documents&JAS_DocumentManager_op=viewDocument&JAS_Document_id=8',
    py_modules=['SmartDrive'],
    install_requires=['OpenElectrons_i2c'],
    )