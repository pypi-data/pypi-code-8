# -*- encoding:utf-8 -*-

import inc


def break_shell(index=1, data="", center=(0, 0, 0), out_radius=25, shell=3, cutoff=(0, 0, 0, 0, 0, 0)):
    """
    the main function to write break hollow sphere
    :param index: a number which indicate the line numbers of main shape data
    :param data: string with all shape data combined
    :param center: center of the hollow sphere
    :param out_radius: out radius of sphere, the unit is nm
    :param shell: shell thickness of sphere
    :param cutoff: remove some part of break shell
    :return: int, string
    """
    number_range = inc.get_range(out_radius, cutoff)
    for j in range(number_range[0], number_range[1]):
        for k in range(number_range[2], number_range[3]):
            for m in range(number_range[4], number_range[5]):
                if break_shell_validate((j, k, m), out_radius, shell):
                    data += inc.print_line(index, center, (j, k, m))
                    index += 1
    return index, data


def break_shell_validate(point=(0, 0, 0), out_radius=25, shell=3):
    """
    validate if a point is in a shell
    :param point: temporary point of shell
    :param out_radius: out radius of shell
    :param shell: thickness of shell
    :return: boolean
    """
    precision = inc.get_precision()
    sqrt_acc = point[0]**2+point[1]**2+point[2]**2
    if ((out_radius-shell)*precision)**2 > sqrt_acc:
        return False
    if (out_radius*precision)**2 < sqrt_acc:
        return False
    return True


_index, _data = break_shell(cutoff=(0, 0, 15, 15, 0, 0), shell=5)
inc.write_shape((50, 50, 50), _index, _data)


