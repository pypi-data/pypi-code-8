# -*- encoding:utf-8 -*-

import inc


def sphere(index=1,
           data="",
           center=(0, 0, 0),
           out_radius=25,
           precision=1):
    """
    the function of create sphere shape.dat
    :param index: a number which indicate the line numbers of main shape data
    :param data: string with all shape data combined
    :param center: center of sphere
    :param out_radius: the radius of sphere
    :return: int, string
    """
    number_range = inc.get_range(out_radius=out_radius, precision=precision)
    for j in range(number_range[0], number_range[1]):
        for k in range(number_range[2], number_range[3]):
            for m in range(number_range[4], number_range[5]):
                if sphere_validate((j, k, m), out_radius, precision):
                    data += inc.print_line(index, center, (j, k, m), precision)
                    index += 1
    return index, data


def sphere_validate(point=(0, 0, 0),
                    out_radius=25,
                    precision=1):
    """
    test if a point is in sphere
    :param point:
    :param out_radius: radius of sphere
    :param precision:
    :return: boolean
    """
    sqrt_acc = point[0]**2 + point[1]**2 + point[2]**2
    if sqrt_acc > (out_radius*precision)**2:
        return False
    return True



