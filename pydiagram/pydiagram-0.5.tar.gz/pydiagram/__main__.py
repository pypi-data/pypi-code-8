# -*- coding: utf-8 -*-
"""
__main__.py
===========

This file turns the package into an excutable.

"""
import argparse
import sys
import os.path
import time
import itertools

import matplotlib as mpl
mpl.use('Agg')  # To avoid launching interactive plot, such as wxAgg.
import mpltex
from mpltex.styles import _colors

from ._version import __version__
from .utils import load, save
from .utils import now2str
from .config import parse_config
from .config import parse_config_predictor_manual
from .diagram import get_info_map, get_diagram_from_info_map
from .diagram import refine_diagram
from .boundary import get_boundary
from .plot import plot_phase_diagram, plot_info
from .simulation import find_invalid_simulations
from .simulation import transform_invalid_simulations_to_diagram
from .simulation import predict_simulations
from .simulation import prepare_simulation_jobs
from .simulation import upload_simulation_jobs
from .simulation import download_simulation_jobs
from .simulation import submit_simulation_jobs


def main_process(config):
    info_level = config.info_level
    parse_mode = config.process.parse
    if type(parse_mode) is bool:
        is_parsed = (not parse_mode)
    else:
        if parse_mode.upper() == 'NO':
            is_parsed = True
        else:
            is_parsed = False
    alongx = config.process.boundary.alongx
    alongy = config.process.boundary.alongy
    diagram_file = config.outfiles.diagram
    info_map_file = config.outfiles.info_map
    boundary_file = config.outfiles.boundary

    info_map = get_info_map(is_parsed=is_parsed, info_level=info_level)
    # pprint(info_map)

    config = parse_config('./config.yml')
    diagram = get_diagram_from_info_map(info_map, config, info_level)
    # pprint(diagram)

    boundary = get_boundary(diagram, info_map, alongx, alongy, info_level)
    # pprint(boundary)

    save(info_map, info_map_file)
    save(diagram, diagram_file)
    save(boundary, boundary_file)


def main_plot(config):
    '''
    mode: [raw, standard, boundary, NA]
    source: [file, process]
    '''
    mode = config.plot.mode
    source = config.plot.data_source
    diagram_file = config.outfiles.diagram
    info_map_file = config.outfiles.info_map
    boundary_file = config.outfiles.boundary

    if source.upper() == 'PROCESS':
        main_process(config)

    info_map = load(info_map_file)
    diagram = load(diagram_file)
    boundary = load(boundary_file)

    if mode.upper() == 'RAW':
        main_plot_diagram(diagram, 'raw', config)
    elif mode.upper() == 'NA':
        invalid_sim = find_invalid_simulations(info_map, config)
        diagram_na = transform_invalid_simulations_to_diagram(invalid_sim)
        main_plot_diagram(diagram_na, 'NA', config)
    elif mode.upper() == 'BOUNDARY':
        main_plot_boundary(boundary, config)
    elif mode.upper() == 'STANDARD':
        main_plot_standard(diagram, boundary, config)
    elif mode.upper() == 'ALL':
        # raw
        main_plot_diagram(diagram, 'raw', config)
        # NA
        invalid_sim = find_invalid_simulations(info_map, config)
        diagram_na = transform_invalid_simulations_to_diagram(invalid_sim)
        main_plot_diagram(diagram_na, 'NA', config)
        # boundary
        main_plot_boundary(boundary, config)
        # standard
        main_plot_standard(diagram, boundary, config)
    elif mode.upper() == 'INFO':
        main_plot_info(info_map, config)
    else:
        print 'Plot mode:', mode, 'is not supported.'
        print 'Abort!'
        sys.exit(1)


def main_plot_diagram(diagram, mode, config):
    xaxis = config.xaxis
    yaxis = config.yaxis
    path = config.figures.diagram
    allow_phase = config.plot.allow_phase
    ignore_phase = config.plot.ignore_phase
    xlim = config.plot.xlim
    ylim = config.plot.ylim
    size = config.plot.size
    pad = config.plot.pad
    nbins = config.plot.nbins
    markersize = config.plot.marker_size
    colors = config.plot.linestyle.colors
    if colors is None:
        colors = _colors
    legend = config.plot.legend
    render = config.plot.render
    mpltex_deco = config.plot.mpltex.decorator

    if render.upper() == 'MPLTEX':
        if mpltex_deco.upper() == 'ACS':
            ploter = mpltex.acs_decorator(plot_phase_diagram)
        elif mpltex_deco.upper() == 'RSC':
            ploter = mpltex.rsc_decorator(plot_phase_diagram)
        elif mpltex_deco.upper() == 'WEB':
            ploter = mpltex.web_decorator(plot_phase_diagram)
        else:
            ploter = mpltex.presentation_decorator(plot_phase_diagram)
    else:
        ploter = plot_phase_diagram

    if mode.upper() == 'RAW':
        figfile = 'diagram_raw_{}_{}'.format(xaxis, yaxis)
        figfile = os.path.join(path, figfile)
        ploter(diagram, None, [], xaxis, yaxis, figfile,
               allow_phase, ignore_phase, xlim, ylim, size, pad, nbins,
               markersize, legend)
    else:
        for phase, coord_list in diagram.iteritems():
            figfile = 'diagram_na_{}_{}_{}'.format(phase, xaxis, yaxis)
            figfile = os.path.join(path, figfile)
            ploter({phase: coord_list}, None, [], xaxis, yaxis, figfile,
                   allow_phase, ignore_phase, xlim, ylim, size, pad, nbins,
                   markersize, legend)


def main_plot_boundary(boundary, config):
    boundary_settings = config.plot.boundary
    xaxis = config.xaxis
    yaxis = config.yaxis
    path = config.figures.diagram
    xlim = config.plot.xlim
    ylim = config.plot.ylim
    size = config.plot.size
    pad = config.plot.pad
    nbins = config.plot.nbins
    markersize = config.plot.marker_size
    legend = config.plot.legend
    render = config.plot.render
    mpltex_deco = config.plot.mpltex.decorator

    if render.upper() == 'MPLTEX':
        if mpltex_deco.upper() == 'ACS':
            ploter = mpltex.acs_decorator(plot_phase_diagram)
        elif mpltex_deco.upper() == 'RSC':
            ploter = mpltex.rsc_decorator(plot_phase_diagram)
        elif mpltex_deco.upper() == 'WEB':
            ploter = mpltex.web_decorator(plot_phase_diagram)
        else:
            ploter = mpltex.presentation_decorator(plot_phase_diagram)
    else:
        ploter = plot_phase_diagram

    figfile = 'boundary_{}_{}'.format(xaxis, yaxis)
    figfile = os.path.join(path, figfile)
    ploter(None, boundary, boundary_settings, xaxis, yaxis,
           figfile=figfile, xlim=xlim, ylim=ylim, size=size,
           pad=pad, nbins=nbins, markersize=markersize, legend=legend)


def main_plot_standard(diagram, boundary, config):
    xaxis = config.xaxis
    yaxis = config.yaxis
    path = config.figures.diagram
    allow_phase = config.plot.allow_phase
    ignore_phase = config.plot.ignore_phase
    xlim = config.plot.xlim
    ylim = config.plot.ylim
    size = config.plot.size
    pad = config.plot.pad
    nbins = config.plot.nbins
    markersize = config.plot.marker_size
    colors = config.plot.linestyle.colors
    if colors is None:
        colors = _colors
    legend = config.plot.legend
    boundary_settings = config.plot.boundary
    render = config.plot.render
    mpltex_deco = config.plot.mpltex.decorator

    if render.upper() == 'MPLTEX':
        if mpltex_deco.upper() == 'ACS':
            ploter = mpltex.acs_decorator(plot_phase_diagram)
        elif mpltex_deco.upper() == 'RSC':
            ploter = mpltex.rsc_decorator(plot_phase_diagram)
        elif mpltex_deco.upper() == 'WEB':
            ploter = mpltex.web_decorator(plot_phase_diagram)
        else:
            ploter = mpltex.presentation_decorator(plot_phase_diagram)
    else:
        ploter = plot_phase_diagram

    figfile = 'diagram_with_boundary_{}_{}'.format(xaxis, yaxis)
    figfile = os.path.join(path, figfile)
    ploter(diagram, boundary, boundary_settings, xaxis, yaxis, figfile,
           allow_phase, ignore_phase, xlim, ylim, size, pad, nbins,
           markersize, legend)


def main_plot_info(info_map, config):
    xaxis = config.xaxis
    yaxis = config.yaxis
    path = config.figures.info
    xlim = config.plot.xlim
    ylim = config.plot.ylim
    size = config.plot.size
    pad = config.plot.pad
    nbins = config.plot.nbins
    markersize = config.plot.marker_size
    linestyle = config.plot.linestyle
    legend = config.plot.legend
    phases = config.plot.info.phases
    val_list = config.plot.info.val
    base = config.plot.info.base
    xory = config.plot.info.xory
    varlim = config.plot.info.varlim
    render = config.plot.render
    mpltex_deco = config.plot.mpltex.decorator

    if render.upper() == 'MPLTEX':
        if mpltex_deco.upper() == 'ACS':
            ploter = mpltex.acs_decorator(plot_info)
        elif mpltex_deco.upper() == 'RSC':
            ploter = mpltex.rsc_decorator(plot_info)
        elif mpltex_deco.upper() == 'WEB':
            ploter = mpltex.web_decorator(plot_info)
        else:
            ploter = mpltex.presentation_decorator(plot_info)
    else:
        ploter = plot_info

    for val in val_list:
        ploter(info_map, xaxis, yaxis, path,
               phases, val, base, xory, varlim,
               xlim, ylim, size, pad, nbins, markersize,
               linestyle, legend, config)


def main_serve(config):
    info_level = config.info_level
    alongx = True
    alongy = True
    batchsize = config.predictor.max_batch_jobs
    sleeptime = config.predictor.update_period

    print 'PyDiagram is running in server mode.'
    print now2str('%Y-%m-%d %H:%M:%S')
    print

    pcd1, pcd2 = parse_config_predictor_manual(config)
    if pcd1 or pcd2:
        info_map = get_info_map(is_parsed=False, info_level=info_level)
        sim_list = predict_simulations(info_map, config,
                                       pcd1, True, info_level)
        sim_list += predict_simulations(info_map, config,
                                        pcd2, False, info_level)
        if sim_list:
            print 'Submit extra simulation jobs.'
            prepare_simulation_jobs(sim_list, config, info_level=info_level)
            upload_simulation_jobs(sim_list, config, info_level=info_level)
            time.sleep(0.5)  # Wait for transferred files ready to be read.
            submit_simulation_jobs(sim_list, config, info_level=info_level)
            print len(sim_list), 'simulations have been submitted.'
            print

    while True:
        print 'Begin to update phase diagram.'

        print
        print 'Download simulation results from sever ...'
        download_simulation_jobs(config, info_level=info_level)
        time.sleep(0.5)  # Wait for transferred files ready to be read.
        print 'Done.'

        print
        print 'Find phase boundary points ...'
        info_map = get_info_map(is_parsed=False, info_level=info_level)
        diagram = get_diagram_from_info_map(info_map, config, info_level)
        boundary = get_boundary(diagram, info_map, alongx, alongy, info_level)
        print 'Done.'

        print
        print 'Refine phase diagram ...'
        sim_list_all = refine_diagram(boundary, info_map, config, info_level)
        print 'Done.'

        for i in range(0, len(sim_list_all), batchsize):
            # the last batch is correct even if its size is
            # smaller than batchsize
            # The right range index can be larger than list size
            sim_list = sim_list_all[i:i+batchsize]  # NOQA

            print
            print 'Submit #{} to #{} simulation jobs.'.format(i+1, i+batchsize)

            print
            print 'Prepare new simulation jobs ...'
            prepare_simulation_jobs(sim_list, config, info_level=info_level)
            print 'Done.'

            print
            print 'Upload prepared simulation jobs ...'
            upload_simulation_jobs(sim_list, config, info_level=info_level)
            time.sleep(0.5)  # Wait for transferred files ready to be read.
            print 'Done.'

            print
            print 'Run simulation jobs in the server ...'
            submit_simulation_jobs(sim_list, config, info_level=info_level)
            print 'Done.'

        print
        print len(sim_list_all), 'simulations have been submitted.'

        print
        print now2str('%Y-%m-%d %H:%M:%S')
        print "Waiting for {} seconds to update again.".format(sleeptime)
        print "Waiting ...",
        spinner = itertools.cycle(['/', '-', '\\', '|'])
        spin_speed = 0.2
        t = 0
        while t < sleeptime:
            sys.stdout.write(spinner.next())  # write the next character
            sys.stdout.flush()                # flush stdout buffer
            sys.stdout.write('\b')            # erase the last written char
            time.sleep(spin_speed)
            t += spin_speed
        print


def main():
    parser = argparse.ArgumentParser(description='pydiagram options.')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='pydiagram {version}'.format(
                                version=__version__))
    parser.add_argument('-p', '--process',
                        action='store_true',
                        help='If present or True, do pydiagram processing.')
    parser.add_argument('-q', '--plot',
                        action='store_true',
                        help='If present or True, do pydiagram plotting.')
    parser.add_argument('-s', '--serve',
                        action='store_true',
                        help='If present or True, use pydiagram as a server.')
    args = parser.parse_args()

    config_file = './config.yml'
    if not os.path.exists(config_file):
        print 'Make sure config.yml in the current directory.'
        sys.exit(1)
    config = parse_config(config_file)
    if not config:
        print 'Error occurs when read config.yml.'
        sys.exit(1)

    if args.process:
        main_process(config)
    elif args.plot:
        main_plot(config)
    elif args.serve:
        main_serve(config)
    else:
        print 'Please supply at least one argument.'
        print 'Run diagram -h for more information.'
        sys.exit(1)

    sys.exit(0)


# Call the main function
main()
