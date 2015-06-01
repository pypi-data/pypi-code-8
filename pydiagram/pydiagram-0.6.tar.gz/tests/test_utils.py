# -*- coding: utf-8 -*-
"""
test_utils.py
=============

Unit tests for pydiagram.utils using ``py.test``.

"""
import os
import time

import numpy as np
import pytest  # NOQA

import pydiagram


def test_find_index():
    a = np.array([14., 14.2, 14.4, 14.6, 14.8,
                  15., 15.2, 15.4, 15.6, 15.8, 16.])
    lim = [14, 16]
    i, j = pydiagram.find_index(a, lim)
    assert i == 0
    assert j == a.size - 1

    lim = [10, 14.4]
    i, j = pydiagram.find_index(a, lim)
    assert i == 0
    assert j == 2

    lim = [10, 14.5]
    i, j = pydiagram.find_index(a, lim)
    assert i == 0
    assert j == 2

    lim = [14.1, 15.9]
    i, j = pydiagram.find_index(a, lim)
    assert i == 1
    assert j == a.size - 2

    lim = [14.1, 20]
    i, j = pydiagram.find_index(a, lim)
    assert i == 1
    assert j == a.size - 1


def test_find_neighbor_index():
    a = np.array([14., 14.2, 14.4, 14.6, 14.8,
                  15., 15.2, 15.4, 15.6, 15.8, 16.])
    val = 13.0
    ret = pydiagram.find_neighbor_index(a, val)
    assert len(ret) == 0

    val = 14.0
    i, j = pydiagram.find_neighbor_index(a, val)
    assert i == 0
    assert j == 1

    val = 14.5
    i, j = pydiagram.find_neighbor_index(a, val)
    assert i == 2
    assert j == 3

    val = 15.0
    i, j = pydiagram.find_neighbor_index(a, val)
    assert i == 4
    assert j == 6

    val = 16.0
    i, j = pydiagram.find_neighbor_index(a, val)
    assert i == a.size - 2
    assert j == a.size - 1

    val = 17.0
    ret = pydiagram.find_neighbor_index(a, val)
    assert len(ret) == 0

    a = np.array([])
    val = 0.0
    ret = pydiagram.find_neighbor_index(a, val)
    assert len(ret) == 0

    a = np.array([1.0])
    val = 0.0
    ret = pydiagram.find_neighbor_index(a, val)
    assert len(ret) == 0

    a = np.array([1.0, 2.0])
    val = 1.0
    i, j = pydiagram.find_neighbor_index(a, val)
    assert i == 0
    assert j == 1

    val = 1.5
    i, j = pydiagram.find_neighbor_index(a, val)
    assert i == 0
    assert j == 1

    val = 2.0
    i, j = pydiagram.find_neighbor_index(a, val)
    assert i == 0
    assert j == 1


def test_find_interp_list():
    range = np.array([14.2, 14.4])
    val = 14.3
    n = 4
    resolution = 0.3
    ret = pydiagram.find_interp_list(range, val, n, resolution, 'boundary')
    assert len(ret) == 0
    ret = pydiagram.find_interp_list(range, val, n, resolution, 'regular')
    assert len(ret) == 0

    resolution = 0.1
    expect = np.array([14.26, 14.3, 14.34])
    ret = pydiagram.find_interp_list(range, val, n, resolution, 'boundary')
    assert np.allclose(ret, expect)

    expect = np.array([14.24, 14.28, 14.3, 14.32, 14.36])
    ret = pydiagram.find_interp_list(range, val, n, resolution, 'regular')
    assert np.allclose(ret, expect)


def test_find_name_value():
    folder1 = 'phi0.1'
    name, value = pydiagram.find_name_value(folder1)
    assert name == 'phi'
    assert value == 0.1

    folder2 = 'xN18'
    name, value = pydiagram.find_name_value(folder2)
    assert name == 'xN'
    assert value == 18

    folder3 = 'kappa0.5n'
    name, value = pydiagram.find_name_value(folder3)
    assert name == 'kappa'
    assert value == -0.5


def test_find_value():
    folder1 = 'phi0.1'
    value = pydiagram.find_value(folder1, 'phi')
    assert value == 0.1
    value = pydiagram.find_value(folder1, 'phih')
    assert value is None


def test_create_mark():
    markfile = 'pydiagram.mark'
    pydiagram.create_mark(markfile)
    assert os.path.exists(markfile)

    time.sleep(1)

    mtime_old = pydiagram.check_mark(markfile)
    pydiagram.create_mark(markfile)
    mtime_new = pydiagram.check_mark(markfile)
    assert mtime_new > mtime_old
    # remove just created mark file
    os.remove(markfile)


def test_check_mark():
    markfile = 'pydiagram.mark'
    try:
        os.remove(markfile)
    except:
        pass
    assert pydiagram.check_mark(markfile) is None

    pydiagram.create_mark(markfile)
    assert not pydiagram.check_mark(markfile) is None
    # remove just created mark file
    os.remove(markfile)


def test_find_F_from_log():
    logfile = 'log.DIS'
    F = pydiagram.find_F_from_log(logfile)
    assert np.isclose(F, 4.127995)

    logfile = 'log.nonexist'
    F = pydiagram.find_F_from_log(logfile)
    assert F is None


def test_find_density_from_log():
    logfile = 'log.DIS'
    phi_avg, phi_min, phi_max = pydiagram.find_density_from_log(logfile, 1.0)
    assert np.isclose(phi_avg, 0.4000)
    assert np.isclose(phi_min, 0.4000)
    assert np.isclose(phi_max, 0.4000)

    logfile = 'log.BCC'
    phi_avg, phi_min, phi_max = pydiagram.find_density_from_log(logfile,
                                                                4.1618)
    assert np.isclose(phi_avg, 0.4000)
    assert np.isclose(phi_min, 0.1804)
    assert np.isclose(phi_max, 0.9558)

    logfile = 'log.nonexist'
    phi_avg, phi_min, phi_max = pydiagram.find_density_from_log(logfile, 1.0)
    assert phi_avg is None
    assert phi_min is None
    assert phi_max is None

    logfile = 'log.BCC'
    phi_avg, phi_min, phi_max = pydiagram.find_density_from_log(logfile, 999.0)
    assert phi_avg is None
    assert phi_min is None
    assert phi_max is None


def test_find_accuracy_from_log():
    logfile = 'log.DIS'
    accuracy = pydiagram.find_accuracy_from_log(logfile, 1.0)
    assert np.isclose(accuracy, 7.93e-11, atol=1e-12)

    logfile = 'log.BCC'
    accuracy = pydiagram.find_accuracy_from_log(logfile, 4.1618)
    assert np.isclose(accuracy, 6.98e-07, atol=1e-12)

    logfile = 'log.nonexist'
    accuracy = pydiagram.find_accuracy_from_log(logfile, 1.0)
    assert accuracy == 1.0

    logfile = 'log.BCC'
    accuracy = pydiagram.find_accuracy_from_log(logfile, 999.0)
    assert accuracy == 1.0


def test_find_aF_from_data():
    datafile = 'scft_out_cell.mat'
    alist, Flist = pydiagram.find_aF_from_data(datafile)
    Flist_true = np.array([4.08053545, 4.07920179, 4.07915675, 4.07884783,
                           4.07890350, 4.07889610, 4.07884783])
    alist_true = np.array([3.9, 4., 4.161803, 4.083692, 4.051725,
                           4.113528, 4.083692])
    assert np.allclose(alist, alist_true)
    assert np.allclose(Flist, Flist_true)

    datafile = 'nonexist.mat'
    alist, Flist = pydiagram.find_aF_from_data(datafile)
    assert alist is None
    assert Flist is None
