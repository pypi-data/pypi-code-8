# -*- encoding:utf-8 -*-

import ddshape.inc as inc


def bshell(index=1, data="", center=(0, 0, 0), out_radius=25, shell=3, cutoff=(0, 0, 0, 0, 0, 0)):
    """
    the main function to write hollow sphere
    :param index: a number which indicate the line numbers of main shape data
    :param data: string with all shape data combined
    :param center: center of the hollow sphere
    :param out_radius: out radius of sphere
    :param shell: shell thickness of sphere
    :param cutoff: remove some part of break shell
    :return: int, string
    """
    for j in range(-1 * out_radius+cutoff[0], out_radius + 1-cutoff[1]):
        for k in range(-1 * out_radius+cutoff[2], out_radius + 1-cutoff[3]):
            for m in range(-1 * out_radius+cutoff[4], out_radius + 1-cutoff[5]):
                sqrt_acc = j ** 2 + k ** 2 + m ** 2
                if (out_radius - shell) ** 2 <= sqrt_acc <= out_radius ** 2:
                    data += inc.print_line(index, center, (j, k, m))
                    index += 1
    return index, data


#index, data = bshell(cutoff=(0, 0, 15, 15, 25, 0), shell=5)
#inc.write_shape((50, 50, 50), index, data)


