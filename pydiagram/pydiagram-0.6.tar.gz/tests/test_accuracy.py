# -*- coding: utf-8 -*-
"""
test_size.py
============

Testing pydiagram.size.

"""
import pydiagram
# import pytest


def test_get_x_accuracy_list():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)

    x, accuracy = pydiagram.get_x_accuracy_list(info_map, 'HEX', 18)
    print x
    print accuracy
    y, accuracy = pydiagram.get_y_accuracy_list(info_map, 'HEX', 0.3)
    print y
    print accuracy


if __name__ == '__main__':
    test_get_x_accuracy_list()
