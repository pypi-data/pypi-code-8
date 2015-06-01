# -*- coding: utf-8 -*-
"""
test_diagram.py
==============

Testing pydiagram.diagram.

"""
import os.path
from pprint import pprint

import pydiagram
import yaml


def test_get_diagram():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    diagram = pydiagram.get_diagram(data_path, is_parsed=True, info_level=3)
    pprint(diagram)


def test_get_info_map():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True, info_level=3)
    pprint(info_map)


def test_refine_diagram():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True, info_level=-1)
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)
    diagram = pydiagram.get_diagram_from_info_map(info_map, config)
    boundary = pydiagram.get_boundary(diagram, info_map, info_level=-1)

    sim_list = pydiagram.refine_diagram(boundary, info_map, config,
                                        info_level=3)
    for sim in sim_list:
        pprint(sim.__dict__)


def test_diagram_polyorder():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4"
    diagram, info_map, aF_map = pydiagram.get_diagram('phi', 'xN', data_path)

    print 'Diagram: '
    print diagram
    print 'info_map: '
    print info_map
    print 'aF_map: '
    print aF_map


def test_diagram_io():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4"
    from_file = False
    if from_file:
        f = os.path.join(data_path, 'diagram.p')
        diagram = pydiagram.load_diagram(f)
        f = os.path.join(data_path, 'info_map.p')
        info_map = pydiagram.load_diagram(f)
        f = os.path.join(data_path, 'aF_map.p')
        aF_map = pydiagram.load_diagram(f)
    else:
        diagram, info_map, aF_map = pydiagram.get_diagram('phi', 'xN',
                                                          data_path)

    # print diagram
    # f = os.path.join(data_path, 'diagram.p')
    # pydiagram.save_diagram(diagram, f)
    # print pydiagram.load_diagram(f)
    yaml_file = os.path.join(data_path, 'diagram.yaml')
    with open(yaml_file, 'w') as f:
        yaml.safe_dump(diagram, f, canonical=False)

    pprint(info_map, width=1)
    # f = os.path.join(data_path, 'info_map.p')
    # pydiagram.save_diagram(info_map, f)
    # print pydiagram.load_diagram(f)
    yaml_file = os.path.join(data_path, 'info_map.yaml')
    with open(yaml_file, 'w') as f:
        yaml.safe_dump(info_map, f, canonical=False)

    # print aF_map
    # f = os.path.join(data_path, 'aF_map.p')
    # pydiagram.save_diagram(aF_map, f)
    # print pydiagram.load_diagram(f)
    # yaml_file = os.path.join(data_path, 'aF_map.yaml')
    # with open(yaml_file, 'w') as f:
    #    yaml.dump(aF_map, f, canonical=False)


def test_diagram_from_info_map():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4"
    from_file = True
    if from_file:
        f = os.path.join(data_path, 'diagram.p')
        diagram = pydiagram.load_diagram(f)
        f = os.path.join(data_path, 'info_map.p')
        info_map = pydiagram.load_diagram(f)
        f = os.path.join(data_path, 'aF_map.p')
        aF_map = pydiagram.load_diagram(f)
    else:
        diagram, info_map, aF_map = pydiagram.get_diagram('phi', 'xN',
                                                          data_path)

    # pprint(diagram)
    f = 'test.dgm'
    xname, yname, info_map = pydiagram.load_dgm(f)
    diagram_from_info_map = pydiagram.get_diagram_from_info_map(info_map)
    # pprint(diagram_from_info_map)
    for phase in diagram:
        print phase
        coord_list1 = sorted(diagram[phase])
        coord_list2 = sorted(diagram_from_info_map[phase])
        size1 = len(coord_list1)
        size2 = len(coord_list2)
        if size1 > size2:
            size = size1
        else:
            size = size2
        for i in xrange(size):
            if i < size1 and i < size2:
                print coord_list1[i], coord_list2[i]
            elif i < size1 and i >= size2:
                print coord_list1[i], 'data'
            elif i >= size1 and i < size2:
                print coord_list2[i], 'info'


if __name__ == '__main__':
    # test_get_diagram()
    # test_get_info_map()
    # test_diagram_polyorder()
    # test_diagram_io()
    # test_diagram_from_info_map()
    test_refine_diagram()
