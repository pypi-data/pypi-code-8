# -*- coding: utf-8 -*-
"""
test_diagram.py
==============

Testing pydiagram.diagram.

"""
import os.path
from pprint import pprint

import numpy as np

import pydiagram
# import pytest


def test_Simulation():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/xN18/phi0.3/Gyroid"
    datafile = os.path.join(data_path, 'data.yml')

    sim = pydiagram.Simulation()
    sim.loadfile(datafile)
    pprint(sim.__dict__)
    print sim.is_valid()
    print sim.get_coord('phi', 'xN')


def test_PolyFTSSimulation():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/xN18/phi0.3/Gyroid"
    datafile = os.path.join(data_path, 'data.yml')
    config_file = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/config.yml"
    config = pydiagram.parse_config(config_file)

    sim = pydiagram.PolyFTSSimulation()
    sim.loadfile(datafile)
    pprint(sim.__dict__)
    print sim.is_valid()
    print sim.is_valid(config)
    print sim.get_coord('xN', 'phi')


def test_PolyorderSimulation():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4/phi0/xN14.6/FCC"
    datafile = os.path.join(data_path, 'data.yml')
    config_file = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4/config.yml"
    config = pydiagram.parse_config(config_file)

    sim = pydiagram.PolyorderSimulation()
    sim.loadfile(datafile)
    pprint(sim.__dict__)
    print sim.is_valid()
    print sim.is_valid(config)
    print sim.get_coord('xN', 'phi')


def test_find_invalid_simulations():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)
    diagram = pydiagram.get_diagram_from_info_map(info_map, config)

    isim = pydiagram.find_invalid_simulations(info_map)
    print 'All invalid simulations:'
    pprint(isim)

    isim = pydiagram.find_invalid_simulations_in_diagram(diagram, info_map)
    print 'Invalid simulations in diagram:'
    pprint(isim)


def test_transform_invalid_simulations_to_diagram():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)

    isim = pydiagram.find_invalid_simulations(info_map)
    diagram_na = pydiagram.transform_invalid_simulations_to_diagram(isim)
    print 'Diagram for all invalid simulations:'
    pprint(diagram_na)


def test_interpolate_simulations():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)

    phase_pair = ('DIS', 'HEX')
    coord = [0.040268141435304015, 20.0]
    sim_list = pydiagram.interpolate_simulations(info_map, phase_pair,
                                                 coord, config,
                                                 info_level=3)
    for sim in sim_list:
        pprint(sim.__dict__)


def test_prepare_simulation_jobs():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=False)
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)
    # phase_pair = ('DIS', 'HEX')
    # coord = [0.040268141435304015, 20.0]
    # sim_list = pydiagram.interpolate_simulations(info_map, phase_pair,
    #                                              coord, config)
    diagram = pydiagram.get_diagram_from_info_map(info_map, config)
    boundary = pydiagram.get_boundary(diagram, info_map)
    sim_list = pydiagram.refine_diagram(boundary, info_map, config)

    pydiagram.prepare_simulation_jobs(sim_list, config,
                                      data_path, info_level=3)


def test_predict_simulations():
    data_path = "/Users/lyx/Sandbox/pydiagram_test/"
    info_map = pydiagram.get_info_map(data_path, is_parsed=False)
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)

    pcd1, pcd2 = pydiagram.parse_config_predictor_manual(config)
    pprint(pcd1)
    pprint(pcd2)

    sim_list = pydiagram.predict_simulations(info_map, config,
                                             pcd1, True,
                                             info_level=-1)
    sim_list += pydiagram.predict_simulations(info_map, config,
                                              pcd2, False,
                                              info_level=-1)
    for sim in sim_list:
        pprint(sim.__dict__)


if __name__ == '__main__':
    # test_find_invalid_simulations()
    # test_transform_invalid_simulations_to_diagram()
    # test_Simulation()
    # test_PolyFTSSimulation()
    # test_PolyorderSimulation()
    # test_interpolate_simulations()
    # test_prepare_simulation_jobs()
    test_predict_simulations()
