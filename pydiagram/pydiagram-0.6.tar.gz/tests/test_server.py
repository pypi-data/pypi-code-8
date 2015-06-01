# -*- coding: utf-8 -*-
"""
test_server.py
==============

Testing pydiagram.server module.

"""
import os.path

import pydiagram
# import pytest


def test_find_server():
    data_path = "/Users/lyx/Sandbox/pydiagram_test/"
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)

    server = pydiagram.find_server(config, info_level=3)
    print server


if __name__ == '__main__':
    test_find_server()
