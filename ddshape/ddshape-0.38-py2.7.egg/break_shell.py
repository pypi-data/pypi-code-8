# -*- encoding:utf-8 -*-

import inc


def break_shell(index=1,
                data="",
                center=(0, 0, 0),
                out_radius=25,
                shell=3,
                cutoff=(0, 0, 0, 0, 0, 0),
                precision=1):
    """
    the main function to write break hollow sphere
    :param index: a number which indicate the line numbers of main shape data
    :param data: string with all shape data combined
    :param center: center of the hollow sphere
    :param out_radius: out radius of sphere, the unit is nm
    :param shell: shell thickness of sphere
    :param cutoff: remove some part of break shell
    :param precision: precision that determine the size of dipole
    :return: int, string
    """
    number_range = inc.get_range(out_radius, cutoff, precision)
    for j in range(number_range[0], number_range[1]):
        for k in range(number_range[2], number_range[3]):
            for m in range(number_range[4], number_range[5]):
                if break_shell_validate((j, k, m),
                                        out_radius,
                                        shell,
                                        precision):
                    data += inc.print_line(index, center, (j, k, m), precision)
                    index += 1
    return index, data


def break_shell_validate(point=(0, 0, 0),
                         out_radius=25,
                         shell=3,
                         precision=1):
    """
    validate if a point is in a shell
    :param point: temporary point of shell
    :param out_radius: out radius of shell
    :param shell: thickness of shell
    :param precision: precision that determine the size of dipole
    :return: boolean
    """
    sqrt_acc = point[0]**2+point[1]**2+point[2]**2
    if not ((out_radius-shell)*precision)**2 <= sqrt_acc <= (out_radius*precision)**2:
        return False
    return True



