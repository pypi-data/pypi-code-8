# -*- coding: utf-8 -*-
"""
test_diagram.py
==============

Testing pydiagram.diagram.

"""
import os.path
from pprint import pprint

import pydiagram


def test_parse():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    pydiagram.parse(data_path)


def test_process_phase_dirs_polyfts():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/phi0.092/xN23.28"
    config_file = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/config.yml"
    config = pydiagram.parse_config(config_file)
    pydiagram.io.process_phase_dirs_polyfts(config, data_path,
                                            'phi', 'xN', (0.092, 23.28), 4)


def test_parse_density_polyfts():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/xN26/phi0.095/HEX"
    densityfile = os.path.join(data_path, 'density.dat')
    print pydiagram.io.parse_density_polyfts(densityfile)


def test_parse_error_polyfts():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/phi0.15/xN18.48/HEX"
    errorfile = os.path.join(data_path, 'error_report.dat')
    print pydiagram.io.parse_error_polyfts(errorfile)


def test_parse_status_polyfts():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/xN18/phi0.3/Gyroid"
    statusfile = os.path.join(data_path, 'STATUS')
    print pydiagram.io.parse_status_polyfts(statusfile)


def test_parse_result_polyfts():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/xN26/phi0.095/HEX"
    datafile = os.path.join(data_path, 'operators.dat')
    print pydiagram.io.parse_result_polyfts(datafile, 3)


def test_parse_result_polyorder():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4/phi0.3/xN18/Gyroid"
    datafile = os.path.join(data_path, 'scft_out_cell.mat')
    print pydiagram.io.parse_result_polyorder(datafile, info_level=3)


def test_parse_log_polyorder():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4/phi0.3/xN18"
    phase = 'Gyroid'
    a = 9.5
    datafile = os.path.join(data_path, phase, 'log')
    print pydiagram.io.parse_log_polyorder(datafile, phase, a, info_level=3)


def test_parse_density_polyorder():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4/phi0.3/xN18/Gyroid"
    datafile = os.path.join(data_path, 'scft_out_min.mat')
    print pydiagram.io.parse_density_polyorder(datafile, info_level=3)


def test_process_phase_dirs_polyorder():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4/phi0.3/xN18"
    config_file = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4/config.yml"
    config = pydiagram.parse_config(config_file)
    pydiagram.io.process_phase_dirs_polyorder(config, data_path,
                                              'phi', 'xN', (0.3, 18), 4)


def test_list_all_data_dir():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    names = ['phi', 'xN']
    # print pydiagram.list_all_data_dir(data_path, 'phi', 'xN',
    #                                   ['xN'], ['phi'])
    print pydiagram.list_all_data_dir(data_path, 'phi', 'xN', names, names)


def test_load_dgm():
    f = 'phase_diagram.dgm'
    xaxis, yaxis, info_map = pydiagram.load_dgm(f, info_level=3)
    print xaxis
    print yaxis
    pprint(info_map)


def test_dump_dgm():
    # data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    # info_map = pydiagram.get_info_map(data_path, is_parsed=True)
    # config_file = os.path.join(data_path, 'config.yml')
    # config = pydiagram.parse_config(config_file)

    f_in = 'phase_diagram.dgm'
    xaxis, yaxis, info_map = pydiagram.load_dgm(f_in)

    f = 'test.dgm'
    pydiagram.dump_dgm(xaxis, yaxis, info_map, dgmfile=f,
                       exclude_invalid=False, config={})


if __name__ == '__main__':
    # test_load_dgm()
    # test_dump_dgm()
    # test_list_all_data_dir()
    # test_parse_result_polyfts()
    # test_parse_status_polyfts()
    # test_parse_error_polyfts()
    # test_parse_density_polyfts()
    test_process_phase_dirs_polyfts()
    # test_parse_result_polyorder()
    # test_parse_log_polyorder()
    # test_parse_density_polyorder()
    # test_process_phase_dirs_polyorder()
    # test_parse()
