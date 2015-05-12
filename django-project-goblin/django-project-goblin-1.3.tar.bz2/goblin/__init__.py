#!/usr/bin/env python
import sys,os

from goblin import logger_setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(BASE_DIR, '..')
sys.path.insert(0, BASE_DIR)

from logger_setup import LOGGING