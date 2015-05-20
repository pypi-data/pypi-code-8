# -*- coding: utf-8 -*-
"""
test_energy.py
==============

Testing pydiagram.energy.

"""
import os.path
from pprint import pprint

import pydiagram
# import pytest


def test_get_x_F_list():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)
    pprint(info_map)
    # f = os.path.join(data_path, 'info_map.p')
    # info_map = pydiagram.load_diagram(f)
    x, F = pydiagram.get_x_F_list(info_map, 'HEX', 18, base='Gyroid')
    print x
    print F
    y, F = pydiagram.get_y_F_list(info_map, 'HEX', 0.3, base='DIS',
                                  info_level=1)
    print y
    print F


if __name__ == '__main__':
    test_get_x_F_list()
