# -*- coding: utf-8 -*-
"""
separation.py
=============

Separation structure related functions.

x_separation_map format
-----------------------

    {
        x1: {
                phase11: [(y111,separation111),(y112,separation112), ...],
                phase12: [(y121,separation121),(y122,separation122), ...],
                ...
            },
        x2: {
                phase21: [(y211,separation211),(y212,separation212), ...],
                phase22: [(y221,separation221),(y222,separation222), ...],
                ...
            },
        ...
    }

y_size_map format
-----------------

    {
        y1: {
                phase11: [(x111,separation111),(x112,separation112), ...],
                phase12: [(x121,separation121),(x122,separation122), ...],
                ...
            },
        y2: {
                phase21: [(x211,separation211),(x212,separation212), ...],
                phase22: [(x221,separation221),(x222,separation222), ...],
                ...
            },
        ...
    }

"""
from .utils import save, load
from .energy import get_energy_map, get_var_F_list, get_F

__all__ = [
    'get_separation_map',
    'save_separation_map',
    'load_separation_map',
    'get_x_separation_list',
    'get_y_separation_list',
    'get_separation',
]


def get_separation_map(info_map, config={}, info_level=-1):
    '''
    separation_xmap format
        {
            phase1: {
                        x11: [(y111,separation111),(y112,separation112), ...],
                        x12: [(y121,separation121),(y122,separation122), ...],
                        ...
                    },
            phase2: {
                        x21: [(y211,separation211),(y212,separation212), ...],
                        x22: [(y221,separation221),(y222,separation222), ...],
                        ...
                    },
            ...
        }
    separation_ymap format
        {
            phase1: {
                        y11: [(x111,separation111),(x112,separation112), ...],
                        y12: [(x121,separation121),(x122,separation122), ...],
                        ...
                    },
            phase2: {
                        y21: [(x211,separation211),(x212,separation212), ...],
                        y22: [(x221,separation221),(x222,separation222), ...],
                        ...
                    },
            ...
        }
    '''
    return get_energy_map(info_map, 'separated', config)


def save_separation_map(separation_map, separation_map_file):
    save(separation_map, separation_map_file)


def load_separation_map(separation_map_file):
    return load(separation_map_file)


def get_x_separation_list(info_map, phase, yval, base='',
                          xlim=None, config={}):
    x_separation_map, y_separation_map = get_separation_map(info_map, config)
    return get_var_F_list(y_separation_map, phase, yval, base, xlim)


def get_y_separation_list(info_map, phase, xval, base='',
                          ylim=None, config={}):
    x_separation_map, y_separation_map = get_separation_map(info_map, config)
    return get_var_F_list(x_separation_map, phase, xval, base, ylim)


def get_separation(info_map, coord, phase):
    separation = get_F(info_map, coord, phase, 'separated')
    if separation is None:
        return False
    else:
        return separation
