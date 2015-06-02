#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup

import sample

setup(
    name='VoiceCom-Sample',
    version=sample.__version__,
    description='Some sample plugin.',
    # packages=['sample'], TODO: Required?
    entry_points={'voicecom.plugins': 'sample = sample'},
)
