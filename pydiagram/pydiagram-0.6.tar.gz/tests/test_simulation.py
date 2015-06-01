# -*- coding: utf-8 -*-
"""
test_diagram.py
==============

Testing pydiagram.diagram.

"""
import os.path
from pprint import pprint

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

    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/xN18/phi0.3/HEX"
    datafile = os.path.join(data_path, 'data.yml')
    sim2 = pydiagram.Simulation()
    sim2.loadfile(datafile)
    pprint(sim2.__dict__)
    print 'sim2 == sim?', sim == sim2

    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4/xN18/phi0.3/LAM"
    datafile = os.path.join(data_path, 'data.yml')
    sim3 = pydiagram.Simulation()
    sim3.loadfile(datafile)
    pprint(sim3.__dict__)
    print 'sim3 == sim?', sim == sim3

    sim2.phase = 'Gyroid'
    print 'modified sim2 == sim?', sim == sim2

    print 'modified sim2 in [sim, sim3]?', sim2 in [sim, sim3]


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
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4_zetaN1000"
    # info_map = pydiagram.get_info_map(data_path, is_parsed=True)
    info_map_file = os.path.join(data_path, 'info_map.p')
    info_map = pydiagram.load(info_map_file)
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)

    phase_pair = ('HEX', 'LAM')
    coord = [0.36, 16.800001447747679]
    sim_list = pydiagram.interpolate_simulations(info_map, phase_pair,
                                                 coord, config,
                                                 info_level=3)
    print 'Predicted simulations for', phase_pair, 'at', coord, ':'
    for sim in sim_list:
        pprint(sim.__dict__)
    if not sim_list:
        print 'None'


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
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4_zetaN1000"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)

    entry = config.predictor.manual[0]

    pcd1, pcd2, spd = pydiagram.parse_config_predictor_manual(entry)
    print 'pcd1:'
    pprint(pcd1)
    print 'pcd2:'
    pprint(pcd2)
    print 'spd:'
    pprint(spd)

    sim_list = pydiagram.predict_simulations(info_map, config,
                                             pcd1, True, spd,
                                             info_level=-1)
    sim_list += pydiagram.predict_simulations(info_map, config,
                                              pcd2, False, spd,
                                              info_level=-1)
    print 'manual added simulations:'
    for sim in sim_list:
        pprint(sim.__dict__)

    sim_list = pydiagram.predict_simulations(info_map, config,
                                             {'Gyroid': [(0.36, 16.8)]},
                                             order=True,
                                             size_predictor_dict={},
                                             info_level=3)
    print 'Automatic generated simulations:'
    for sim in sim_list:
        pprint(sim.__dict__)


def test_filter_simulations():
    sim1 = pydiagram.PolyFTSSimulation()
    sim1.phase = 'HEX'
    sim1.coord = [0.3, 18.0]

    sim2 = pydiagram.PolyFTSSimulation()
    sim2.phase = 'LAM'
    sim2.coord = [0.3, 18.0]

    sim3 = pydiagram.PolyFTSSimulation()
    sim3.phase = 'Gyroid'
    sim3.coord = [0.3, 18.0]

    sim4 = pydiagram.PolyFTSSimulation()
    sim4.phase = 'HEX'
    sim4.coord = [0.32, 18.0]

    sim5 = pydiagram.PolyFTSSimulation()
    sim5.phase = 'HEX'
    sim5.coord = [0.3, 18.2]

    sim6 = pydiagram.PolyFTSSimulation()
    sim6.phase = 'LAM'
    sim6.coord = [0.3, 18.0]

    sim_list = [sim1, sim2, sim3, sim4, sim5, sim6]
    sim_list = pydiagram.filter_simulations(sim_list)
    for sim in sim_list:
        print sim.__dict__


def test_find_simulation():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4_zetaN1000"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)
    # config_file = os.path.join(data_path, 'config.yml')
    # config = pydiagram.parse_config(config_file)

    print pydiagram.find_simulation(info_map, 'Gyroid', [0.36, 16.8])


if __name__ == '__main__':
    # test_find_invalid_simulations()
    # test_transform_invalid_simulations_to_diagram()
    # test_Simulation()
    # test_PolyFTSSimulation()
    # test_PolyorderSimulation()
    test_interpolate_simulations()
    # test_prepare_simulation_jobs()
    # test_predict_simulations()
    # test_filter_simulations()
    # test_find_simulation()
