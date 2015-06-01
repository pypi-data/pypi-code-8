# -*- coding: utf-8 -*-
"""
boundary.py
===========

Phase boundary related functions.

boundary format
---------------

    {
        (phase11, phase12): [(x11, y11), (x12, y12), ...],
        (phase21, phase22): [(x21, y21), (x22, y22), ...],
        ...
    }
where for each (phase1, phase2) pair, the order of these two phases is ensured
to be
        phase1 > phase2
"""
from pprint import pprint
from operator import itemgetter
import numpy as np
from scipy.interpolate import UnivariateSpline

from .diagram import inverse_diagram
from .energy import get_energy_map
from .utils import find_index, find_index_of_common_elements
from .utils import save, load

__all__ = [
    'get_boundary',
    'get_ODT_boundary',
    'get_OOT_boundary',
    'get_connected_boundary',
    'get_boundary_point_along_x',
    'get_boundary_point_along_y',
    'get_boundary_point',
    'merge_boundary',
    'interpolate_boundary',
    'save_boundary',
    'load_boundary',
]


def get_ODT_boundary(boundary, sort_axis='x'):
    ODT_boundary = []
    for phase_pair, coord_list in boundary.iteritems():
        phase1, phase2 = phase_pair
        if phase1 == 'DIS' or phase2 == 'DIS':
            ODT_boundary += coord_list
    if len(ODT_boundary) == 0:
        return (np.array([]), np.array([]))
    if sort_axis == 'x':
        ODT_boundary.sort()
    else:
        ODT_boundary = sorted(ODT_boundary, key=itemgetter(1))
    xs = np.array([x for (x, y) in ODT_boundary])
    ys = np.array([y for (x, y) in ODT_boundary])
    return (xs, ys)


def get_OOT_boundary(boundary, phase1, phase2, sort_axis='x'):
    if phase1 > phase2:
        key = (phase1, phase2)
    else:
        key = (phase2, phase1)
    if key in boundary:
        OOT_boundary = boundary[key]
    else:
        return (np.array([]), np.array([]))
    if sort_axis == 'x':
        OOT_boundary.sort()
    else:
        OOT_boundary = sorted(OOT_boundary, key=itemgetter(1))
    xs = np.array([x for (x, y) in OOT_boundary])
    ys = np.array([y for (x, y) in OOT_boundary])
    return (xs, ys)


def get_connected_boundary(boundary, phase_pair_list, sort_axis='x'):
    connected_boundary = []
    for phase1, phase2 in phase_pair_list:
        if phase1 > phase2:
            key = (phase1, phase2)
        else:
            key = (phase2, phase1)
        if key in boundary:
            connected_boundary += boundary[key]
    if len(connected_boundary) == 0:
        return (np.array([]), np.array([]))
    if sort_axis == 'x':
        connected_boundary.sort()
    else:
        connected_boundary = sorted(connected_boundary, key=itemgetter(1))
    xs = np.array([x for (x, y) in connected_boundary])
    ys = np.array([y for (x, y) in connected_boundary])
    return (xs, ys)


def merge_boundary(boundary1, boundary2):
    '''
    Merge all contents in boundary2 into boundary1 and return it.
    '''
    for key in boundary2:
        if key in boundary1:
            boundary1[key] = boundary1[key] + boundary2[key]
        else:
            boundary1[key] = boundary2[key]

    return boundary1


def get_boundary(diagram, info_map, alongx=True, alongy=True,
                 config={}, info_level=-1):
    boundary = {}
    diagram_inv = inverse_diagram(diagram)
    x_map, y_map = get_energy_map(info_map, config=config,
                                  info_level=info_level)

    # find the phase boundary along y direction (keeping x fixed)
    if alongy:
        for x, phase_yF_dict in x_map.iteritems():
            boundary_y = get_boundary_point_along_y(diagram_inv, phase_yF_dict,
                                                    x, info_level)
            if info_level > 2:
                print "Boundary along y for x =", x
                pprint(boundary_y)
            boundary = merge_boundary(boundary, boundary_y)

    # find the phase boundary along y direction (keeping x fixed)
    if alongx:
        for y, phase_xF_dict in y_map.iteritems():
            boundary_x = get_boundary_point_along_x(diagram_inv, phase_xF_dict,
                                                    y, info_level)
            if info_level > 2:
                print "Boundary along x for y =", y
                pprint(boundary_x)
            boundary = merge_boundary(boundary, boundary_x)

    return boundary


def get_boundary_point_along_line(diagram_inv, phase_var1F_dict, var2,
                                  xory='x', info_level=-1):
    boundary = {}
    if xory.upper() == 'X':
        alongx = True
    else:
        alongx = False

    if info_level > 1:
        print 'var2 =', var2

    # format: [(var1_1, phase), (var1_2, phase), (var1_3, phase)]
    var1_phase_list = []
    for coord, phase in diagram_inv.iteritems():
        x0, y0 = coord
        if alongx:
            if np.allclose(var2, y0):
                var1_phase_list.append((x0, phase))
        else:
            if np.allclose(var2, x0):
                var1_phase_list.append((y0, phase))
    var1_phase_list.sort()  # x in ascending order
    if len(var1_phase_list) == 0:
        return boundary
    if info_level > 2:
        print 'var1_phase_list =', var1_phase_list

    var11, phase1 = var1_phase_list[0]
    for (var1, phase) in var1_phase_list:
        if phase != phase1:
            var12 = var1
            phase2 = phase
            if info_level > 2:
                print phase1, var11, phase2, var12
                print 'phase_var1F_dict =', phase_var1F_dict
            var1b = get_boundary_point(phase_var1F_dict,
                                       phase1, phase2, var11, var12,
                                       info_level)
            if var1b is None:
                if info_level > 0:
                    print 'No boundary detected for (',
                    print var2, phase1, phase2, var11, var12, ')'
                # var1b = 0.5 * (var11 + var12)
                var11 = var12
                phase1 = phase2
                continue
            if var1b < 0:
                if info_level > 0:
                    print 'Negative boundary detected for (',
                    print var2, phase1, phase2, var11, var12, ')'
                var11 = var12
                phase1 = phase2
                continue

            if phase1 > phase2:
                if (phase1, phase2) in boundary:
                    if alongx:
                        boundary[(phase1, phase2)].append((var1b, var2))
                    else:
                        boundary[(phase1, phase2)].append((var2, var1b))
                else:
                    if alongx:
                        boundary[(phase1, phase2)] = [(var1b, var2)]
                    else:
                        boundary[(phase1, phase2)] = [(var2, var1b)]
            else:
                if (phase2, phase1) in boundary:
                    if alongx:
                        boundary[(phase2, phase1)].append((var1b, var2))
                    else:
                        boundary[(phase2, phase1)].append((var2, var1b))
                else:
                    if alongx:
                        boundary[(phase2, phase1)] = [(var1b, var2)]
                    else:
                        boundary[(phase2, phase1)] = [(var2, var1b)]
            var11 = var12
            phase1 = phase2
        else:
            var11 = var1
            phase1 = phase  # this line can be removed

    return boundary


def get_boundary_point_along_x(diagram_inv, phase_xF_dict, y,
                               info_level=-1):
    return get_boundary_point_along_line(diagram_inv, phase_xF_dict, y,
                                         'x', info_level)


def get_boundary_point_along_y(diagram_inv, phase_yF_dict, x,
                               info_level=-1):
    return get_boundary_point_along_line(diagram_inv, phase_yF_dict, x,
                                         'y', info_level)


def get_boundary_point(phase_varF_dict, phase1, phase2, var1, var2,
                       info_level=-1):
    '''
    Return a phase boundary point (in x or y dimension) between phase1 and phase2.
    If the phase boundary is the ODT, we need to
    approximate the phase boundary point by extrapolating the free energy of the most stable ordered phase to match the free energy of the DIS phase.
    Otherwise (for OOT), use the phase1 and phase2 provided and find the boundary point by interpolating the free energy difference between phase1 and phase2 to be 0.
    '''
    if phase1 not in phase_varF_dict:
        if info_level > -1:
            print 'Warning: phase1 (' + phase1 + ') not in phase_varF_dict.'
        return None
    if phase2 not in phase_varF_dict:
        if info_level > -1:
            print 'Warning: phase2 (' + phase2 + ') not in phase_varF_dict.'
        return None
    if var1 > var2:
        if info_level > -1:
            print 'Waring: require var1 < var2 in get_boundary_point.'
        return None

    # Sort F and var lists for each phase
    varF1_list = phase_varF_dict[phase1]
    varF1_list.sort()
    var1_list = np.array([var for (var, F) in varF1_list])
    F1_list = np.array([F for (var, F) in varF1_list])
    varF2_list = phase_varF_dict[phase2]
    varF2_list.sort()
    var2_list = np.array([var for (var, F) in varF2_list])
    F2_list = np.array([F for (var, F) in varF2_list])

    if info_level > 2:
        print 'F vs var for phase', phase1
        print varF1_list
        print 'F vs var for phase', phase2
        print varF2_list

    # Find common data points between phase1 and phase2
    index1 = find_index_of_common_elements(var1_list, var2_list)
    index2 = find_index_of_common_elements(var2_list, var1_list)
    if index1.size == 0 or index2.size == 0:
        return None
    var1_list = var1_list[index1]
    F1_list = F1_list[index1]
    var2_list = var2_list[index2]
    F2_list = F2_list[index2]

    if info_level > 2:
        print 'Common F and var list for phase', phase1
        print var1_list
        print F1_list
        print 'Common F and var list for phase', phase2
        print var2_list
        print F2_list

    # Find the neighboring points that enclose the boundary point
    # Note when phase is DIS, var1_list and var2_list may have only one item.
    # In such case, find_index can still return [0, 0] as expected.
    # Example:
    #       phase1 = DIS, phase2 = HEX
    #       var1_list = [24.0]
    #       var1 = 20.0, var2 = 24.0
    # This gives i = 0, and j = 0.
    i, j = find_index(var1_list, (var1, var2))
    if i is None or j is None:
        return None
    # reference phase is DIS if phase1 or phase2 is 'DIS'
    # otherwise, reference phase is phase1
    if phase1 == 'DIS':
        dF_list = F2_list - F1_list
        if j + 2 > dF_list.size:
            # insufficient non DIS phase data,
            # approximate the boundary point in the middle of
            # the transition gap
            return 0.5 * (var1 + var2)
        else:
            k, b = np.polyfit(var1_list[j:j+2], dF_list[j:j+2], 1)  # NOQA
            varb = -b / k
    elif phase2 == 'DIS':
        dF_list = F1_list - F2_list
        if j + 2 > dF_list.size:
            return 0.5 * (var1 + var2)
        else:
            k, b = np.polyfit(var1_list[j:j+2], dF_list[j:j+2], 1)  # NOQA
            varb = -b / k
    else:
        dF_list = F2_list - F1_list
        if i + 2 > dF_list.size:
            return None
        else:
            k, b = np.polyfit(var1_list[i:i+2], dF_list[i:i+2], 1)  # NOQA
            varb = -b / k

    return varb


def interpolate_boundary(x, y, n=30, k=1, s=0, method='range'):
    '''
    algorithm adapted from: http://stackoverflow.com/questions/14344099/smooth-spline-representation-of-an-arbitrary-contour-flength-x-y

    :param n: number of interpolation points.
    :param method: one of 'standard', 'range', or 'distant'.
    '''
    x = np.array(x)
    y = np.array(y)
    if x.size == 0 or y.size == 0 or x.size != y.size:
        return x, y

    # remove duplicated elements and sort list in ascending order
    x, index = np.unique(x, return_index=True)
    y = np.array(y)[index]
    if x.size < 2:
        return x, y
    if x.size < k + 1:
        k = x.size - 1

    if method == 'distant':
        t = np.zeros(x.shape)
        t[1:] = np.sqrt((x[1:] - x[:-1])**2 + (y[1:] - y[:-1])**2)  # NOQA
        t = np.cumsum(t)
    elif method == 'range':
        t = np.arange(x.shape[0], dtype=float)
    else:
        pass

    if method == 'range' or method == 'distant':
        t /= t[-1]
        nt = np.linspace(0, 1, n)
        fx = UnivariateSpline(t, x, k=k, s=s)
        fy = UnivariateSpline(t, y, k=k, s=s)
        xq = fx(nt)
        yq = fy(nt)
    else:
        spl = UnivariateSpline(x, y, k=k, s=s)
        xq = np.linspace(x[0], x[-1], n)
        yq = spl(xq)
    return xq, yq


def save_boundary(boundary, boundary_file):
    save(boundary, boundary_file)


def load_boundary(boundary_file):
    return load(boundary_file)
