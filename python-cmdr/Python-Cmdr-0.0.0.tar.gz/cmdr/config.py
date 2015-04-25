#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from easyconfig import Config, yaml_mapping

# Initialize config
config = Config({
    'COMMANDS_PATH': '',
    'ENTRY_POINT': 'main',
})

# Override config
yaml_filename = os.environ.get('CMDR_CONFIG_YAML')
if yaml_filename:
    config.from_mapping(yaml_mapping(yaml_filename))

# Validate config
if not config.COMMANDS_PATH:
    raise RuntimeError('Configuration `COMMANDS_PATH` is empty')
if not config.ENTRY_POINT:
    raise RuntimeError('Configuration `ENTRY_POINT` is empty')
