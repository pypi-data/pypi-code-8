# -*- coding: utf-8 -*-
"""
test_size.py
============

Testing pydiagram.size.

"""
import pydiagram
# import pytest


def test_get_x_separation_list():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)

    x, separation = pydiagram.get_x_separation_list(info_map, 'HEX', 18)
    print x
    print separation
    y, separation = pydiagram.get_y_separation_list(info_map, 'Gyroid', 0.3)
    print y
    print separation


if __name__ == '__main__':
    test_get_x_separation_list()
