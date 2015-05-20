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
    'interpolate_boundary',
    'get_boundary_line',
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


def get_boundary(diagram, info_map, alongx=True, alongy=True,
                 config={}, info_level=-1):
    boundary = {}
    diagram_inv = inverse_diagram(diagram)
    x_map, y_map = get_energy_map(info_map)

    # find the phase boundary along y direction (keeping x fixed)
    if alongy:
        for x, phase_yF_dict in x_map.iteritems():
            if info_level > 1:
                print x
            # format: [(y1, phase), (y2, phase), (y3, phase)]
            y_phase_list = []
            for coord, phase in diagram_inv.iteritems():
                x0, y0 = coord
                if np.allclose(x, x0):
                    y_phase_list.append((y0, phase))
            y_phase_list.sort()  # y in ascending order
            if len(y_phase_list) == 0:
                continue
            if info_level > 2:
                print y_phase_list

            y1, phase1 = y_phase_list[0]
            for (y, phase) in y_phase_list:
                if phase != phase1:
                    y2 = y
                    phase2 = phase
                    if info_level > 2:
                        print phase1, y1, phase2, y2
                        print phase_yF_dict
                    yb = get_boundary_point(phase_yF_dict,
                                            phase1, phase2, y1, y2,
                                            info_level)
                    if yb is None:
                        if info_level > 0:
                            print 'No boundary detected for (',
                            print x, phase1, phase2, y1, y2, ')'
                        # yb = 0.5 * (y1 + y2)
                        y1 = y2
                        phase1 = phase2
                        continue
                    if yb < 0:
                        if info_level > 0:
                            print 'Negative boundary detected for (',
                            print x, phase1, phase2, y1, y2, ')'
                        y1 = y2
                        phase1 = phase2
                        continue

                    if phase1 > phase2:
                        if (phase1, phase2) in boundary:
                            boundary[(phase1, phase2)].append((x, yb))
                        else:
                            boundary[(phase1, phase2)] = [(x, yb)]
                    else:
                        if (phase2, phase1) in boundary:
                            boundary[(phase2, phase1)].append((x, yb))
                        else:
                            boundary[(phase2, phase1)] = [(x, yb)]
                    y1 = y2
                    phase1 = phase2
                else:
                    y1 = y
                    phase1 = phase  # this line can be removed

    if info_level > 1:
        print "Boundary after y direction search: "
        pprint(boundary)

    # find the phase boundary along y direction (keeping x fixed)
    if alongx:
        for y, phase_xF_dict in y_map.iteritems():
            if info_level > 1:
                print y
            # format: [(x1, phase), (x2, phase), (x3, phase)]
            x_phase_list = []
            for coord, phase in diagram_inv.iteritems():
                x0, y0 = coord
                if np.allclose(y, y0):
                    x_phase_list.append((x0, phase))
            x_phase_list.sort()  # x in ascending order
            if len(x_phase_list) == 0:
                continue
            if info_level > 2:
                print x_phase_list

            x1, phase1 = x_phase_list[0]
            for (x, phase) in x_phase_list:
                if phase != phase1:
                    x2 = x
                    phase2 = phase
                    if info_level > 2:
                        print phase1, x1, phase2, x2
                        print phase_xF_dict
                    xb = get_boundary_point(phase_xF_dict,
                                            phase1, phase2, x1, x2,
                                            info_level)
                    if xb is None:
                        if info_level > 0:
                            print 'No boundary detected for (',
                            print y, phase1, phase2, x1, x2, ')'
                        # xb = 0.5 * (x1 + x2)
                        x1 = x2
                        phase1 = phase2
                        continue
                    if xb < 0:
                        if info_level > 0:
                            print 'Negative boundary detected for (',
                            print y, phase1, phase2, x1, x2, ')'
                        x1 = x2
                        phase1 = phase2
                        continue

                    if phase1 > phase2:
                        if (phase1, phase2) in boundary:
                            boundary[(phase1, phase2)].append((xb, y))
                        else:
                            boundary[(phase1, phase2)] = [(xb, y)]
                    else:
                        if (phase2, phase1) in boundary:
                            boundary[(phase2, phase1)].append((xb, y))
                        else:
                            boundary[(phase2, phase1)] = [(xb, y)]
                    x1 = x2
                    phase1 = phase2
                else:
                    x1 = x
                    phase1 = phase  # this line can be removed

    if info_level > 1:
        print "Boundary after x direction search: "
        pprint(boundary)

    return boundary


def get_boundary_point(phase_varF_dict, phase1, phase2, var1, var2,
                       info_level=-1):
    '''
    Return a phase boundary point (in x or y dimension) between phase1 and phase2.
    If the phase boundary is the ODT, we need to
    approximate the phase boundary point using DIS and the phase with
    the lowest free energy.
    Otherwise (for OOT), use the phase1 and phase2 provided.
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

    varF1_list = phase_varF_dict[phase1]
    varF1_list.sort()
    var1_list = np.array([var for (var, F) in varF1_list])
    F1_list = np.array([F for (var, F) in varF1_list])
    varF2_list = phase_varF_dict[phase2]
    varF2_list.sort()
    var2_list = np.array([var for (var, F) in varF2_list])
    F2_list = np.array([F for (var, F) in varF2_list])

    if info_level > 2:
        print varF1_list
        print varF2_list

    # Find common data points between var1 and var2
    index1 = find_index_of_common_elements(var1_list, var2_list)
    index2 = find_index_of_common_elements(var2_list, var1_list)
    if index1.size == 0 or index2.size == 0:
        return None
    var1_list = var1_list[index1]
    F1_list = F1_list[index1]
    var2_list = var2_list[index2]
    F2_list = F2_list[index2]

    if info_level > 2:
        print var1_list
        print F1_list
        print var2_list
        print F2_list

    i, j = find_index(var1_list, (var1, var2))
    if i is None or j is None:
        return None
    # reference phase is DIS if phase1 or phase2 is 'DIS'
    # otherwise, reference phase is phase1
    if phase1 == 'DIS':
        dF_list = F2_list - F1_list
        if j + 2 > dF_list.size:
            return None
        else:
            k, b = np.polyfit(var1_list[j:j+2], dF_list[j:j+2], 1)  # NOQA
            varb = -b / k
    elif phase2 == 'DIS':
        dF_list = F1_list - F2_list
        if j + 2 > dF_list.size:
            return None
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


def interpolate_boundary(x, y, n=100, k=3, s=0, method='range'):
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


def get_boundary_line(boundary, phase_pair_list=[], interp_k=3, interp_s=0,
                      interp_method='range', sort_axis='x'):
    pass


def save_boundary(boundary, boundary_file):
    save(boundary, boundary_file)


def load_boundary(boundary_file):
    return load(boundary_file)
