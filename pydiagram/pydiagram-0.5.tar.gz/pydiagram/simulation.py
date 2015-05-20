# -*- coding: utf-8 -*-
"""
simulation.py
=============

simulation related classes and functions.

invalid_simulations format
--------------------------

    {
        (x1,y1): [phase11, phase12, phase13, ...],
        (x2,y2): [phase21, phase22, phase23, ...],
        (x3,y3): [phase31, phase32, phase33, ...],
        ...
    }

"""
import re
import os.path
from shutil import copyfile
import subprocess
import time

import yaml
import numpy as np
from scipy.spatial import cKDTree
from scipy.interpolate import interp2d
# from scipy.interpolate import griddata

from .settings import *
from .size import is_valid_cell_opt
from .size import predict_size
from .size import get_x_a_list, get_y_a_list
from .utils import find_neighbor_index
from .utils import find_interp_list
from .utils import format_number_for_dirname
from .utils import format_array_by_precision
from .server import run_command

__all__ = [
    'Simulation',
    'PolyorderSimulation',
    'PolyFTSSimulation',
    'find_invalid_simulations',
    'find_invalid_simulations_in_diagram',
    'find_valid_simulations',
    'find_valid_coordinates_and_sizes',
    'transform_invalid_simulations_to_diagram',
    'predict_simulations',
    'interpolate_simulations',
    'prepare_simulation_jobs',
    'upload_simulation_jobs',
    'download_simulation_jobs',
    'submit_simulation_jobs',
]


class Simulation:
    '''A Simulation object contains all information relevant to PyDigram
    Attributes:
        phase:      One of settings.PHASE_LIST
        xaxis:      x variable name
        yaxis:      y variable name
        corrd:      [x, y]
        F:          free energy
        a:          unit cell size
        accuracy:   L2-norm of force
        separated:  spearation state
    '''
    def __init__(self):
        self.phase = NA_PHASE
        self.xaxis = ''
        self.yaxis = ''
        self.order = True  # True: ./<xaxis>#/<yaxis>#/; False: reverse
        self.coord = []
        self.neighbor_coord = []
        self.F = None
        self.a = 0.0
        self.accuracy = None
        self.separated = None
        self.status = -1

    def loadfile(self, datafile):
        if not os.path.exists(datafile):
            return
        with open(datafile, 'r') as f:
            data = yaml.safe_load(f)
        self.load(data)

    def load(self, data):
        self.phase = data['phase']
        self.xaxis = data['xaxis']
        self.yaxis = data['yaxis']
        try:
            self.coord = list(data['coord'])
        except:
            pass  # use default []
        try:
            self.F = float(data['F'])
        except:
            pass  # use default None
        try:
            self.a = float(data['a'])
        except:
            pass  # use default 0.0
        try:
            self.accuracy = float(data['accuracy']['force'])
        except:
            pass  # use default None
        try:
            self.separated = bool(data['separated'])
        except:
            pass  # use default None
        try:
            self.status = data['status']
        except:
            pass  # use default -1

    def is_valid(self, config={}):
        # Free energy should exist
        if self.F is None:
            return False

        # Cell size should larger than 0.0
        if not self.a > 0.0:
            return False

        # accuracy should be less than a tolerance.
        # accuracy is None means accuracy is not available.
        # if accuracy is not available, skip the check.
        tol_default = TOL_STOP * C_STOP
        try:
            tol_force = config['tolerance'].get('stop_force', tol_default)
            tol_force = float(tol_force)
        except:
            tol_force = tol_default
        if self.accuracy is not None:
            if self.accuracy > tol_force:
                return False

        # separated is None means separated is not available.
        # if separated is not available, skip the check.
        if self.separated is not None:
            # separated should be true for non-DIS phase
            if self.phase != 'DIS' and not self.separated:
                return False
            # separated should be false for DIS phase
            if self.phase == 'DIS' and self.separated:
                return False

        # All tests passed.
        return True

    def get_coord(self, xaxis, yaxis):
        if xaxis == self.xaxis and yaxis == self.yaxis:
            return self.coord
        elif xaxis == self.yaxis and yaxis == self.xaxis:
            return self.coord[::-1]
        else:
            return []


class PolyorderSimulation(Simulation):
    '''A class derived from Simulation
    Attributes (Additional):
        a_list:    cell optimization cell size list
        F_list:    free energy list corresponding to a_list
    '''
    def __init__(self):
        Simulation.__init__(self)
        self.a_list = []
        self.F_list = []

    def load(self, data):
        Simulation.load(self, data)
        try:
            self.a_list = data['a_list']
        except:
            pass  # use defalut []
        try:
            self.F_list = data['F_list']
        except:
            pass  # use default []

    def loadfile(self, datafile):
        Simulation.loadfile(self, datafile)
        if not os.path.exists(datafile):
            return
        with open(datafile, 'r') as f:
            data = yaml.safe_load(f)
        self.load(data)

    def is_valid(self, config={}):
        if not Simulation.is_valid(self, config):
            return False

        # whether perform the basic check
        try:
            basic_check = config.get('basic_check', False)
        except:
            basic_check = False
        if basic_check:
            return True

        # cell optimization should be successful
        try:
            tol_F = float(config['tolerance'].get('F', TOL_F))
        except:
            tol_F = TOL_F
        if self.a_list and self.F_list:
            if not is_valid_cell_opt(self.a_list, self.F_list, tol_F):
                return False

        # All tests passed
        return True


class PolyFTSSimulation(Simulation):
    '''A class derived from Simulation
    Attributes (Additional):
        accuracy_stress:    L2-norm of stress tensors
        status:             simulation status
    '''
    def __init__(self):
        Simulation.__init__(self)
        self.accuracy_stress = None

    def load(self, data):
        Simulation.load(self, data)
        try:
            self.accuracy_stress = float(data['accuracy']['stress'])
        except:
            pass  # use default 1.0

    def loadfile(self, datafile):
        Simulation.loadfile(self, datafile)
        if not os.path.exists(datafile):
            return
        with open(datafile, 'r') as f:
            data = yaml.safe_load(f)
        self.load(data)

    def is_valid(self, config={}):
        if not Simulation.is_valid(self, config):
            return False

        # whether perform the basic check
        try:
            basic_check = config.get('basic_check', False)
        except:
            basic_check = False
        if basic_check:
            return True

        # accuracy of stress should less than a tolerance
        try:
            tol_stress = config['tolerance'].get('stop_stress', TOL_STRESS)
            tol_stress = float(tol_stress)
        except:
            tol_stress = TOL_STRESS
        if (self.accuracy_stress > tol_stress and
                self.accuracy_stress is not None):
            return False

        # the status should not be 1 (Failed).
        # other status are all OK.
        # this is a very loose check because -1-NA, 0-Running, 2-Done, and
        # 3-Timeout will all pass the check.
        if self.status == 1:
            return False

        # All tests passed
        return True


def find_invalid_simulations(info_map, config={}, info_level=-1):
    invalid_simulations = {}
    for phase, coord_info_dict in info_map.iteritems():
        for coord, info in coord_info_dict.iteritems():
            if info_level > 2:
                print 'Examing:', coord, phase
            if not info.is_valid(config):
                if coord in invalid_simulations:
                    invalid_simulations[coord].append(phase)
                else:
                    invalid_simulations[coord] = [phase]
                if info_level > 2:
                    print coord, phase, 'is invalid.'
    return invalid_simulations


def find_invalid_simulations_in_diagram(diagram, info_map, config={},
                                        info_level=-1):
    '''
    We assume that all coord and phase in diagram are in info_map.
    No extra check are taken.
    '''
    invalid_simulations = {}
    for phase, coord_list in diagram.iteritems():
        coord_info_dict = info_map[phase]
        for coord in coord_list:
            if info_level > 2:
                print 'Examing', coord, phase
            info = coord_info_dict[coord]
            if not info.is_valid(config):
                if coord in invalid_simulations:
                    invalid_simulations[coord].append(phase)
                else:
                    invalid_simulations[coord] = [phase]
                if info_level > 2:
                    print coord, phase, 'is invalid.'
    return invalid_simulations


def transform_invalid_simulations_to_diagram(invalid_simulations):
    '''
    Just re-organize the invalid_simulations to diagram format.
    '''
    diagram_na = {}
    for coord, phase_list in invalid_simulations.iteritems():
        for phase in phase_list:
            if phase in diagram_na:
                diagram_na[phase].append(coord)
            else:
                diagram_na[phase] = [coord]
    return diagram_na


def find_valid_simulations(info_map, config={}, info_level=-1):
    valid_simulations = []
    for phase, coord_info_dict in info_map.iteritems():
        for coord, info in coord_info_dict.iteritems():
            if info_level > 2:
                print 'Examing:', coord, phase
            if info.is_valid(config):
                valid_simulations.append(info)
                if info_level > 2:
                    print coord, phase, 'is valid.'
    return valid_simulations


def find_valid_coordinates_and_sizes(info_map, phase, config={},
                                     info_level=-1):
    x_list = []
    y_list = []
    a_list = []
    if phase in info_map:
        coord_info_dict = info_map[phase]
        for coord, info in coord_info_dict.iteritems():
            if info.is_valid(config):
                x_list.append(coord[0])
                y_list.append(coord[1])
                a_list.append(info.a)

    return (x_list, y_list, a_list)


def find_range(info_map, phase_pair, coord, config, info_level=-1):
    p1, p2 = phase_pair
    x, y = coord

    x_list, ax_list = get_x_a_list(info_map, p1, y, config=config)
    x_range_index1 = find_neighbor_index(x_list, x)
    y_list, ay_list = get_y_a_list(info_map, p1, x, config=config)
    y_range_index1 = find_neighbor_index(y_list, y)
    if x_range_index1:
        x_range1 = x_list[x_range_index1].tolist()
    else:
        x_range1 = []
    if y_range_index1:
        y_range1 = y_list[y_range_index1].tolist()
    else:
        y_range1 = []
    if info_level > 2:
        print p1
        print 'x:', x_list, x_range1, 'y:', y
        print 'y:', y_list, y_range1, 'x:', x
    if x_range1 and y_range1:
        return x_range1, y_range1

    x_list, ax_list = get_x_a_list(info_map, p2, y, config=config)
    x_range_index2 = find_neighbor_index(x_list, x)
    y_list, ay_list = get_y_a_list(info_map, p2, x, config=config)
    y_range_index2 = find_neighbor_index(y_list, y)
    if x_range_index2:
        x_range2 = x_list[x_range_index2].tolist()
    else:
        x_range2 = []
    if y_range_index2:
        y_range2 = y_list[y_range_index2].tolist()
    else:
        y_range2 = []
    if info_level > 2:
        print p2
        print 'x:', x_list, x_range2, 'y:', y
        print 'y:', y_list, y_range2, 'x:', x
    if x_range2 and y_range2:
        return x_range2, y_range2

    if x_range1 and y_range2:
        return x_range1, y_range2
    if x_range2 and y_range1:
        return x_range2, y_range1
    if x_range1:
        return x_range1, []
    if y_range1:
        return [], y_range1
    if x_range2:
        return x_range2, []
    if y_range2:
        return [], y_range2

    return [], []


def find_simulation(info_map, phase, coord):
    if phase not in info_map:
        return None
    if tuple(coord) not in info_map[phase]:
        return None
    return info_map[phase][tuple(coord)]  # info is a simulation instance


def predict_simulations(info_map, config, phase_coordlist_dict, order=True,
                        info_level=-1):
    xaxis = config.xaxis
    yaxis = config.yaxis
    sim_list = []
    for phase, coord_list in phase_coordlist_dict.iteritems():
        coord_array_predict = np.array(coord_list)

        xs, ys, a_list = find_valid_coordinates_and_sizes(info_map, phase,
                                                          config, info_level)
        # Simply ignore this phase if there are no valid simulations
        # of this phase.
        if len(xs) < 2:
            continue

        coord_array_exist = np.array([xs, ys]).T
        neighbor_finder = cKDTree(coord_array_exist)
        distances, indices = neighbor_finder.query(coord_array_predict)
        coord_array_neighbor = coord_array_exist[indices]

        if phase != 'DIS':
            # Uncomment following lines to enable additional interpolation
            #
            # xmin, xmax = np.amin(xs), np.amax(xs)
            # ymin, ymax = np.amin(ys), np.amax(ys)
            # xi = np.linspace(xmin, xmax, 11)
            # yi = np.linspace(ymin, ymax, 11)
            # X, Y = np.meshgrid(xi, yi)
            # Z = griddata((xs, ys), a_list, (X, Y), method='linear')
            # zz = Z.flatten()
            # ind_nan = np.logical_not(np.isnan(zz))
            # xx = xs + list(X.flatten()[ind_nan])
            # yy = ys + list(Y.flatten()[ind_nan])
            # zz = a_list + list(zz[ind_nan])
            # size_predictor = interp2d(xx, yy, zz, kind='linear')
            size_predictor = interp2d(xs, ys, a_list, kind='linear')

        for i in xrange(len(coord_list)):
            x, y = list(coord_array_predict[i])
            sim = Simulation()
            sim.phase = phase
            sim.xaxis = xaxis
            sim.yaxis = yaxis
            sim.order = order
            sim.coord = [x, y]
            sim.neighbor_coord = list(coord_array_neighbor[i])
            if phase != 'DIS':
                sim.a = size_predictor(x, y).item()
            else:
                sim.a = 1.0
            sim_list.append(sim)

    return sim_list


def interpolate_simulations(info_map, phase_pair, coord, config,
                            info_level=-1):
    xaxis = config.xaxis
    yaxis = config.yaxis
    p1, p2 = phase_pair
    x, y = coord
    phases = [p1, p2]
    for boundary_info in config.predictor.boundary:
        # Must use key access instead of attribute
        # Otherwise it will return list of tuples
        # boundary_info['pairs'] returns
        #       [['HEX', 'LAM']]
        # while boundary_info.pairs returns
        #       (('HEX', 'LAM'),)
        if [p1, p2] in boundary_info['pairs']:
            phases = phases + list(boundary_info.extra)
            break
        if [p2, p1] in boundary_info['pairs']:
            phases = phases + list(boundary_info.extra)
            break
    mode = config.predictor.mode
    preferred = config.predictor.preferred
    precision_x = config.predictor.precision_x
    precision_y = config.predictor.precision_y
    n = config.predictor.interpolation.n

    x_range, y_range = find_range(info_map, phase_pair, coord, config,
                                  info_level)
    if not x_range and not y_range:
        return []

    sim_list = []
    for phase in phases:
        if info_level > 2:
            print phase
        if (preferred.upper() == 'Y' and y_range) or not x_range:
            var_list = find_interp_list(y_range, y, n, precision_y, mode)
            var_array, a_array = predict_size(info_map, phase, x, var_list,
                                              xory='y', config=config,
                                              info_level=info_level)
            var_array = format_array_by_precision(var_array, precision_y)
            var_array, index = np.unique(var_array, return_index=True)
            a_array = a_array[index]
            if info_level > 2:
                print 'interp var:', var_list
                print 'predict var:', var_array
                print 'predict size:', a_array
            for i in xrange(var_array.size):
                coord = [x, var_array[i]]
                # if simulatin already exists, skip creating this simulation
                # no matter whether the existed simulation is valid.
                if find_simulation(info_map, phase, coord) is not None:
                    continue
                sim = Simulation()
                sim.phase = phase
                sim.xaxis = xaxis
                sim.yaxis = yaxis
                sim.order = True
                sim.coord = coord
                sim.a = a_array[i]
                if y - y_range[0] < y_range[1] - y:
                    sim.neighbor_coord = [x, y_range[0]]
                else:
                    sim.neighbor_coord = [x, y_range[1]]
                sim_list.append(sim)
        else:
            var_list = find_interp_list(x_range, x, n, precision_x, mode)
            var_array, a_array = predict_size(info_map, phase, y, var_list,
                                              xory='x', config=config,
                                              info_level=info_level)
            var_array = format_array_by_precision(var_array, precision_x)
            var_array, index = np.unique(var_array, return_index=True)
            a_array = a_array[index]
            if info_level > 2:
                print 'interp:', var_list
                print 'size:', var_array, a_array
            for i in xrange(var_array.size):
                coord = [var_array[i], y]
                # if simulatin already exists, skip creating this simulation
                # no matter whether the existed simulation is valid.
                if find_simulation(info_map, phase, coord) is not None:
                    continue
                sim = Simulation()
                sim.phase = phase
                sim.xaxis = xaxis
                sim.yaxis = yaxis
                sim.order = False
                sim.coord = coord
                sim.a = a_array[i]
                if x - x_range[0] < x_range[1] - x:
                    sim.neighbor_coord = [x_range[0], y]
                else:
                    sim.neighbor_coord = [x_range[1], y]
                sim_list.append(sim)
    return sim_list


def find_datadir(sim, config, basedir='./', info_level=-1):
    '''
    Return the datadir based on the coordination:
    if Simulation.order is True
        <xaxis><x>/<yaxis><y>
    if Simulation.order is False
        <yaxis><y>/<xaxis><x>
    '''
    xaxis = config.xaxis
    yaxis = config.yaxis
    precision_x = config.predictor.precision_x
    precision_y = config.predictor.precision_y
    phase = sim.phase

    x, y = sim.coord
    x_str = format_number_for_dirname(x, precision_x)
    xdir = xaxis + x_str
    y_str = format_number_for_dirname(y, precision_y)
    ydir = yaxis + y_str
    if sim.order:
        datadir = os.path.join(basedir, xdir, ydir, phase)
    else:
        datadir = os.path.join(basedir, ydir, xdir, phase)

    return datadir


def prepare_param_file(sim, config, basedir='./', info_level=-1):
    '''
    The project configuration file should contain an option
        config['predictor']['param_dummy']
    which contains a dictionary of dummy_key : val_expr pair.
    dummy_key should present in the parameter template file which holds the position to be replaced.
    val_expr is an expression to evaluate the value which will replace the corresponding dummy_key in the parameter template file.
    The allowed variables in val_expr are
        ['a', 'x', 'y']
    Example:
        predictor:
            param_dummy:
                DUMMY_a:        a
                DUMMY_phih:     x
                DUMMY_phic:     1.0 - x
                DUMMY_xN:       y
    '''
    template = config.predictor.template
    datadir = find_datadir(sim, config, basedir, info_level)
    paramfilename = config.infiles.parameter
    phase = sim.phase

    paramfile = os.path.join(datadir, paramfilename)
    param_temp_name = phase + template.parameter
    param_tempfile = os.path.join(template.path, param_temp_name)

    with open(param_tempfile, "rb") as f:
        lines = f.readlines()

    a = sim.a  # this will appear in val_expr
    precision_x = config.predictor.precision_x
    precision_y = config.predictor.precision_y
    x, y = sim.coord
    x_str = format_number_for_dirname(x, precision_x)
    y_str = format_number_for_dirname(y, precision_y)
    x = float(x_str)  # this will appear in val_expr
    y = float(y_str)  # this will appear in val_expr
    dummies = config.predictor.param_dummy
    with open(paramfile, "w") as f:
        for line in lines:
            for key, val_expr in dummies.iteritems():
                val = eval(val_expr)
                val_str = str(val)
                line = re.sub(key, val_str, line)
            f.write(line)
    if info_level > 2:
        print "Parameter file created:", paramfile
        print "Based on:", param_tempfile


def prepare_seed_file(sim, config, basedir='./', info_level=-1):
    template = config.predictor.template
    datadir = find_datadir(sim, config, basedir, info_level)
    seedfilename = config.infiles.seed
    seedsourcename = config.predictor.seed_source
    phase = sim.phase
    xaxis = config.xaxis
    yaxis = config.yaxis

    seedfile = os.path.join(datadir, seedfilename)
    seed_temp_name = phase + template.seed
    seed_tempfile = os.path.join(template.path, seed_temp_name)
    nx, ny = sim.neighbor_coord
    nx_str = format_number_for_dirname(nx)
    nxdir = xaxis + nx_str
    ny_str = format_number_for_dirname(ny)
    nydir = yaxis + ny_str
    seed_sourcefile_xy = os.path.join(basedir, nxdir, nydir,
                                      phase, seedsourcename)
    seed_sourcefile_yx = os.path.join(basedir, nydir, nxdir,
                                      phase, seedsourcename)
    if os.path.isfile(seed_sourcefile_xy):
        seed_sourcefile = seed_sourcefile_xy
    elif os.path.isfile(seed_sourcefile_yx):
        seed_sourcefile = seed_sourcefile_yx
    else:
        seed_sourcefile = seed_tempfile

    copyfile(seed_sourcefile, seedfile)

    if info_level > 2:
        print "Seed file created:", seedfile
        print "Based on:", seed_sourcefile


def prepare_submit_file(sim, config, basedir='./', info_level=-1):
    xaxis = config.xaxis
    yaxis = config.yaxis
    precision_x = config.predictor.precision_x
    precision_y = config.predictor.precision_y
    phase = sim.phase
    x, y = sim.coord
    x_str = format_number_for_dirname(x, precision_x)
    y_str = format_number_for_dirname(y, precision_y)

    template = config.predictor.template
    datadir = find_datadir(sim, config, basedir, info_level)
    phase = sim.phase
    subfilename = config.infiles.submission
    sub_temp_name = phase + template.submission
    subfile = os.path.join(datadir, subfilename)
    sub_tempfile = os.path.join(template.path, sub_temp_name)
    if not os.path.isfile(sub_tempfile):
        sub_tempfile = os.path.join(template.path, subfilename)
    paramfilename = config.infiles.parameter
    logfilename = config.infiles.log
    exe_serial = config.predictor.executable.serial
    exe_paralell = config.predictor.executable.paralell

    with open(sub_tempfile, "rb") as f:
        lines = f.readlines()

    jobname = phase + '-' + xaxis + x_str + '-' + yaxis + y_str
    jobparam = paramfilename
    joblog = logfilename
    if phase == 'DIS':
        jobexe = exe_serial
    else:
        jobexe = exe_paralell
    with open(subfile, "w") as f:
        for line in lines:
            line = re.sub("DUMMY_name", jobname, line)
            line = re.sub("DUMMY_param", jobparam, line)
            line = re.sub("DUMMY_log", joblog, line)
            line = re.sub("DUMMY_exe", jobexe, line)
            f.write(line)

    if info_level > 2:
        print "submission script created:", subfile
        print "Based on:", sub_tempfile


def prepare_simulation_jobs(sim_list, config, basedir='./', info_level=-1):
    seed_exclude_list = config.predictor.seed_exclude
    for sim in sim_list:
        # prepare the datadir
        datadir = find_datadir(sim, config, basedir, info_level)
        if not os.path.exists(datadir):
            os.makedirs(datadir)
        # prepare parameter file
        prepare_param_file(sim, config, basedir, info_level)
        # prepare seed file
        if sim.phase not in seed_exclude_list:
            prepare_seed_file(sim, config, basedir, info_level)
        # prepare submission script
        prepare_submit_file(sim, config, basedir, info_level)


def upload_simulation_jobs(sim_list, config, basedir='./', info_level=-1):
    '''
    Upload prepared simulation jobs to the server using Rsync.
    '''
    # Currently we only support the first server in the predictor.server list
    server = config.predictor.server[0]
    server_address = server.address
    # Ensure there is a trailing os.path.sep for correct Rsync behavior
    server_basedir = os.path.join(server.basedir, '')
    sync = ['rsync']  # TODO: support other sync tools in configuration file
    sync_flag = ['-amuv']  # -u only transfer newer files
    include_list = ["--include=*/"]
    for sim in sim_list:
        datadir = find_datadir(sim, config, '', info_level)
        datadir, base = os.path.split(datadir)  # strip <phase> folder
        include = '--include=' + datadir + '/**'
        include_list.append(include)
    parsedfilename = config.outfiles.point_data
    exclude1 = ['--exclude=' + parsedfilename]
    exclude2 = ['--exclude=*']
    cwd = [os.path.join(basedir, '')]
    server = [server_address + ':' + server_basedir]
    args = sync + sync_flag + exclude1 + include_list + exclude2 + cwd + server
    if info_level > -1:
        print "Ready to upload simulation jobs to server via Rsync:"
        print args
    response, err_msg = run_command(args)
    if info_level > -1:
        print "Rsync returns with following messages."
        print "Rsync response:"
        print response
    if info_level > 2:
        print "Rsync error message:"
        print err_msg


def download_simulation_jobs(config, basedir='./', info_level=-1):
    # Currently we only support the first server in the predictor.server list
    server = config.predictor.server[0]
    server_address = server.address
    # Ensure there is a trailing os.path.sep for correct Rsync behavior
    server_basedir = os.path.join(server.basedir, '')
    server = [server_address + ':' + server_basedir]
    sync = ['rsync']  # TODO: support other sync tools in configuration file
    sync_flag = ['-amuv']  # -u only transfer newer files
    xaxis = config.xaxis
    yaxis = config.yaxis
    include_list = [
        '--include=*/',
        '--include=' + xaxis + '*/**',
        '--include=' + yaxis + '*/**'
    ]
    parsedfilename = config.outfiles.point_data
    exclude1 = ['--exclude=' + parsedfilename]
    exclude2 = ['--exclude=*']
    cwd = [os.path.join(basedir, '')]
    args = sync + sync_flag + exclude1 + include_list + exclude2 + server + cwd
    if info_level > -1:
        print "Ready to download simulation jobs from server via Rsync:"
        print args
    response, err_msg = run_command(args)
    if info_level > -1:
        print "Rsync returns with following messages."
        print "Rsync response:"
        print response
    if info_level > 2:
        print "Rsync error message:"
        print err_msg


def submit_simulation_jobs(sim_list, config, basedir='./', info_level=-1):
    # Currently we only support the first server in the predictor.server list
    server = config.predictor.server[0]
    server_address = server.address
    server_basedir = server.basedir
    server = [server_address]
    ssh = ['ssh']
    ssh_flag = ['-t', '-t']  # to keep connection
    for sim in sim_list:
        datadir = find_datadir(sim, config, '', info_level)
        datadir = os.path.join(server_basedir, datadir)
        cd = 'cd ' + datadir + ';'
        subfilename = config.infiles.submission
        qsub = 'qsub ' + subfilename
        # cmd = ['qsub ' + os.path.join(server_basedir, datadir, subfilename)]
        cmd = [cd + qsub]
        args = ssh + ssh_flag + server + cmd
        if info_level > -1:
            print "Ready to submit simulation jobs:"
            print args
        response, err_msg = run_command(args)
        if info_level > -1:
            print "SSH returns with following messages."
            print "SSH response:"
            print response
        if info_level > 2:
            print "SSH error message:"
            print err_msg
        time.sleep(0.2)
