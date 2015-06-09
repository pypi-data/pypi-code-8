# -*- encoding:utf-8 -*-

# These are some common function which may be used in different shape.
# module inc

import math
import os
from string import Template
import shutil


def get_effective_radius(nums=1, d=0.001):
    """
    get the effective radius of shape according the size of d and the total nums of d.
    default d=0.0001.
    """
    effective_radius = d * (3 * nums / math.pi / 4) ** (1. / 3)
    return effective_radius


def tpl_dir():
    """
    get template path of shape.tpl
    """
    real_file = os.path.realpath(__file__)
    real_path = os.path.dirname(real_file)
    tpl_full_path = os.path.join(real_path, 'Template', 'shape.tpl')
    return tpl_full_path


def tpl_path():
    return os.path.dirname(tpl_dir())


def shape_dir():
    """
    get the path of shape.dat
    """
    return os.path.join(os.path.abspath('.'), 'shape.dat')


def print_line(index=1, center=(0, 0, 0), point=(0, 0, 0), precision=1):
    """
    format data that will be writted into shape.dat
    """
    line = "%6d\t%3d\t%3d\t%3d\t1\t1\t1\n" % (
        index,
        center[0]*precision + point[0],
        center[1]*precision + point[1],
        center[2]*precision + point[2])
    return line


def write_shape(point_max=(50, 50, 50), index=1, data="", precision=1):
    """
    write shape.dat with given point max and index and data
    """
    # indent should align to '{' or '('
    replace_string = {'nx': point_max[0],
                      'ny': point_max[1],
                      'nz': point_max[2],
                      'total': index - 1,
                      'data': data}
    # read template content
    content_tpl = open(tpl_dir(), 'r').read()
    tpl = Template(content_tpl)
    # replace template with real data
    content_shape = tpl.substitute(replace_string)
    open(shape_dir(), 'w').write(content_shape)
    # get effective radius and display it
    dipole = 0.001/float(precision)
    effective_radius = get_effective_radius(nums=index, d=dipole)
    print 'Write shape.dat successfully and effective radius is %s...' % effective_radius
    return effective_radius


def get_range(out_radius=25, cutoff=(0, 0, 0, 0, 0, 0), precision=1):
    """
    get range for break shell
    :param out_radius: the radius of shell
    :param cutoff: offset of break shell
    :return:
    """
    # return (-x, x, -y, y, -z, z)
    return (precision*(-1*out_radius+cutoff[0]),
            precision*(1*out_radius-cutoff[1])+1,
            precision*(-1*out_radius+cutoff[2]),
            precision*(1*out_radius-cutoff[3])+1,
            precision*(-1*out_radius+cutoff[4]),
            precision*(1*out_radius-cutoff[5])+1,
            )


def rep_variable(rep_dict, tpl_full_path, dest_full_path):
    """
    :param rep_dict: dict to be replace
    :param tpl_full_path: template full path
    :param dest_full_path: destination full path
    :return: void
    """
    tpl_content = file(tpl_full_path)
    tpl = Template(tpl_content)
    tpl_rep = tpl.substitute(rep_dict)
    open(dest_full_path, 'w').write(tpl_rep)


def copy_to_project(aeff, dest_dir):
    """
    copy ddscat.par with r
    :param aeff:
    :param dest_dir:
    :return:
    """
    # fielda path
    fielda_path = os.path.join(dest_dir, 'fielda')
    if not os.path.exists(dest_dir):
        print 'not have path %s' % dest_dir
        exit()
    if not os.path.exists(fielda_path):
        print 'not have path %s' % fielda_path
        os.mkdir(fielda_path)

    replace_dict = {'aeff':aeff}
    template_dir = tpl_path()

    # get template path
    ddscat_dir = os.path.join(template_dir, 'ddscat.tpl')
    fielda_dir = os.path.join(template_dir, 'fielda.tpl')
    # dest_dir
    ddscat_dest = os.path.join(dest_dir, 'ddscat.par')
    fielda_dest  = os.path.join(fielda_path, 'ddscat.par')
    # replace
    rep_variable(replace_dict, ddscat_dir, ddscat_dest)
    rep_variable(replace_dict, fielda_dir, fielda_dest)
    # 将shape.dat复制到目标位置
    shutil.copy(shape_dir(), dest_dir)
    shutil.copy(shape_dir(), fielda_path)
    # 生成vtr文件
    create_vtr(dest_dir)


def create_vtr(dest_dir):
    """
    create vtr file in dest_dir
    :param dest_dir: destination path
    :return: void
    """
    os.chdir(dest_dir)
    os.system('vtrcon')


def del_vtr(dest_dir):
    """
    delete vtr file in dest_dir and dest_dir have format
    like r'string' is better
    :param dest_dir: destination path
    :return: void
    """
    os.chdir(dest_dir)
    os.system('del *.vtr *.pvd')