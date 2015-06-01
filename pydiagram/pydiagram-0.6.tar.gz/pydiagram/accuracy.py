# -*- coding: utf-8 -*-
"""
accuracy.py
===========

Accuracy related functions.

x_accuracy_map format
---------------------

    {
        x1: {
                phase11: [(y111,accuracy111),(y112,accuracy112), ...],
                phase12: [(y121,accuracy121),(y122,accuracy122), ...],
                ...
            },
        x2: {
                phase21: [(y211,accuracy211),(y212,accuracy212), ...],
                phase22: [(y221,accuracy221),(y222,accuracy222), ...],
                ...
            },
        ...
    }

y_accuracy_map format
---------------------

    {
        y1: {
                phase11: [(x111,accuracy111),(x112,accuracy112), ...],
                phase12: [(x121,accuracy121),(x122,accuracy122), ...],
                ...
            },
        y2: {
                phase21: [(x211,accuracy211),(x212,accuracy212), ...],
                phase22: [(x221,accuracy221),(x222,accuracy222), ...],
                ...
            },
        ...
    }

"""
from .utils import save, load
from .energy import get_energy_map, get_var_F_list, get_F

__all__ = [
    'get_accuracy_map',
    'save_accuracy_map',
    'load_accuracy_map',
    'get_x_accuracy_list',
    'get_y_accuracy_list',
    'get_accuracy',
]


def get_accuracy_map(info_map, config={}, info_level=-1):
    '''
    accuracy_xmap format
        {
            phase1: {
                        x11: [(y111,accuracy111),(y112,accuracy112), ...],
                        x12: [(y121,accuracy121),(y122,accuracy122), ...],
                        ...
                    },
            phase2: {
                        x21: [(y211,accuracy211),(y212,accuracy212), ...],
                        x22: [(y221,accuracy221),(y222,accuracy222), ...],
                        ...
                    },
            ...
        }
    accuracy_ymap format
        {
            phase1: {
                        y11: [(x111,accuracy111),(x112,accuracy112), ...],
                        y12: [(x121,accuracy121),(x122,accuracy122), ...],
                        ...
                    },
            phase2: {
                        y21: [(x211,accuracy211),(x212,accuracy212), ...],
                        y22: [(x221,accuracy221),(x222,accuracy222), ...],
                        ...
                    },
            ...
        }
    '''
    return get_energy_map(info_map, 'accuracy', config)


def save_accuracy_map(accuracy_map, accuracy_map_file):
    save(accuracy_map, accuracy_map_file)


def load_accuracy_map(accuracy_map_file):
    return load(accuracy_map_file)


def get_x_accuracy_list(info_map, phase, yval, base='', xlim=None, config={}):
    x_accuracy_map, y_accuracy_map = get_accuracy_map(info_map, config)
    return get_var_F_list(y_accuracy_map, phase, yval, base, xlim)


def get_y_accuracy_list(info_map, phase, xval, base='', ylim=None, config={}):
    x_accuracy_map, y_accuracy_map = get_accuracy_map(info_map, config)
    return get_var_F_list(x_accuracy_map, phase, xval, base, ylim)


def get_accuracy(info_map, coord, phase):
    return get_F(info_map, coord, phase, 'accuracy')
