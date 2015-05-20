# -*- coding: utf-8 -*-
"""
test_size.py
============

Testing pydiagram.size.

"""
import os.path

import pydiagram
# import pytest


def test_get_x_a_list():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)

    x, a = pydiagram.get_x_a_list(info_map, 'HEX', 18)
    print x
    print a
    y, a = pydiagram.get_y_a_list(info_map, 'Gyroid', 0.3)
    print y
    print a


def test_predict_size():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)

    x, a = pydiagram.predict_size(info_map, 'HEX', 18,
                                  [0.2, 0.22, 0.24, 0.26, 0.28, 0.3],
                                  xory='x',
                                  config=config,
                                  info_level=3)
    print x
    print a
    y, a = pydiagram.predict_size(info_map, 'HEX', 0.3,
                                  [14, 15, 16, 17],
                                  xory='y',
                                  config=config,
                                  info_level=3)
    print y
    print a


if __name__ == '__main__':
    # test_get_x_a_list()
    test_predict_size()
