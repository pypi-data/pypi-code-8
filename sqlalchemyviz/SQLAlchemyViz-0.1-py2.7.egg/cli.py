# -*- coding: utf-8 -*-
# Copyright (C) 2015 Sebastian Eckweiler
#
# This module is part of SQLAlchemyViz and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
from __future__ import unicode_literals

import argparse
import os
import sys

import pydot

from .viz import dump_diagram

def get_metadata(path):
    """
    Import metadata from the specified path.

    :param str path: String specifying from where the
                     metadata should be imported.
    :return: The sqlalchemy metadata instance.
    """
    mod_name, attr_name = path.split(':', 1)
    attr_name = str(attr_name)

    sys.path.append(os.path.curdir)
    module = __import__(mod_name, {}, {}, [attr_name])

    for attr_name in attr_name.split('.'):
        attr = getattr(module, attr_name)
    return attr


def set_graphviz_location(path):
    """
    Specify the graphviz executables folder.

    :param str path: Sets the path where pydot
                     looks for the graphviz executables.
    """
    # pick graphviz from the specified folder
    pydot.find_graphviz = lambda: pydot.__find_executables(path)


def main():
    parser = argparse.ArgumentParser('sqlaviz',
        description='Create an ER diagram from a sqlalchemy schema object.'
    )

    parser.add_argument('metadata', metavar='pkg.module:metadata', type=str,
                        help='Import path for the metadata identifier.')
    parser.add_argument('-f', '--file', type=str,
                        default='diagram.pdf',
                        help='Write diagram to specified file {default: diagram.pdf}.')
    parser.add_argument('-p', '--prog', type=str, metavar='PROG',
                        default='neato', choices=['dot', 'twopi', 'neato', 'circo', 'fdp'],
                        help=('Name of the graphviz layout program to use {default: "neato"}. Other choices are: '
                              '"dot", "twopi", "circo" or "fdp".'))
    parser.add_argument('-o', '--opt', metavar='OPTION',
                        type=str, action='append', default=[],
                        help='Where OPTION is e.g. "graph_bgcolor=red". May be supplied multiple times.')
    parser.add_argument('--sort-columns', action='store_true', default=False,
                        help='Sort columns alphabetically.')
    parser.add_argument('-g', '--graphviz', metavar='GRAPHVIZ_PATH', type=str,
                        help='Path to folder containing the graphviz executables.')

    kwargs = dict(parser.parse_args()._get_kwargs())

    graphviz = kwargs.pop('graphviz')
    if graphviz:
        set_graphviz_location(graphviz)

    dump_diagram(meta=get_metadata(kwargs.pop('metadata')),
                 diagram_opts=dict(x.split('=', 1) for x in kwargs.pop('opt')),
                 path=kwargs.pop('file'),
                 prog=kwargs.pop('prog'),
                 **kwargs)