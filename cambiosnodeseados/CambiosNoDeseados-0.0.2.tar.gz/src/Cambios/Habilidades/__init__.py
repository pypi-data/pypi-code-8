#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from glob import glob

c = path.abspath(path.dirname(__file__))
archivos = glob(path.join(c, '*.py'))

__all__ = [modulo[len(c)+1:-3] for modulo in archivos if not modulo == path.join(c, __file__)]
