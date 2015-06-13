# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='PyStormLib',
    version='0.1',
    description='Wrapper around Stormlib',
    author='Fabien Reboia',
    author_email='srounet@gmail.com',
    license = "BSD",
    url = "https://github.com/srounet/pystormlib",
    packages = setuptools.find_packages(),
    package_data = {
        '': ['*.dll'],
    },
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
)
