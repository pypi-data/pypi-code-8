#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
from .generator import Generator


class Argument(object):
    """
        We will catch command line arguments here.
    """

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--length', help="Key Length", default=8)
        # Can be all, lower, upper, digit, alpha
        parser.add_argument('-t', '--types', help="Char types. lower,upper, digit or alpha", default='all')
        parser.add_argument('-c', '--count', help="Count", default=1)
        parser.add_argument('-v', '--version', action="version", help="Version", version='%s' % Generator.VERSION)
        parser.add_argument('-p', '--prefix', help="Prefix")
        parser.add_argument('-s', '--suffix', help="Suffix")
        self.args = parser.parse_args()
