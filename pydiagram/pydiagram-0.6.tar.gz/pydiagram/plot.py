# -*- coding: utf-8 -*-
"""
plot.py
=======

Plotting related functions.

"""
import os.path
import itertools

import matplotlib as mpl
mpl.use('Agg')  # To avoid launching interactive plot, such as wxAgg.
import matplotlib.pyplot as plt
import mpltex
from mpltex.styles import _colors, _lines, _markers

from .diagram import get_diagram_points
from .boundary import get_ODT_boundary, get_connected_boundary
from .boundary import interpolate_boundary
from .energy import get_x_F_list, get_y_F_list
from .size import get_x_a_list, get_y_a_list
from .size import get_a_F_list, interp_cell_opt
from .accuracy import get_x_accuracy_list, get_y_accuracy_list
from .utils import find_label


__all__ = [
    'plot_diagram',
    'plot_boundary_line',
    'plot_boundary_point',
    'plot_phase_diagram',
    'plot_F',
    'plot_size',
    'plot_accuracy',
    'plot_info',
    'plot_cell_opt',
    'plot_cell_opt_point',
]


def plot_diagram(ax, diagram, markersize=3, colors=_colors,
                 allow_phase=[], ignore_phase=[]):
    colors = itertools.cycle(colors)
    if len(allow_phase) == 0:
        allow_phase = diagram.keys()
    for phase in diagram.keys():
        if phase in ignore_phase:
            continue
        if phase not in allow_phase:
            continue
        x, y = get_diagram_points(diagram, phase)
        # To adjust the size be consistent with plot()
        s = markersize**2  # NOQA
        ax.scatter(x, y, label=phase, s=s,
                   facecolor=colors.next(), linewidth=0)


def plot_boundary_line(ax, boundary, phase_pair_list=[], label='ODT',
                       interp_n=50, interp_k=3, interp_s=0,
                       interp_method='range', sort_axis='x', **kwargs):
    if not phase_pair_list:
        x, y = get_ODT_boundary(boundary, sort_axis)
    else:
        x, y = get_connected_boundary(boundary, phase_pair_list, sort_axis)

    # If there is only 1 or no boundary point, skip plotting
    if x.size > 1:
        if x.size > interp_k:
            xq, yq = interpolate_boundary(x, y, interp_n, interp_k, interp_s,
                                          interp_method)
        else:
            xq, yq = interpolate_boundary(x, y, interp_n, x.size - 1, interp_s,
                                          interp_method)
        kwargs['linestyle'] = '-'  # Ensure plot solid line
        ax.plot(xq, yq, label=label, **kwargs)


def plot_boundary_point(ax, boundary, phase_pair_list=[], label='ODT',
                        sort_axis='x', **kwargs):
    if not phase_pair_list:
        x, y = get_ODT_boundary(boundary, sort_axis)
    else:
        x, y = get_connected_boundary(boundary, phase_pair_list, sort_axis)

    if x.size > 0:
        kwargs['linestyle'] = ''  # Ensure only plot scatter points
        ax.plot(x, y, label=label, **kwargs)


def plot_phase_diagram(diagram, boundary, settings,
                       xaxis, yaxis, figfile='./diagram',
                       allow_phase=[], ignore_phase=[],
                       xlim=[], ylim=[], size=[], pad=0.1,
                       nbins=None, markersize=3, legend={}):
    '''
    `settings` is a list of dicts containing infomation of each phase boundary.
    settings = [dict1, dict2, dict3, ...]
    Each dict has following key-value pairs:
    {
        'label': 'ODT'  # mandatory
        'pairs': []     # optional
        'sort_axis':    # optional
        'interp_n':     # optional
        'interp_k':     # optional
        'interp_s':     # optional
        'method':       # optional
        'marker':       # optional
    }
    '''
    ls_boundary = mpltex.linestyle_generator(lines=['-'], markers=[])
    ls_boundary_point = mpltex.linestyle_generator(lines=[],
                                                   markers=['x'],
                                                   hollow_styles=[])
    fig, ax = plt.subplots(1)
    # ajust size to be square plot suitable for phase diagram
    # size compatible with mpltex.presentation_decorator
    if size:
        fig.set_size_inches(size[0], size[1])

    if diagram:
        plot_diagram(ax, diagram, markersize=markersize,
                     allow_phase=allow_phase, ignore_phase=ignore_phase)

    for setting in settings:
        label = setting.get('label')
        if label is None:
            continue
        pairs = setting.get('pairs', [])
        if not pairs:
            label = 'ODT'
        sort_axis = setting.get('sort_axis', 'x')
        n = setting.get('interp_n', 30)
        k = setting.get('interp_k', 1)
        s = setting.get('interp_s', 0)
        method = setting.get('method', 'standard')
        marker = setting.get('marker', False)
        styles = ls_boundary.next()
        if diagram:
            label = ''  # If phase points, ignore boundary label
        plot_boundary_line(ax, boundary, pairs, label,
                           n, k, s, method, sort_axis, **styles)
        if marker:
            styles = ls_boundary_point.next()
            styles['markersize'] = markersize
            label = ''
            plot_boundary_point(ax, boundary, pairs, label,
                                sort_axis, **styles)

    if nbins is not None:
        ax.locator_params(nbins=nbins)
    xlabel = find_label(xaxis)
    ylabel = find_label(yaxis)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    if legend:
        ax.legend(loc=legend['location'], ncol=legend['ncol'], scatterpoints=1)
    fig.tight_layout(pad=pad)

    fig.savefig(figfile)
    plt.close('all')


def convert_linestyle(linestyle):
    '''Convert linestyle properties to mpltex.linestyle_generator
    '''
    if linestyle.colors is not None:
        colors = linestyle.colors
    else:
        colors = _colors
    if linestyle.lines is not None:
        lines = linestyle.lines
    else:
        lines = _lines
    if linestyle.markers is not None:
        markers = linestyle.markers
    else:
        markers = _markers
    if linestyle.hollow is None:
        hollow = []
    else:
        hollow = linestyle.hollow
    ls_generator = mpltex.linestyle_generator(colors=colors,
                                              lines=lines,
                                              markers=markers,
                                              hollow_styles=hollow)
    return ls_generator


def plot_F(info_map, xaxis, yaxis, path,
           phases, val, base=None, xory='x', varlim=[],
           xlim=[], ylim=[], size=[], pad=0.1, nbins=None,
           markersize=3, linestyle={}, legend={}, config={}):
    try:
        output = config.plot.info.get('output', 'figure')
    except:
        output = 'figure'
    ls_generator = convert_linestyle(linestyle)
    figfile = 'F'
    if xory == 'x':
        middir = yaxis + str(val)
    else:
        middir = xaxis + str(val)
    basedir = os.path.join(path, middir)
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    figfile = os.path.join(basedir, figfile)
    if xory == 'x':
        xlabel = find_label(xaxis)
    else:
        xlabel = find_label(yaxis)
    if base:
        ylabel = '$F - F_{' + base + '}$'
    else:
        ylabel = '$F$'

    fig, ax = plt.subplots(1)

    if output.upper() == 'STDOUT':
        print
        print 'Free energy plot for',
        if xory == 'x':
            print yaxis, '=', val,
        else:
            print xaxis, '=', val,
        if base is not None:
            print 'with reference phase', base
    for phase in phases:
        if xory == 'x':
            var, F = get_x_F_list(info_map, phase, val, base,
                                  xlim=varlim, config=config)
        else:
            var, F = get_y_F_list(info_map, phase, val, base,
                                  ylim=varlim, config=config)
        ax.plot(var, F, label=phase, **ls_generator.next())
        if output.upper() == 'STDOUT':
            print phase
            print '\t', var
            print '\t', F

    if nbins is not None:
        ax.locator_params(nbins=nbins)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc=legend.location, ncol=legend.ncol, scatterpoints=1)
    fig.tight_layout(pad=pad)

    fig.savefig(figfile)
    plt.close('all')


def plot_size(info_map, xaxis, yaxis, path,
              phases, val, xory='x', varlim=[],
              xlim=[], ylim=[], size=[], pad=0.1, nbins=None,
              markersize=3, linestyle={}, legend={}, config={}):
    try:
        output = config.plot.info.get('output', 'figure')
    except:
        output = 'figure'
    ls_generator = convert_linestyle(linestyle)
    figfile = 'size'
    if xory == 'x':
        middir = yaxis + str(val)
    else:
        middir = xaxis + str(val)
    basedir = os.path.join(path, middir)
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    figfile = os.path.join(basedir, figfile)
    if xory == 'x':
        xlabel = find_label(xaxis)
    else:
        xlabel = find_label(yaxis)
    ylabel = 'cell size'

    fig, ax = plt.subplots(1)

    if output.upper() == 'STDOUT':
        print
        print 'Size plot for',
        if xory == 'x':
            print yaxis, '=', val
        else:
            print xaxis, '=', val
    for phase in phases:
        if xory == 'x':
            var, a = get_x_a_list(info_map, phase, val,
                                  xlim=varlim, config=config)
        else:
            var, a = get_y_a_list(info_map, phase, val,
                                  ylim=varlim, config=config)
        ax.plot(var, a, label=phase, **ls_generator.next())
        if output.upper() == 'STDOUT':
            print phase
            print '\t', var
            print '\t', a

    if nbins is not None:
        ax.locator_params(nbins=nbins)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc=legend.location, ncol=legend.ncol, scatterpoints=1)
    fig.tight_layout(pad=pad)

    fig.savefig(figfile)
    plt.close('all')


def plot_accuracy(info_map, xaxis, yaxis, path,
                  phases, val, xory='x', varlim=[],
                  xlim=[], ylim=[], size=[], pad=0.1, nbins=None,
                  markersize=3, linestyle={}, legend={}, config={}):
    try:
        output = config.plot.info.get('output', 'figure')
    except:
        output = 'figure'
    ls_generator = convert_linestyle(linestyle)
    figfile = 'accuracy'
    if xory == 'x':
        middir = yaxis + str(val)
    else:
        middir = xaxis + str(val)
    basedir = os.path.join(path, middir)
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    figfile = os.path.join(basedir, figfile)
    if xory == 'x':
        xlabel = find_label(xaxis)
    else:
        xlabel = find_label(yaxis)
    ylabel = 'error'

    fig, ax = plt.subplots(1)

    if output.upper() == 'STDOUT':
        print
        print 'Accuracy plot for',
        if xory == 'x':
            print yaxis, '=', val
        else:
            print xaxis, '=', val
    for phase in phases:
        if xory == 'x':
            var, acc = get_x_accuracy_list(info_map, phase, val,
                                           xlim=varlim, config=config)
        else:
            var, acc = get_y_accuracy_list(info_map, phase, val,
                                           ylim=varlim, config=config)
        ax.plot(var, acc, label=phase, **ls_generator.next())
        if output.upper() == 'STDOUT':
            print phase
            print '\t', var
            print '\t', acc

    if nbins is not None:
        ax.locator_params(nbins=nbins)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc=legend.location, ncol=legend.ncol, scatterpoints=1)
    fig.tight_layout(pad=pad)

    fig.savefig(figfile)
    plt.close('all')


def plot_info(info_map, xaxis, yaxis, path,
              phases, val, base=None, xory='x', varlim=[],
              xlim=[], ylim=[], size=[], pad=0.1, nbins=None,
              markersize=3, linestyle={}, legend={}, config={}):
    plot_F(info_map, xaxis, yaxis, path, phases, val, base, xory,
           varlim, xlim, ylim, size, pad, nbins, markersize,
           linestyle, legend, config)

    plot_size(info_map, xaxis, yaxis, path, phases, val, xory,
              varlim, xlim, ylim, size, pad, nbins, markersize,
              linestyle, legend, config)

    plot_accuracy(info_map, xaxis, yaxis, path, phases, val, xory,
                  varlim, xlim, ylim, size, pad, nbins, markersize,
                  linestyle, legend, config)
    # display_separation(info_map, phases, val, xory, varlim)


def plot_cell_opt(ax, info_map, coord, phase,
                  interp_n=100, interp_k=3, interp_s=0,
                  show_label=True, **kwargs):
    a, F = get_a_F_list(info_map, coord, phase)

    if not show_label:
        label = ''
    else:
        label = str(coord) + ': ' + phase

    if a.size < interp_k:
        interp_k = a.size
    aq, Fq = interp_cell_opt(a, F, interp_n, interp_k, interp_s)
    ax.plot(aq, Fq, label=label, **kwargs)


def plot_cell_opt_point(ax, aF_map, coord, phase, show_label=True, **kwargs):
    a, F = get_a_F_list(aF_map, coord, phase)

    if not show_label:
        label = ''
    else:
        label = str(coord) + ': ' + phase

    if a.size > 0:
        ax.plot(a, F, label=label, **kwargs)
