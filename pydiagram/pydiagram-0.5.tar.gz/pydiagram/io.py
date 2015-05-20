# -*- coding: utf-8 -*-
"""
io.py
=====

Supported formats
-----------------

1. Python.Pickle dumped file
2. YAML file
3. A universal format file with extension "dgm"

NOTE: there is no aF_map in the dgm file.

dgm file format
---------------
First line: [x-axis name] [y-axis name]
other lines: [x value] [y value] [phase name] [free energy] [optimum cell size] [accuracy] [separation state]
Where separation state: 0 for non-separated and 1 for separated.
The first five columns are mandated while the last two are optional.
The optional values are assumed by their order.
For example, if only 6 columns are provided, then the 6th column is for [optimum cell size].

Sample file:
    phi xN
    0.1 12.5    HEX 3.953993    2.9543  8.7e-7  1
    0.1 12.6    LAM 3.970134    2.5877  1.7e-8  1

"""
import os.path
import yaml
import numpy as np
from scipy.io import loadmat

from .settings import *
from .config import parse_config
from .utils import find_name_value
from .utils import find_F_from_log, find_accuracy_from_log
from .utils import find_density_from_log
from .utils import compare_file_time
from .simulation import Simulation

__all__ = [
    'parse',
    'dump_dgm',
    'load_dgm',
    'list_all_data_dir',
]


def parse(basedir='./', config_file='config.yml', info_level=-1):
    '''
    Parse the simulation results output from various SCFT solvers.
    Currently support Polyorder and PolyFTS.
    The parser will create an YAML file in each result folder.
    The format of YAML file::

        xaxis:      phi
        yaxis:      xN
        coord:      [0.2, 18]
        phase:      HEX
        status:     2  # 0-Running, 1-Failed, 2-Done, 3-Timeout
        F:          3.953993
        a:          2.9543
        accuracy:
            force:  8.7e-7
            stress: 9.3e-5
        separated:  True
        a_list:     []
        F_list:     []

    '''
    config_file = os.path.join(basedir, config_file)
    config = parse_config(config_file)

    solver = config['solver']
    if not solver.upper() in SOLVER_LIST:
        print "Solver", solver, 'is not supported. Abort!'
        exit(1)

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

    for datapath, coord in data_dirs.iteritems():
        if info_level > 0:
            print datapath
            print coord
        if solver.upper() == 'POLYORDER':
            process_phase_dirs_polyorder(config, datapath,
                                         xaxis, yaxis, coord,
                                         info_level)
        elif solver.upper() == 'POLYFTS':
            process_phase_dirs_polyfts(config, datapath,
                                       xaxis, yaxis, coord,
                                       info_level)


def list_all_data_dir(basedir, xaxis, yaxis, names1, names2):
    '''
    :param xaxis: name of x axis variable
    :type xaxis: string
    :param yaxis: name of y axis variable
    :type yaxis: string
    :param names1: allowed 1st level dir name
    :type names1: list
    :param names2: allowed 2nd level dir name
    :type names2: list
    '''
    dirs = {}
    for dir1 in os.listdir(basedir):
        path1 = os.path.join(basedir, dir1)
        if not os.path.isdir(path1):
            continue
        name1, var1 = find_name_value(dir1)
        if name1 not in names1:
            continue
        if var1 is not None:
            for dir2 in os.listdir(path1):
                datapath = os.path.join(path1, dir2)
                if not os.path.isdir(datapath):
                    continue
                name2, var2 = find_name_value(dir2)
                if name2 not in names2:
                    continue
                if var2 is not None:
                    if name1 == xaxis:
                        x = var1
                        y = var2
                    else:
                        x = var2
                        y = var1
                    dirs[datapath] = (x, y)
    return dirs


def process_phase_dirs_polyfts(config, datapath,
                               xaxis, yaxis, coord,
                               info_level=-1):
    '''
    config should be the one returned by pydiagram.config.parse_config
    '''
    outfilename = config['outfiles']['point_data']
    datafilename = config['infiles']['result']
    densityfilename = config['infiles']['density']
    errorfilename = config['infiles']['error']
    statusfilename = config['infiles']['status']
    # logfilename = config['infiles']['log']

    tol_phi = float(config.tolerance.get('phi', TOL_PHI))
    parse_mode = config.process.parse
    if type(parse_mode) is bool:
        force_parse = False  # parse mode is 'yes' or 'no'
    else:
        if parse_mode.upper() == 'FORCE':
            force_parse = True
        else:
            force_parse = False

    for phasedir in os.listdir(datapath):
        if info_level > 2:
            print phasedir
        if phasedir not in PHASE_LIST:
            continue
        path = os.path.join(datapath, phasedir)
        if not os.path.isdir(path):
            continue
        outfile = os.path.join(path, outfilename)
        datafile = os.path.join(path, datafilename)
        densityfile = os.path.join(path, densityfilename)
        errorfile = os.path.join(path, errorfilename)
        statusfile = os.path.join(path, statusfilename)
        # logfile = os.path.join(path, logfilename)

        if compare_file_time(outfile, datafile) and not force_parse:
            continue

        F, accuracy_stress, a = parse_result_polyfts(datafile, info_level)
        if phasedir == 'DIS':
            accuracy_stress = 0.0
            a = 1.0
        accuracy = parse_error_polyfts(errorfile, info_level)
        separated = parse_density_polyfts(densityfile, tol_phi, info_level)
        status = parse_status_polyfts(statusfile, info_level)

        data = {'xaxis': xaxis, 'yaxis': yaxis, 'coord': list(coord),
                'phase': phasedir, 'status': status,
                'F': F, 'a': a,
                'accuracy': {'force': accuracy, 'stress': accuracy_stress},
                'separated': separated,
                'a_list': [], 'F_list': []}
        with open(outfile, 'w') as f:
            yaml.dump(data, f)
        if info_level > 3:
            print data


def parse_result_polyfts(datafile, info_level=-1):
    '''
    Typical datafile name is operators.dat
    The first line is the header has the following format
        # step Hamiltonian StressTensor# ChemicalPotential# CellTensor#
    where the number of StreeTensor is
        n = d(d+1)/2 + 1
    for d dimensional calculations. Note the last StreeTensor is not the real stress tensor but the pressure.
    Then the accuracy of cell size optimization is the L2-norm of the stress tensors:
        \sqrt{\sum_{i=1}^{n-1} \sigma_i^2}
    '''
    F = 'NA'
    stress = 'NA'
    a = 0.0
    if not os.path.exists(datafile):
        return F, stress, a

    with open(datafile, 'rb') as f:
        first = f.readline()
        if first == '':  # Empty file
            return F, stress, a
        f.seek(-2, 2)               # Jump to the second last byte.
        while f.read(1) != "\n":    # Until EOL is found...
            f.seek(-2, 1)           # ...jump back the read byte plus one more.
        last = f.readline()         # Read last line.
        if last == first:  # Only header line in the file
            return F, stress, a
        if info_level > 2:
            print datafile
            print first
            print last

    try:
        header = first.strip().split('#')
        header = header[1].split()      # header[0] is '#'
        result = last.strip().split()
        stress_list = []
        a_list = []
        for i in xrange(len(header)):
            if header[i].upper() == "HAMILTONIAN":
                F = float(result[i])
            else:
                name, value = find_name_value(header[i])
                if name.upper() == "STRESSTENSOR":
                    stress_list.append(float(result[i]))
                elif name.upper() == "CELLTENSOR":
                    a_list.append(float(result[i]))
    except:
        return F, stress, a

    stress_array = np.array(stress_list)[:-1]
    stress = np.linalg.norm(stress_array)
    dim = int(np.sqrt(len(a_list)))
    a_vec = np.array(a_list)[:dim]
    a = np.linalg.norm(a_vec)
    return F, stress.item(), a.item()


def parse_error_polyfts(errorfile, info_level=-1):
    '''
    Typical errorfile name is error_report.dat
    For each row, they are time steps, errors for each species.
    We choose the L1-norm of these errors as the accuracy.
    Error file does not have header line.
    '''
    if not os.path.exists(errorfile):
        return None

    with open(errorfile, 'rb') as f:
        first = f.readline()
        if first == '':  # Empty file
            return None

    with open(errorfile, 'rb') as f:
        for line in f:
            pass
        last = line

    result = last.strip().split()
    try:
        accuracy_array = np.array(map(float, result))[1:]
        accuracy = np.max(accuracy_array)
    except:
        return None
    return accuracy.item()


def parse_density_polyfts(densityfile, tol_phi=TOL_PHI, info_level=-1):
    '''
    This parser is based on Kris Delaney's code.
    '''
    if not os.path.exists(densityfile):
        return None

    with open(densityfile, 'rb') as f:
        first = f.readline()
        if first == '':  # Empty file
            return None

    try:
        with open(densityfile, 'rb') as f:
            fieldindex = 1  # Only check the first specie
            impart = False  # don't check the imaginary part
            version = int(f.readline().strip().split()[3])  # NOQA
            nfields = int(f.readline().strip().split()[3])  # NOQA
            ndim = int(f.readline().strip().split()[3])
            griddim = f.readline().strip().split()[4:4+ndim]  # NOQA
            # Convert all list entries to int
            griddim = [int(i) for i in griddim]
            kspacedata = True
            complexdata = True
            flagsline = f.readline().strip().split()
            if flagsline[4] == "0":
                kspacedata = False  # NOQA
            if flagsline[9] == "0":
                complexdata = False
            f.readline()  # Skip the last header line
            # Which column to use for field data?
            if complexdata:
                col = ndim + (fieldindex - 1) * 2
                if impart is True:
                    col = col + 1
            else:
                col = ndim + (fieldindex - 1)
            # Get the grid data
            data_row = np.loadtxt(f, usecols=[col])
    except:
        return None

    data_col = np.transpose(data_row)
    phi_avg = np.mean(data_col)
    phi_min = np.min(data_col)
    if np.abs(phi_avg - phi_min) > tol_phi:
        separated = True
    else:
        separated = False
    return separated


def parse_status_polyfts(statusfile, info_level=-1):
    '''
    Typical statusfile name is STATUS
    -1  -   Not available
    0   -   Running
    1   -   Failed
    2   -   Done
    3   -   Timeout
    '''
    if not os.path.exists(statusfile):
        return -1

    with open(statusfile, 'r') as f:
        line = f.readline().strip()

    if line == '':
        return -1

    try:
        status = int(line)
    except:
        return -1

    return status


def process_phase_dirs_polyorder(config, datapath,
                                 xaxis, yaxis, coord,
                                 info_level=-1):
    '''
    config should be the one returned by pydiagram.config.parse_config.
    '''
    outfilename = config['outfiles']['point_data']
    datafilename = config['infiles']['result']
    densityfilename = config['infiles']['density']
    logfilename = config['infiles']['log']

    tol_phi = float(config.tolerance.get('phi', TOL_PHI))
    tol_cell = float(config.tolerance.get('cell_size', TOL_CELL_SIZE))
    parse_mode = config.process.parse
    if type(parse_mode) is bool:
        force_parse = False  # parse mode is 'yes' or 'no'
    else:
        if parse_mode.upper() == 'FORCE':
            force_parse = True
        else:
            force_parse = False

    for phasedir in os.listdir(datapath):
        if info_level > 2:
            print phasedir
        if phasedir not in PHASE_LIST:
            continue
        path = os.path.join(datapath, phasedir)
        if not os.path.isdir(path):
            continue
        outfile = os.path.join(path, outfilename)
        datafile = os.path.join(path, datafilename)
        densityfile = os.path.join(path, densityfilename)
        logfile = os.path.join(path, logfilename)

        if compare_file_time(outfile, datafile) and not force_parse:
            continue

        alist = np.array([])
        Flist = np.array([])
        if phasedir == 'DIS':
            a = 1.0
            F, accuracy, separated = parse_log_polyorder(logfile, phasedir, a,
                                                         tol_cell, info_level)
            if F is None:
                F = 'NA'
        else:
            alist, Flist = parse_result_polyorder(datafile, info_level)
            if Flist.size == 0:
                F = 'NA'  # Not available
                a = 0.0
                accuracy = 'NA'
                separated = None
            else:
                a = float(alist[-1])  # convert to float for PyYAML dump
                F = float(Flist[-1])  # convert to float for PyYAML dump
                alist = alist[:-1]  # throw away last element
                Flist = Flist[:-1]  # throw away last element
                separated = parse_density_polyorder(densityfile, tol_phi,
                                                    info_level)
                F0, accuracy, separated0 = parse_log_polyorder(logfile,
                                                               phasedir,
                                                               a,
                                                               tol_cell,
                                                               info_level)
                if separated is None:
                    separated = separated0

        data = {'xaxis': xaxis, 'yaxis': yaxis, 'coord': list(coord),
                'phase': phasedir, 'F': F, 'a': a,
                'accuracy': {'force': accuracy, 'stress': None},
                'separated': separated,
                'a_list': alist.tolist(), 'F_list': Flist.tolist()}
        stream = file(outfile, 'w')
        yaml.dump(data, stream)


def parse_result_polyorder(datafile, info_level=-1):
    alist, Flist = np.array([]), np.array([])
    try:
        mat = loadmat(datafile)
        alist = mat['a']
        alist = alist.reshape(alist.size)
        Flist = mat['F']
        Flist = Flist.reshape(Flist.size)
    except:
        if info_level > -1:
            print "\tWarning: there is no data in", datafile
    return alist, Flist


def parse_log_polyorder(logfile, phase, a, tol=TOL_CELL_SIZE, info_level=-1):
    F = find_F_from_log(logfile, phase, info_level)
    accuracy = find_accuracy_from_log(logfile, a, info_level)
    if phase == 'DIS':
        separated = False
    else:
        phi_avg, phi_min, phi_max = find_density_from_log(logfile, a)
        if phi_avg is None or phi_min is None or phi_max is None:
            separated = None
        else:
            if np.abs(phi_avg - phi_min) > tol:
                separated = True
            else:
                separated = False
    return F, accuracy, separated


def parse_density_polyorder(densityfile, tol_phi=TOL_PHI, info_level=-1):
    separated = None
    try:
        mat = loadmat(densityfile)
        phi = mat['phiA'].flatten()
        phi_avg = np.mean(phi)
        phi_min = np.min(phi)
        if np.abs(phi_avg - phi_min) > tol_phi:
            separated = True
        else:
            separated = False
    except:
        if info_level > 2:
            print "\tWarning: there is no data in", densityfile

    return separated


def dump_dgm(xname, yname, info_map, dgmfile='',
             exclude_invalid=False, config={}, info_level=-1):
    '''
    if no dgmfile provided, return dumped string.
    '''
    dumpstr = xname + '\t' + yname + '\n'
    for phase, coord_info_dict in info_map.iteritems():
        for coord, info in coord_info_dict.iteritems():
            x, y = coord
            F = info.F
            a = info.a
            acc = info.accuracy
            sep = info.separated
            if sep:
                sep_str = '1'
            elif sep is not None:
                sep_str = '0'
            if exclude_invalid and not info.is_valid(config):
                continue
            line = str(x) + '\t' + str(y) + '\t' + phase + '\t' + str(F) + '\t'
            line += str(a) + '\t' + str(acc) + '\t' + sep_str + '\n'
            dumpstr += line

    if dgmfile == '':
        return dumpstr

    with open(dgmfile, 'w') as f:
        f.write(dumpstr)


def load_dgm(dgmfile, config={}, info_level=-1):
    xaxis = ''
    yaxis = ''
    info_map = {}

    if not os.path.exists(dgmfile):
        if info_level > 0:
            print 'File', dgmfile, 'does not exist.'
        return xaxis, yaxis, info_map

    with open(dgmfile, 'r') as f:
        firstline = f.readline()
        xaxis, yaxis = firstline.split()
        for line in f:
            values = line.split()
            if info_level > 2:
                print values
            if len(values) < 5:
                if info_level > 0:
                    print 'Require at least 5 columns in', dgmfile
                return {}
            x = float(values[0])
            y = float(values[1])
            phase = values[2]
            try:
                F = float(values[3])
            except:
                F = None
            try:
                a = float(values[4])
            except:
                a = None
            if len(values) > 5:
                try:
                    acc = float(values[5])
                except:
                    acc = None
            else:
                acc = None
            if len(values) > 6:
                try:
                    sep = bool(values[6])
                except:
                    sep = None
            else:
                sep = None
            coord = (x, y)
            data = {'xaxis': xaxis, 'yaxis': yaxis, 'coord': list(coord),
                    'phase': phase, 'F': F, 'a': a,
                    'accuracy': {'force': acc, 'stress': None},
                    'separated': sep,
                    'a_list': [], 'F_list': []}
            info = Simulation()
            info.load(data)

            if phase in info_map:
                coord_info_dict = info_map[phase]
                # Determine whether to override the info
                if coord in coord_info_dict:
                    info_old = coord_info_dict[coord]
                    if info.F is not None:
                        if info_old.F is None:
                            info_map[phase][coord] = info
                        elif info.F < info_old.F and info.is_valid(config):
                            info_map[phase][coord] = info
                else:
                    info_map[phase][coord] = info
            else:
                info_map[phase] = {coord: info}

    return xaxis, yaxis, info_map


def display():
    pass
