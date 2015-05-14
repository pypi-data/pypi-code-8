#!/usr/bin/env python

from setuptools import setup


import setuptools

setuptools.setup(
	name='musashi.openstack_backports',
	packages=['musashi.cinder.extensions', 'musashi.cinder', 'musashi'],
	version="0.0.4",
	author="Stephen Paul Suarez",
	author_email="ssuarez@musashi.ph",
	url="https://github.com/musashi-dev/musashi.openstack_backports"
)
