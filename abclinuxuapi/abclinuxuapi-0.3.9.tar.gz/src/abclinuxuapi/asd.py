#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================



# Variables ===================================================================



# Functions & classes =========================================================



# Main program ================================================================
with open("asd.html") as f:
    data = f.read()

from blogpost import Blogpost

b = Blogpost.from_html(data, lazy=False)
