#!/bin/env python
# -*- coding: utf-8 -*-

import os

here = os.path.abspath(os.path.dirname(__file__))
dockerfly_version = open(os.path.join(here, 'version.txt')).read().strip()

#database
RUN_ROOT= '/var/dockerfly'
LOG_ROOT = os.path.join(RUN_ROOT, 'log')
DB_ROOT  = os.path.join(RUN_ROOT, 'db')

default_container_db = os.path.join(DB_ROOT, 'containers.json')
default_ippool_db = os.path.join(DB_ROOT, 'ippool.json')
dbs = [default_container_db, default_ippool_db]
