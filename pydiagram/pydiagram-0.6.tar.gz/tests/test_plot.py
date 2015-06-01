# -*- coding: utf-8 -*-
"""
test_diagram.py
==============

Testing pydiagram.diagram.

"""
import os.path
import matplotlib.pyplot as plt
import mpltex

import pydiagram


def test_plot_diagram():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    diagram = pydiagram.get_diagram(data_path, is_parsed=True)

    markersize = 10
    allow_phase = []  # ['Gyroid', 'HEX', 'LAM']
    ignore_phase = []  # ['DIS']

    fig, ax = plt.subplots(1)
    pydiagram.plot_diagram(ax, diagram, markersize=markersize,
                           allow_phase=allow_phase, ignore_phase=ignore_phase)
    ax.legend(loc='best', ncol=2)
    plt.show()


def test_plot_boundary():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True)
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)
    diagram = pydiagram.get_diagram_from_info_map(info_map, config)
    boundary = pydiagram.get_boundary(diagram, info_map)

    phase1 = ''
    phase2 = ''
    show_boundarypoint = True
    show_boundary = False
    interp_n = 100
    interp_k = 3
    interp_s = 0
    interp_method = 'range'
    sort_axis = 'x'
    # for boundary points
    linestyle1 = mpltex.linestyle_generator(lines=[],
                                            # markers=[],
                                            hollow_styles=[])
    # for interpolated phase boundary
    linestyle2 = mpltex.linestyle_generator(lines=['-'],
                                            markers=[],
                                            hollow_styles=[])

    fig, ax = plt.subplots(1)
    if show_boundarypoint:
        pydiagram.plot_boundary_point(ax, boundary,
                                      phase1=phase1, phase2=phase2,
                                      sort_axis=sort_axis,
                                      show_label=True,
                                      **linestyle1.next())

    if show_boundary:
        pydiagram.plot_boundary(ax, boundary, phase_pair_list=[],
                                label='',
                                interp_n=interp_n,
                                interp_k=interp_k,
                                interp_s=interp_s,
                                interp_method=interp_method,
                                sort_axis=sort_axis,
                                **linestyle2.next())

    ax.legend(loc='best', ncol=2, scatterpoints=1)
    plt.show()


if __name__ == '__main__':
    # test_plot_diagram()
    test_plot_boundary()
