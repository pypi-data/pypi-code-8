# -*- coding: utf-8 -*-
"""
test_config.py
==============

Testing pydiagram.config

"""
import os.path
# from pprint import pprint

import pydiagram


def test_parse_config():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)
    print config


if __name__ == '__main__':
    test_parse_config()
