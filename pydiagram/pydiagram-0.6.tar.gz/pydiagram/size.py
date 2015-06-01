# -*- coding: utf-8 -*-
"""
size.py
=======

Cell size related functions.

x_size_map format
-----------------

    {
        x1: {
                phase11: [(y111,a111),(y112,a112), ...],
                phase12: [(y121,a121),(y122,a122), ...],
                ...
            },
        x2: {
                phase21: [(y211,a211),(y212,a212), ...],
                phase22: [(y221,a221),(y222,a222), ...],
                ...
            },
        ...
    }

y_size_map format
-----------------

    {
        y1: {
                phase11: [(x111,a111),(x112,a112), ...],
                phase12: [(x121,a121),(x122,a122), ...],
                ...
            },
        y2: {
                phase21: [(x211,a211),(x212,a212), ...],
                phase22: [(x221,a221),(x222,a222), ...],
                ...
            },
        ...
    }

"""
import numpy as np
from scipy.interpolate import UnivariateSpline

from .utils import save, load
from .energy import get_energy_map, get_var_F_list, get_F
from .settings import TOL_STOP, C_STOP

__all__ = [
    'get_size_map',
    'save_size_map',
    'load_size_map',
    'get_x_a_list',
    'get_y_a_list',
    'get_a_F_list',
    'interp_cell_opt',
    'is_valid_cell_opt',
    'get_a',
    'predict_size'
]


def get_size_map(info_map, config={}, info_level=-1):
    '''
    size_xmap format
        {
            phase1: {
                        x11: [(y111,a111),(y112,a112), ...],
                        x12: [(y121,a121),(y122,a122), ...],
                        ...
                    },
            phase2: {
                        x21: [(y211,a211),(y212,a212), ...],
                        x22: [(y221,a221),(y222,a222), ...],
                        ...
                    },
            ...
        }
    size_ymap format
        {
            phase1: {
                        y11: [(x111,a111),(x112,a112), ...],
                        y12: [(x121,a121),(x122,a122), ...],
                        ...
                    },
            phase2: {
                        y21: [(x211,a211),(x212,a212), ...],
                        y22: [(x221,a221),(x222,a222), ...],
                        ...
                    },
            ...
        }
    '''
    return get_energy_map(info_map, 'a', config)


def save_size_map(size_map, size_map_file):
    save(size_map, size_map_file)


def load_size_map(size_map_file):
    return load(size_map_file)


def get_x_a_list(info_map, phase, yval, base='', xlim=None, config={}):
    x_size_map, y_size_map = get_size_map(info_map, config)
    return get_var_F_list(y_size_map, phase, yval, base, xlim)


def get_y_a_list(info_map, phase, xval, base='', ylim=None, config={}):
    x_size_map, y_size_map = get_size_map(info_map, config)
    return get_var_F_list(x_size_map, phase, xval, base, ylim)


def get_a_F_list(info_map, coord, phase):
    '''
    Return cell optimization data output by Polyorder.
    '''
    a_empty = np.array([])
    F_empty = np.array([])
    if phase not in info_map:
        return a_empty, F_empty

    coord_info_dict = info_map[phase]
    if coord not in coord_info_dict:
        return a_empty, F_empty

    try:
        a_list = np.array(coord_info_dict[coord].a_list)
        F_list = np.array(coord_info_dict[coord].F_list)
    except:
        return a_empty, F_empty

    # remove duplicated elements and sort list in ascending order
    a_list, index = np.unique(a_list, return_index=True)
    F_list = F_list[index]
    return a_list, F_list


def get_a_F_list_old(aF_map, coord, phase):
    '''
    Return cell optimization data output by Polyorder.
    '''
    a_empty = np.array([])
    F_empty = np.array([])
    if phase not in aF_map:
        return a_empty, F_empty

    coord_aF_dict = aF_map[phase]
    if coord not in coord_aF_dict:
        return a_empty, F_empty

    a_list, F_list = coord_aF_dict[coord]
    # remove duplicated elements and sort list in ascending order
    a_list, index = np.unique(a_list, return_index=True)
    F_list = np.array(F_list)[index]
    return a_list, F_list


def interp_cell_opt(x, y, n=100, k=3, s=0):
    if x.size == 0:
        return np.array([]), np.array([])

    if x.size < k:
        k = x.size
    spl = UnivariateSpline(x, y, k=k, s=s)
    xq = np.linspace(x[0], x[-1], n)
    yq = spl(xq)
    # x_min = spl.derivative().roots()
    # y_min = spl(x_min)
    return xq, yq


def is_valid_cell_opt(a, F, tol=TOL_STOP/C_STOP):  # NOQA
    # Convert to numpy ndarray
    a = np.array(a)
    F = np.array(F)
    a, index = np.unique(a, return_index=True)
    F = F[index]

    # There is no cell optimization data
    if a.size == 0:
        return False

    # All cell size should not result in same F
    if np.allclose(F, np.zeros(F.size) + np.mean(F), atol=tol):
        return False

    # There should be one and only one minimum
    # Use 4th order spline since roots() only implemented for 3rd order spline.
    # If spl is 4th order spline, then spl.derivative is a 3rd order spline.
    if a.size <= 4:
        return False
    spl = UnivariateSpline(a, F, k=4, s=0)
    a_min = spl.derivative().roots()
    # F_min = spl(a_min)
    if a_min.size != 1:
        return False

    # Pass all test, the cell optimization is successful
    return True


def get_a(info_map, coord, phase):
    return get_F(info_map, coord, phase, 'a')


def predict_size(info_map, phase, var1, var2_list,
                 xory='y', varlim=None,
                 config={}, info_level=-1):
    '''
    var1: fix the value of an axis
    var2: a list of values of another axis
    For values inside the available size list range:
        do specified interpolatiion
    For values outside the available size list range:
        do linear extrapolatoin
    Return:
        var2_array:  numpy array of var2, which is subset of var2_list
        size_array:  numpy array of predicted sizes corresponding to var2_array
    '''
    if xory.upper() == 'X':
        var_list, a_list = get_x_a_list(info_map, phase, var1,
                                        xlim=varlim, config=config)
    else:
        var_list, a_list = get_y_a_list(info_map, phase, var1,
                                        ylim=varlim, config=config)
    if info_level > 2:
        print var_list
        print a_list

    if var_list.size < 2:
        if info_level > 0:
            print "Require at least 2 points to predict."
            print phase, var1, var2_list, xory, varlim
        return np.array([]), np.array([])

    var2_array = np.sort(np.array(var2_list))  # Sort the input list
    vmin = var_list[0]
    vmax = var_list[-1]

    # Find all values in var2_list that are left outside the range of var_list
    # Do linear extrapolation
    var2_array_left = var2_array[(var2_array < vmin)]
    spl_ext = UnivariateSpline(var_list, a_list, k=1, s=0, ext=0)
    size_array_left = spl_ext(var2_array_left)

    # Find all values in var2_list that are right outside the range of var_list
    # Do linear extrapolation
    var2_array_right = var2_array[(var2_array > vmax)]
    size_array_right = spl_ext(var2_array_right)

    # Find all values in var2_list that are within the range of var_list
    # Do specified interpolation
    var2_array_in = var2_array[(var2_array >= vmin) & (var2_array <= vmax)]
    interp = config.predictor.interpolation
    method = interp.method
    k = interp.k
    s = interp.s
    if var_list.size < k or method.upper() == 'LINEAR':
        # Perform piecewise linear interpolation
        size_array_in = np.interp(var2_array_in, var_list, a_list)
    else:
        # Perform spline interpolation
        spl = UnivariateSpline(var_list, a_list, k=k, s=s)
        size_array_in = spl(var2_array_in)

    var2_array = np.append(var2_array_left, var2_array_in)
    var2_array = np.append(var2_array, var2_array_right)
    size_array = np.append(size_array_left, size_array_in)
    size_array = np.append(size_array, size_array_right)
    return var2_array, size_array
