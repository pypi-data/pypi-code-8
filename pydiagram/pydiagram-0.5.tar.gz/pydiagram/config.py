# -*- coding: utf-8 -*-
"""
config.py
=========

This module dedicates to provide a consitent interface to access the project
configurations. The project configurations should be read from a YAML file
located in the top level project directory.

Here the word "project" means a task to create a phase diagram
by running a bunch of SCFT/FTS simulations.
"""
import os.path

import numpy as np
import yaml
from attrdict import AttrDict

from .settings import *


__all__ = [
    'parse_config',
    'parse_config_predictor_manual',
]


def parse_config(config_file, info_level=-1):
    '''Store configurations as an AttrDict instance
    The configuration instance is built in the following order:
        1. Initialize to empty AttrDict
        2. Read in default configuration file
        3. Override default configurations with user specified ones
    Note:
        1. The .plot.boundary section should be left empty in the default file. This section is designed to contain a full list of dicts, each of them describes how to plot a certain phase boundary. By default, we do not know any phase boundaries in advance. Thus, it is reasonable to leave it blank. And it also ease the integration of user's configurations.
    '''
    config = AttrDict({})
    # Read in the default configurations first
    root_path = os.path.abspath(os.path.dirname(__file__))
    default_file = os.path.join(root_path, '../config.yml')
    with open(default_file, 'r') as f:
        config = AttrDict(yaml.safe_load(f))
    # Read in the user specified configurations
    if not os.path.exists(config_file):
        return config
    with open(config_file, 'r') as f:
        try:
            config_user = AttrDict(yaml.safe_load(f))
        except:
            return config
    # Merge and return the final config object
    # AttrDict performs right-favored merging
    return config + config_user


def parse_config_old(config_file, info_level=-1):
    '''
    configuration file should in YAML format.
    Return a Python dict.
    Note:
        This function is obsolete.
    '''
    if not os.path.exists(config_file):
        return {}

    with open(config_file, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except:
            config = {}

    return config


def parse_config_predictor_manual(config):
    '''
    phase_coordlist_dict1 is for order == True
    phase_coordlist_dict2 is for order == False
    '''
    phase_coordlist_dict1 = {}
    phase_coordlist_dict2 = {}
    for sim in config.predictor.manual:
        grid = sim.get('grid', True)
        if grid:
            X, Y = np.meshgrid(sim.x, sim.y)
            coord_list = zip(X.flatten(), Y.flatten())
        else:
            if len(sim.x) == len(sim.y):
                coord_list = zip(sim.x, sim.y)
            else:
                coord_list = []
        order = sim.get('order', True)
        for phase in sim.phases:
            if order:
                if phase in phase_coordlist_dict1:
                    phase_coordlist_dict1[phase] += coord_list
                else:
                    phase_coordlist_dict1[phase] = coord_list[:]
            else:
                if phase in phase_coordlist_dict2:
                    phase_coordlist_dict2[phase] += coord_list
                else:
                    phase_coordlist_dict2[phase] = coord_list[:]

    return phase_coordlist_dict1, phase_coordlist_dict2

