# -*- coding: utf-8 -*-
"""
energy.py
=========

Free energy related functions.

x_map format
------------

    {
        x1: {
                phase11: [(y111,F111),(y112,F112), ...],
                phase12: [(y121,F121),(y122,F122), ...],
                ...
            },
        x2: {
                phase21: [(y211,F211),(y212,F212), ...],
                phase22: [(y221,F221),(y222,F222), ...],
                ...
            },
        ...
    }

y_map format
------------

    {
        y1: {
                phase11: [(x111,F111),(x112,F112), ...],
                phase12: [(x121,F121),(x122,F122), ...],
                ...
            },
        y2: {
                phase21: [(x211,F211),(x212,F212), ...],
                phase22: [(x221,F221),(x222,F222), ...],
                ...
            },
        ...
    }
"""
import numpy as np

from .utils import save, load
from .utils import find_index, find_index_of_common_elements

__all__ = [
    'get_energy_map',
    'save_energy_map',
    'load_energy_map',
    'get_x_F_list',
    'get_y_F_list',
    'get_F',
]


def get_energy_map(info_map, ret='F', config={}, info_level=-1):
    '''
    F_xmap format
        {
            phase1: {
                        x11: [(y111,F111),(y112,F112), ...],
                        x12: [(y121,F121),(y122,F122), ...],
                        ...
                    },
            phase2: {
                        x21: [(y211,F211),(y212,F212), ...],
                        x22: [(y221,F221),(y222,F222), ...],
                        ...
                    },
            ...
        }
    F_ymap format
        {
            phase1: {
                        y11: [(x111,F111),(x112,F112), ...],
                        y12: [(x121,F121),(x122,F122), ...],
                        ...
                    },
            phase2: {
                        y21: [(x211,F211),(x212,F212), ...],
                        y22: [(x221,F221),(x222,F222), ...],
                        ...
                    },
            ...
        }
    '''
    F_xmap = {}
    F_ymap = {}
    for phase, coord_info_dict in info_map.iteritems():
        x_yF_dict = {}
        y_xF_dict = {}
        for coord, info in coord_info_dict.iteritems():
            if not info.is_valid(config):
                continue
            x, y = coord
            try:
                F = getattr(info, ret)
            except:
                F = info.F  # default is the energy map
            if F is None:
                continue
            if x in x_yF_dict:
                x_yF_dict[x].append((y, F))
            else:
                x_yF_dict[x] = [(y, F)]
            if y in y_xF_dict:
                y_xF_dict[y].append((x, F))
            else:
                y_xF_dict[y] = [(x, F)]
        if info_level > 2:
            print phase
            print x_yF_dict
            print y_xF_dict
        F_xmap[phase] = x_yF_dict
        F_ymap[phase] = y_xF_dict

    x_map = {}
    y_map = {}
    for phase, x_yF_dict in F_xmap.iteritems():
        for x, yF_list in x_yF_dict.iteritems():
            if x in x_map:
                x_map[x].update({phase: yF_list})
            else:
                x_map[x] = {phase: yF_list}
    for phase, y_xF_dict in F_ymap.iteritems():
        for y, xF_list in y_xF_dict.iteritems():
            if y in y_map:
                y_map[y].update({phase: xF_list})
            else:
                y_map[y] = {phase: xF_list}

    return x_map, y_map


def save_energy_map(energy_map, energy_map_file):
    save(energy_map, energy_map_file)


def load_energy_map(energy_map_file):
    return load(energy_map_file)


def get_x_F_list(info_map, phase, yval, base='', xlim=None,
                 config={}, info_level=-1):
    x_map, y_map = get_energy_map(info_map, config=config)
    return get_var_F_list(y_map, phase, yval, base, xlim, info_level)


def get_y_F_list(info_map, phase, xval, base='', ylim=None,
                 config={}, info_level=-1):
    x_map, y_map = get_energy_map(info_map, config=config)
    return get_var_F_list(x_map, phase, xval, base, ylim, info_level)


def get_var_F_list(var_map, phase, val, base='', varlim=None, info_level=-1):
    '''
    Free energy difference use base as the reference state,
    i.e. the energy list returned is
            F_phase - F_base
    '''
    phase_varF_dict = None
    for var, dt in var_map.iteritems():
        if np.isclose(var, val):
            phase_varF_dict = dt

    var_empty = np.array([])
    F_empty = np.array([])
    if phase_varF_dict is None:
        if info_level > 0:
            print 'No data for', val, phase
        return var_empty, F_empty
    if phase not in phase_varF_dict:
        if info_level > 0:
            print 'No data for', phase
        return var_empty, F_empty

    if not base:
        is_diff = False
    elif base in phase_varF_dict:
        is_diff = True
        varF_list = phase_varF_dict[base]
        varF_list.sort()
        var_base = np.array([var for (var, F) in varF_list])
        F_base = np.array([F for (var, F) in varF_list])
    else:
        is_diff = False
        if info_level > 0:
            print base, 'is not used as reference phase.'

    varF_list = phase_varF_dict[phase]
    varF_list.sort()
    var_phase = np.array([var for (var, F) in varF_list])
    F_phase = np.array([F for (var, F) in varF_list])

    if is_diff:
        index1 = find_index_of_common_elements(var_phase, var_base)
        index2 = find_index_of_common_elements(var_base, var_phase)
        if len(index1) == 0 or len(index2) == 0:
            if info_level > 0:
                print 'No common elements among', phase,
                print 'and reference phase', base
            return var_empty, F_empty
        var_phase = var_phase[index1]
        F_phase = F_phase[index1]
        var_base = var_base[index2]
        F_base = F_base[index2]
        i = 0
        j = var_phase.size - 1
        if varlim:
            i, j = find_index(var_phase, varlim)
        if i < 0 or j < 0:
            if info_level > 0:
                print 'No data in range', varlim
            return var_empty, F_empty
        return var_phase[i:j+1], F_phase[i:j+1] - F_base[i:j+1]  # NOQA
    else:
        i = 0
        j = var_phase.size - 1
        if varlim:
            i, j = find_index(var_phase, varlim)
        if i < 0 or j < 0:
            if info_level > 0:
                print 'No data in range', varlim
            return var_empty, F_empty
        return var_phase[i:j+1], F_phase[i:j+1]  # NOQA


def get_F(info_map, coord, phase, ret='F'):
    '''
    Obtain one of Simulation attributes in info_map via coord and phase.
    The default attribute is F.
    If the attribute is not exist, return None.
    '''
    if phase not in info_map:
        return None

    coord_info_dict = info_map[phase]
    if coord not in coord_info_dict:
        return None

    info = coord_info_dict[coord]

    try:
        F = getattr(info, ret)
    except:
        F = None

    return F
