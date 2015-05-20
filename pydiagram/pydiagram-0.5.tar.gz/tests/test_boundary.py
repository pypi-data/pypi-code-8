# -*- coding: utf-8 -*-
"""
test_boundary.py
===============

Testing pydiagram.boundary.

"""
import os.path
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline

import pydiagram


def test_boundary():
    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a_polyfts/diagram_xN_phi_f0.4"
    info_map = pydiagram.get_info_map(data_path, is_parsed=True, info_level=-1)
    # for phase, coord_info_dict in info_map.iteritems():
    #     for coord, info in coord_info_dict.iteritems():
    #         print phase, coord
    #         print info.__dict__
    config_file = os.path.join(data_path, 'config.yml')
    config = pydiagram.parse_config(config_file)
    diagram = pydiagram.get_diagram_from_info_map(info_map, config)

    boundary = pydiagram.get_boundary(diagram, info_map, info_level=3)
    pprint(boundary)


def test_find_boundary_normal_vector():
    '''
    The two methods for finding the normal vector of a phase boudnary:
    (1) Assume the free energy surfaces for A and B phases are F(x,y) and G(x,y), respectively. Then the free energy difference of these two phases are F(x,y)-G(x,y). Thus the projection of the intersection of the free energy surfaces of these two phases on the x-y plane is W(x,y) = F(x,y)-G(x,y) = 0. This is an implicit function of the intersection curve on the x-y plane. The normal vector is
                (dW/dx, dW/dy)
    (2) We first find the phase boundary point by linear approximation near the cross point. Then we do spline fitting to connect these phase boundary point. Assume the function of the phase boundary is y = f(x).The normal vector to the phase boundary is
                (-dy/dx, 1)
        which is normal to the tangent vector
                (1, dy/dx)
    Main conclusion:
        The above two approaches lead to similar results.
    '''
    p1 = 'HEX'
    p2 = 'Gyroid'
    x0 = 0.24
    xname, yname, info_map = pydiagram.load_dgm('phase_diagram.dgm')
    y_LG, F_LG = pydiagram.get_y_F_list(info_map, p1, x0, base=p2)
    # plt.plot(y_LG, F_LG, '-o')

    i, j = pydiagram.find_index(F_LG, [0, 0])
    print i, j
    y1 = y_LG[j]
    F3 = F_LG[j]
    y2 = y_LG[i]
    F4 = F_LG[i]

    print 'linear fit:'
    k, b = np.polyfit(y_LG[j:i+1], F_LG[j:i+1], 1)
    y0 = -b / k
    print y_LG[j], y0, y_LG[i]
    print 'spline fit:'
    spl = UnivariateSpline(y_LG, F_LG)
    yq = np.linspace(y_LG[0], y_LG[-1], 50)
    Fq = spl(yq)
    y0 = spl.roots()[0]
    F0 = spl(y0)  # should be 0
    print y_LG[j], y0, y_LG[i]

    x1 = 0.23
    y1_LG, F1_LG = pydiagram.get_y_F_list(info_map, p1, x1, base=p2)
    spl = UnivariateSpline(y1_LG, F1_LG)
    F1 = spl(y0)
    # plt.plot(y1_LG, F1_LG, '-o')

    x2 = 0.25
    y2_LG, F2_LG = pydiagram.get_y_F_list(info_map, p1, x2, base=p2)
    spl = UnivariateSpline(y2_LG, F2_LG)
    F2 = spl(y0)
    # plt.plot(y2_LG, F2_LG, '-o')

    print 'x0, x1, x2 =', x0, x1, x2
    print 'y0, y1, y2 =', y0, y1, y2
    print 'F0, F1, F2, F3, F4', F0, F1, F2, F3, F4

    # dx = x0 - x1  # also = x2 - x0
    # Fx = (F2 - F1) / (2 * dx)
    h1 = x0 - x1
    h2 = x2 - x0
    h = h1 + h2  # also = y2 - y1
    Fx = -h2/(h1*h)*F1 + (h2/(h1*h) - h1/(h2*h))*F0 + h1/(h2*h)*F2
    h1 = y0 - y1
    h2 = y2 - y0
    h = h1 + h2  # also = y2 - y1
    Fy = -h2/(h1*h)*F3 + (h2/(h1*h) - h1/(h2*h))*F0 + h1/(h2*h)*F4
    print 'Fx, Fy =', Fx, Fy

    denom = np.sqrt(Fx**2 + Fy**2)
    vx = Fx / denom
    vy = Fy / denom
    print 'vx, vy =', vx, vy

    data_path = "/Users/lyx/Google Drive/simulation/scft_ab3_a/diagram_xN_phi_f0.4"
    f = os.path.join(data_path, 'boundary.p')
    boundary = pydiagram.load_boundary(f)
    xb, yb = pydiagram.get_connected_boundary(boundary, [(p1, p2)], 'y')
    # print xb, yb
    plt.plot(xb, yb, 'o')
    xq, yq = pydiagram.interpolate_boundary(xb, yb, 50, 2, 0, 'distant')
    plt.plot(xq, yq)
    plt.show()
    xb = xb[:-5]
    yb = yb[:-5]
    xb = xb[::-1]
    yb = yb[::-1]
    spl = UnivariateSpline(xb, yb, k=4, s=0.1)
    dspl = spl.derivative()
    k = dspl(0.24)
    xt = xq
    yt = k * (xt - 0.24) + 14.7
    # plt.plot(xt, yt, '--')
    dxt = xq
    dyt = dspl(xq)
    plt.plot(xb, dspl(xb), 'o', dxt, dyt)
    plt.show()
    dspl2 = spl.derivative(2)
    dxt2 = xq
    dyt2 = dspl2(xq)
    plt.plot(xb, dspl2(xb), 'o', dxt2, dyt2)
    xn = np.linspace(0.23, 0.25, 11)
    yn = (-1/k) * (xn - 0.24) + 14.7
    # print 'xn =', xn
    # print 'yn =', yn
    # plt.plot(xn, yn)
    # plt.axes().set_aspect('equal', 'datalim')
    vx = -dspl(0.24)
    vy = 1
    denom = np.sqrt(vx**2 + vy**2)
    vx /= denom
    vy /= denom
    print 'vx, vy =', vx, vy

    plt.show()


if __name__ == '__main__':
    test_boundary()
    # test_find_boundary_normal_vector()
