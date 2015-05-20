# -*- coding: utf-8 -*-
"""
utils.py
========

"""
import re
import pickle
import os.path
import datetime

import numpy as np
from scipy.io import loadmat

from .settings import *

__all__ = [
    'find_aF_from_data',
    'find_F_from_log',
    'find_accuracy_from_log',
    'find_density_from_log',
    'find_value',
    'find_name_value',
    'find_index',
    'find_index_of_common_elements',
    'find_neighbor_index',
    'find_interp_list',
    'find_label',
    'format_number_without_trailing_zero',
    'format_number_for_dirname',
    'format_number_by_precision',
    'format_array_by_precision',
    'create_mark',
    'check_mark',
    'compare_file_time',
    'now2str',
    'save',
    'load',
]


def compare_file_time(file1, file2):
    try:
        t1 = os.path.getmtime(file1)
    except:
        return False  # file1 does not exist
    try:
        t2 = os.path.getmtime(file2)
    except:
        return True  # file2 does not exist
    return t1 > t2  # True if file1 is newer than file2


def create_mark(mark_file):
    basedir = os.path.dirname(mark_file)
    if os.path.exists(basedir):
        with open(mark_file, 'w') as f:  # NOQA
            pass


def check_mark(mark_file):
    try:
        mtime = os.path.getmtime(mark_file)
    except:
        mtime = None
    return mtime


def find_aF_from_data(datafile, info_level=-1):
    alist, Flist = None, None
    try:
        mat = loadmat(datafile)
        alist = mat['a']
        alist = alist.reshape(alist.size)
        Flist = mat['F']
        Flist = Flist.reshape(Flist.size)
    except:
        if info_level > -1:
            print "\tWarning: there is no data in", datafile
    return alist, Flist


def find_F_from_log(logfile, phase, info_level=-1):
    '''
    Need to obtain the free energy F from LOG file if there is no DATA file.
    For DIS phase, it is not necessary to optimization cell size thus there is
    no DATA file.
    For other phases, the minimum free energy is found at the last line of the log file.
    '''
    F = None
    if phase == 'DIS':
        try:
            with open(logfile, 'rb') as f:
                for line in f:
                    line = "".join(line.split())  # remove all whitespaces
                    if not re.match('H=', line) is None:
                        rst = line.split('=')
                        F = float(rst[1])
        except:
            if info_level > -1:
                print 'Warning: error occurs when processing', logfile
    else:
        try:
            with open(logfile, 'rb') as f:
                first = f.readline()  # NOQA
                f.seek(-2, 2)               # Jump to the second last byte.
                while f.read(1) != "\n":    # Until EOL is found...
                    f.seek(-2, 1)  # ...jump back the read byte plus one more.
                last = f.readline()         # Read last line.
            last = "".join(last.split())  # remove all whitespaces
            result = last.split('=')
            F = float(result[1])
        except:
            if info_level > -1:
                print 'Warning: error occurs when processing', logfile

    return F


def find_accuracy_from_log(logfile, cell_size, info_level=-1):
    accuracy = 'NA'  # Default accuracy
    try:
        with open(logfile, 'r') as f:
            cell_size_found = False
            for line in f:
                line = "".join(line.split())  # remove all whitespaces
                if not re.match('\(lx,ly,lz\)=', line) is None:
                    rst = line.split('=')
                    size = float(rst[1].split(',')[0])
                    if np.abs(size - cell_size) < TOL_CELL_SIZE:
                        cell_size_found = True
                    else:
                        cell_size_found = False
                if not re.match('ResidualError=', line) is None \
                        and cell_size_found:
                    # format "phiA=0.4000[0.1815,0.9535]"
                    rst = line.split('=')
                    accuracy = float(rst[1])
    except:
        if info_level > -1:
            print 'Warning: error occurs when processing', logfile
    return accuracy


def find_density_from_log(logfile, cell_size, info_level=-1):
    phi_avg, phi_min, phi_max = None, None, None
    try:
        with open(logfile, 'r') as f:
            cell_size_found = False
            for line in f:
                line = "".join(line.split())  # remove all whitespaces
                if not re.match('\(lx,ly,lz\)=', line) is None:
                    rst = line.split('=')
                    size = float(rst[1].split(',')[0])
                    if np.abs(size - cell_size) < TOL_CELL_SIZE:
                        cell_size_found = True
                    else:
                        cell_size_found = False
                if not re.match('phiA=[\d.]+\[', line) is None \
                        and cell_size_found:
                    # format "phiA=0.4000[0.1815,0.9535]"
                    rst = line.split('=')
                    rst = rst[1].split('[')
                    phi_avg = float(rst[0])
                    rst = rst[1].split(',')
                    phi_min = float(rst[0])
                    rst = rst[1].split(']')
                    phi_max = float(rst[0])
    except:
        if info_level > -1:
            print 'Warning: error occurs when processing', logfile
    return (phi_avg, phi_min, phi_max)


def find_value(folder_name, varname):
    name, value = find_name_value(folder_name)
    if name == varname:
        return value
    else:
        return None


def find_name_value(folder_name):
    '''
    The format of folder_name:
            <varname><varvalue>
    Example:
            phi0.1          # should return 'phi', 0.1
            xN14.2          # should return 'xN', 14.2
            kappa0.5n       # should return 'kappa', -0.5
    '''
    pattern = '([-+]?\d*\.\d+|[-+]?\d+)'
    rst = re.split(pattern, folder_name)
    if len(rst) < 2:
        return folder_name, None
    name = rst[0]
    valuestr = rst[1]
    sign_str = ''
    if len(rst) > 2:
        sign_str = rst[2]
    if sign_str == 'n':
        value = -float(valuestr)
    else:
        value = float(valuestr)

    return name, value


def find_index(a, lim):
    '''
    Find the index i for which a[i] >= min and a[i-1] < min.
    Find the index j for which a[j] <= max and a[j+1] > max.
    Example:
        >>> a = np.array([1, 2, 3, 4, 5, 6], dtype=float)
        >>> lim1 = (2.5, 5)
        >>> find_index(a, lim1)  # gives (2, 4)
        >>> lim2 = (4, 8)
        >>> find_index(a, lim2)  # gives (3, 5)
        >>> lim3 = (-2, -1)
        >>> find_index(a, lim3)  # gives (None, None)

    Parameters
    ----------
    :param a: an array in ascending order
    :type a: numpy.ndarray, 1D
    :param lim: a tuple (min, max) specify the range to extract the index.
    :type lim: tuple of length 2
    '''
    a = np.array(a)
    min, max = lim
    ind, = np.where((a >= min) & (a <= max))
    if ind.size == 0:
        return None, None
    else:
        return ind[0], ind[-1]


def find_index_of_common_elements(a, b):
    '''
    Find common elements in a and b.
    Example:
        >>> a = np.array([ 12. ,  12.2,  12.4,  13. ,  13.2])
        >>> b = np.array([ 12. ,  12.2,  13. ,  13.2])
        >>> index1 = find_index_of_common_elements(a, b)
        # array([ True,  True, False,  True,  True], dtype=bool)
        >>> index2 = find_index_of_common_elements(b, a)
        # array([ True,  True,  True,  True, False], dtype=bool)
    Note: the order of input arrays is important as can be seen in the above example.

    Parameters
    ----------
    :param a: an array in ascending order
    :type a: numpy.ndarray, 1D
    :param b: an array in ascending order
    :type b: numpy.ndarray, 1D
    '''
    return np.in1d(a, b)


def find_neighbor_index(a, val):
    '''
    find index i, j so that
        a[i] <= val < a[j]
    '''
    a = np.array(a)
    if a.size == 0:
        return []
    if val < a[0] or val > a[-1] or a.size < 2:
        return []

    index, = np.where(a == val)
    if index.size > 0:
        i = index[0]
        if a.size == 2:
            return [0, 1]
        else:  # at least 3 elements
            if i == 0:
                return [0, 1]
            elif i == a.size - 1:
                return [i-1, i]  # NOQA
            else:
                return [i-1, i+1]  # NOQA
    else:
        i = np.searchsorted(a, val)
        return [i-1, i]  # NOQA


def find_interp_list(range, var, n, resolution, mode):
    '''
    Find an intepolation list within range.
        min, max = range
    If mode is regular
        uniform grid in range
        [min+1*d, min+2*d, min+3*d, ..., max-1*d] + [var]
        where d = (max - min) / n
    If mode is boundary
        only three points
        [var-d, var, var+d]
    '''
    min, max = range
    # boundary point already within resolution
    if max - min < resolution:
        return []
    # boundary piont not in range
    if var < min or var > max:
        return []

    if mode.upper() == 'REGULAR':
        a = np.linspace(min, max, n + 2)
        a = a[1:-1]
        i = np.searchsorted(a, var)
        if i == a.size:
            a = np.append(a, var)
        else:
            if not np.isclose(a[i], var):
                a = np.insert(a, i, var)
    else:
        a = []
        d = 1.0 * (max - min) / (n + 1)
        if var - d > min:
            a.append(var - d)
        else:
            a.append(var - 0.5 * (var - min))
        a.append(var)
        if var + d < max:
            a.append(var + d)
        else:
            a.append(var + 0.5 * (max - var))
        a = np.array(a)

    return a


def find_label(name):
    '''
    Return the LaTeX string of input.

    Parameters
    ----------
    :param name: the string to be masked.
    :type name: string
    '''
    if name in NAME_LABEL_DICT:
        label = NAME_LABEL_DICT[name]
    else:
        label = '$' + name + '$'
    return label


def format_number_without_trailing_zero(num):
    '''
    Examples:
        num         out
        0.10        0.1
        25.0        25
        20          20
        -0.0300     -0.03
    '''
    num_str = str(num)
    if num < 0:
        s = num_str.rstrip('0').rstrip('.') if '.' in num_str else num_str
        return s.lstrip('-') + 'n'
    else:
        return num_str.rstrip('0').rstrip('.') if '.' in num_str else num_str


def format_number_for_dirname(num, precision=None):
    '''
    Example:
        num         precision       out
        0.13499     0.01            0.13
    '''
    if precision is not None:
        dec = -int(np.fix(np.log10(precision)) - 1)
        num = np.around(num, dec)  # round to precision digit
    return format_number_without_trailing_zero(num)


def format_number_by_precision(num, precision):
    return float(format_number_for_dirname(num, precision))


def format_array_by_precision(arr, precision):
    arr = np.array(arr)
    for i in xrange(arr.size):
        arr[i] = format_number_by_precision(arr[i], precision)

    return arr


def now2str(format):
    '''
    An example of format is
        %Y%m%d-%H%M%S
    '''
    return datetime.datetime.now().strftime(format)


def save(result_dict, out_file):
    '''
    Dump dict object into file.
    :param result_dict: can be any Python.dict type.
    '''
    with open(out_file, 'wb') as f:
        # json.dump(result_dict, f)
        pickle.dump(result_dict, f)


def load(in_file):
    with open(in_file, 'rb') as f:
        # return json.load(f)
        return pickle.load(f)
