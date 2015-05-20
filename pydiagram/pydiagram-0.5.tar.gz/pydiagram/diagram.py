# -*- coding: utf-8 -*-
"""
diagram.py
==========

Diagram related functions.
Use Python.pickle for I/O operations.

Folder structure
----------------

The structure of the folder containing SCFT/FTS output data files
    The 1st level folder is for x dimension.
    The pattern of the folder name is
            "xname<xvalue>"
    The 2nd level folder is for y dimension.
    The pattern of the folder name is
            "yname<yvalue>"
    The 3rd level folder is for various phases.
    The pattern of the folder name is
            "phase_name"
    where phase_name is one of pydiagram.settings.PHASE_LIST.

Diagram format
--------------

    {
        phase1: [(x11, y11), (x12, y12), ...],
        phase2: [(x21, y21), (x22, y22), ...],
        ...
    }

Inverse diagram format
----------------------

    {
        (x1,y1): phase,
        (x2,y2): phase,
        (x3,y3): phase,
        ...
    }

info_map format
---------------
    {
        phase1: {
                    (x11, y11): info11,
                    (x12, y12): info12,
                    ...
                },
        phase2: {
                    (x21, y21): info21,
                    (x22, y22): info22,
                    ...
                },
        ...
    }
    where each info# is an instance of the Simulation or its derived class.

aF_map format
-------------
    {
        phase1: {
                    (x11, y11): (a_list11, F_list11),
                    (x12, y12): (a_list12, F_list12),
                    ...
                },
        phase2: {
                    (x21, y21): (a_list21, F_list21),
                    (x22, y22): (a_list22, F_list22),
                    ...
                },
        ...
    }
where a_list and F_list have following format
    [a1, a2, a3, ...]
    [F1, F2, F3, ...]
"""
import os.path

import numpy as np

from .utils import save, load
from settings import *
from .io import parse, list_all_data_dir
from .config import parse_config
from .simulation import PolyFTSSimulation, PolyorderSimulation
from .simulation import interpolate_simulations

__all__ = [
    'get_diagram',
    'get_info_map',
    'get_diagram_from_info_map',
    'update_diagram',
    'update_info_map',
    'refine_diagram',
    'inverse_diagram',
    'verify_diagram',
    'save_diagram',
    'load_diagram',
    'get_diagram_points',
]


def get_diagram(basedir='./', config_file='config.yml', is_parsed=False,
                info_level=-1):
    info_map = get_info_map(basedir, config_file, is_parsed, info_level)

    config = parse_config(config_file)
    return get_diagram_from_info_map(info_map, config, info_level)


def get_info_map(basedir='./', config_file='config.yml', is_parsed=False,
                 info_level=-1):
    if not is_parsed:
        parse(basedir, config_file, info_level)

    config_file = os.path.join(basedir, config_file)
    config = parse_config(config_file)

    solver = config['solver']
    if not solver.upper() in SOLVER_LIST:
        print "Fatal error: solver", solver, 'is not supported. Abort!'
        exit(1)

    if solver.upper() == 'PYDIAGRAM':
        dgmfilename = config.infiles.get('pydiagram', 'phase_diagram.dgm')
        dgmfile = os.path.join(basedir, dgmfilename)
        x, y, info_map = load_dgm(dgmfile, config, info_level)
        if x.upper() != xaxis.upper() or y.upper() != yaxis.upper():
            print 'Fatal error: x and y axes in dgm file:', x, y,
            print 'do not match those in configuration file:', xaxis, yaxis
            print 'Abort!'
            exit(1)
        return info_map

    xaxis = config['xaxis']
    yaxis = config['yaxis']
    strict = config['strict_axis']
    if strict:
        names1 = [xaxis]
        names2 = [yaxis]
    else:
        names1 = [xaxis, yaxis]
        names2 = [xaxis, yaxis]
    data_dirs = list_all_data_dir(basedir, xaxis, yaxis, names1, names2)

    # YAML file contains parsed data
    datafilename = config['outfiles']['point_data']
    info_map = {}
    for datapath, coord in data_dirs.iteritems():
        for phasedir in os.listdir(datapath):
            if phasedir not in PHASE_LIST:
                continue
            datafile = os.path.join(datapath, phasedir, datafilename)
            if not os.path.exists(datafile):
                continue
            if solver.upper() == 'POLYORDER':
                info = PolyorderSimulation()
            elif solver.upper() == 'POLYFTS':
                info = PolyFTSSimulation()
            info.loadfile(datafile)
            coord = tuple(info.get_coord(xaxis, yaxis))
            if info_level > 2:
                print coord, phasedir
                print info.__dict__
            if phasedir in info_map:
                coord_info_dict = info_map[phasedir]
                # Determine whether to override the info
                if coord in coord_info_dict:
                    info_old = coord_info_dict[coord]
                    if info.F is not None:
                        if info_old.F is None:
                            info_map[phasedir][coord] = info
                        elif info.F < info_old.F and info.is_valid(config):
                            info_map[phasedir][coord] = info
                else:
                    info_map[phasedir][coord] = info
            else:
                info_map[phasedir] = {coord: info}
    return info_map


def get_diagram_from_info_map(info_map, config, info_level=-1):
    diagram = {}
    all_phases = info_map.keys()
    for phase, coord_info_dict in info_map.iteritems():
        if info_level > 2:
            print phase
        for coord, info in coord_info_dict.iteritems():
            if info_level > 2:
                print coord
            already_find = False
            for key in diagram.keys():
                if coord in diagram[key]:
                    already_find = True
                    break
            if already_find:
                continue
            if not info.is_valid(config):
                continue
            phase_min = phase
            F_min = info.F
            if info_level > 2:
                print phase_min, F_min
            for phase_tmp in all_phases:
                coord_info_dict_tmp = info_map[phase_tmp]
                if coord in coord_info_dict_tmp:
                    info_tmp = coord_info_dict_tmp[coord]
                    if not info_tmp.is_valid(config):
                        continue
                    F = info_tmp.F
                    if F < F_min:
                        phase_min = phase_tmp
                        F_min = F
                    if info_level > 2:
                        print phase_tmp, F
            if phase_min in diagram:
                if coord not in diagram[phase_min]:
                    diagram[phase_min].append(coord)
            else:
                diagram[phase_min] = [coord]
            if info_level > 2:
                print 'Minimum:', coord, phase_min, F_min
    return diagram


def update_diagram(diagram, diagram_old, info_level=-1):
    '''
    Update old diagram with new one.
    There are two situations:
    1. Items in new diagram are not in old one.
        Add these items into old one.
    2. Items in new diagram are also in old one.
        Update the item values in old one.
    '''
    # Update the diagram
    for phase in diagram:
        if phase not in diagram_old:
            diagram_old[phase] = diagram[phase]
        else:
            for coord in diagram[phase]:
                if coord not in diagram_old[phase]:
                    diagram_old[phase].append(coord)
    return diagram_old


def update_info_map(info_map, info_map_old, info_level=-1):
    '''
    Update old info_map with new one.
    There are two situations:
    1. Items in new info_map are not in old one.
        Add these items into old one.
    2. Items in new info_map are also in old one.
        Update the item values in old one.
    '''
    # Update the info_map
    for phase in info_map:
        if phase not in info_map_old:
            info_map_old[phase] = info_map[phase]
        else:
            for coord in info_map[phase]:
                # always update the info object
                info_map_old[phase][coord] = info_map[phase][coord]
    return info_map_old


def inverse_diagram(diagram):
    '''
    Inverse the phase diagram to the format
            {(x1,y1):phase, (x2,y2):phase, (x3,y3):phase, ...}
    '''
    diagram_inv = {}
    for phase, coord_list in diagram.iteritems():
        for coord in coord_list:
            if coord in diagram_inv:
                return {}  # One coord corresponds to two stable phases
            else:
                diagram_inv[coord] = phase
    return diagram_inv


def verify_diagram(diagram):
    diagram_inv = inverse_diagram(diagram)
    if diagram_inv:
        return True
    else:
        return False


def refine_diagram(boundary, info_map, config, info_level=-1):
    '''
    If config.predictor.boundary is empty, refine the diagram based on all phase boundary points in the boundary object.
    '''
    # Ensure the phase pair key unique
    target_boundary = []
    for boundary_info in config.predictor.boundary:
        for phase_pair in boundary_info.pairs:
            phase1, phase2 = phase_pair
            if phase1 not in PHASE_LIST or phase2 not in PHASE_LIST:
                continue
            if phase1 > phase2:
                target_boundary.append((phase1, phase2))
            else:
                target_boundary.append((phase2, phase1))

    sim_list = []
    for phase_pair, coord_list in boundary.iteritems():
        # Skip phase boundary that not in target boundary
        # if target boundary is not empty
        if (phase_pair not in target_boundary) and target_boundary:
            continue
        if info_level > 2:
            print phase_pair
        for coord in coord_list:
            sim = interpolate_simulations(info_map, phase_pair, coord,
                                          config, info_level)
            if info_level > 2:
                print coord
                for s in sim:
                    print s.__dict__
            sim_list = sim_list + sim
    return sim_list


def get_diagram_points(diagram, phase):
    if phase not in diagram:
        return np.array([]), np.array([])
    coord_list = diagram[phase]
    coord_list.sort()
    x = np.array([xy[0] for xy in coord_list])
    y = np.array([xy[1] for xy in coord_list])
    return x, y


def save_diagram(diagram, diagram_file):
    save(diagram, diagram_file)


def load_diagram(diagram_file):
    return load(diagram_file)
