#!/usr/bin/env python


import os
from setuptools import setup

#def readme():
#    with open('README.txt') as f:
#        return f.read()

setup(name='neutron_pardnet_lbaas',
      version='0.0.1',
      description='pardnet driver for Openstack Neutron LBaaS service',
      long_description='pardnet driver for Openstack Neutron LBaaS service',
      classifiers=[
        'Environment :: OpenStack',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7'
      ],
      keywords=['openstack','pardnet','lbaas'],
      url='https://pypi.python.org/pypi/neutron_pardnet_lbaas',
      author='jaff cheng, pardnet',
      author_email='312973099@qq.com',
      packages=['neutron_pardnet_lbaas'],
      zip_safe=False)

