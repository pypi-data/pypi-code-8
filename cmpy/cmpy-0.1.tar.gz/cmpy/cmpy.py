# -*- coding: utf-8 -*-
"""
cmpy : Compare in Python
------------------------
A simple utility for detecting differences in directories and files.
"""
from functools import wraps
import stat
import os


__all__ = ['deep_fcmp', 'shallow_fcmp', 'DCompare', 'FCompare']

# ----------------
# Global Constants
# ----------------

CACHE_SIZE = 2 ** 8
BUFFER_SIZE = 2 ** 10


# --------------------
# Exception Definition
# --------------------


class CompareException(Exception):
    """ Base comparison exception """
    pass


class FileCompareException(CompareException):
    """ Exception for file comparison """
    pass


class DirectoryCompareException(CompareException):
    """ Exception for directory comparison """
    pass


# ---------------------
# Memoization Decorator
# ---------------------


def memoize(v):
    """
    Memoization decorator definition to be used for deep copy methods to improve performance.

    :param v:
    :return:
    """
    _cache = {}

    @wraps(v)
    def memoizer(*args):
        # Invalidate cache once it exceeds defined cache size
        if len(_cache) > CACHE_SIZE:
            _cache.clear()

        paths = args[:2]
        if paths not in _cache:
            _cache[paths] = v(*args)
        return _cache[paths]

    return memoizer


# --------------
# Static Methods
# --------------


def _get_sig(path):
    """
    Get the pertinent data for a path derived from an os.stat() call, to be used in determining
    file equality. The pertinent data returned by this function is considered the 'signature'
    corresponding to the path.

    :param path: Path to get the signature for
    :return: tuple of stat mode, stat size, and stat modification time
    :rtype: tuple
    """
    _stat = os.stat(path)
    return _stat.st_mode, _stat.st_size, _stat.st_mtime


@memoize
def deep_fcmp(f1, f2, buff_size=BUFFER_SIZE):
    """
    Perform a deep file compare by analyzing the bytes contained within the file. Shallow
    equality is confirmed before analyzing file bytes.

    :param f1: path of first file to compare
    :param f2: path of second file to compare
    :param buff_size: chunk size of file reads
    :return: True if equal, False otherwise
    :rtype: bool
    """
    if shallow_fcmp(f1, f2):
        with open(f1, 'rb') as _f1, open(f2, 'rb') as _f2:
            while True:
                buf1 = _f1.read(buff_size)
                buf2 = _f2.read(buff_size)

                if buf1 != buf2:
                    return False
                if not buf1 and not buf2:
                    return True
    return False


def shallow_fcmp(s1, s2):
    """
    Perform a shallow file compare by checking the signature of the two files.

    :param s1: path of first file to compare, or the signature of the first file
    :param s2: path of second file to compare, or the signature of the second file
    :return: True if equal, False otherwise
    :rtype: bool
    """
    if isinstance(s1, str) and isinstance(s2, str):
        s1 = _get_sig(s1)
        s2 = _get_sig(s2)

    if s1 == s2 and stat.S_ISREG(s1[0]):
        return True
    return False


# -----------------
# Class Definitions
# -----------------


class Compare(object):
    """
    Base abstract class from which all other comparison classes subclass.

    Class Members:
    -------------------------------------------------------------------
    path1       : The first path to be used in the comparison
    path2       : The second path to be used in the comparison
    sig1        : The signature corresponding to path1
    sig2        : The signature corresponding to path2
    shallow     : A flag determining whether to perform a shallow
                  compare or deep compare. Defaults to True.
    buffer_size : The buffer_size to read from files while
                  performing a deep copy. Defaults to the global
                  BUFFER_SIZE value.
    """
    def __init__(self, path1, path2, shallow, buffer_size):
        self.path1 = path1
        self.path2 = path2
        self.sig1 = _get_sig(path1)
        self.sig2 = _get_sig(path2)
        self.shallow = shallow
        self.buffer_size = buffer_size

    def compare(self):
        """ Override this method """
        pass


class DCompare(Compare):
    """
    DCompare compares two directories for equality by comparing the directory contents.

    Class Members:
    -------------------------------------------------------------------
    path1       : The first directory to be used in the comparison
    path2       : The second directory to be used in the comparison
    sig1        : The signature corresponding to path1
    sig2        : The signature corresponding to path2
    shallow     : Flag determining whether to perform a shallow
                  compare or deep compare. Defaults to True.
    buffer_size : The buffer_size to read from files while
                  performing a deep copy. Defaults to the global
                  BUFFER_SIZE value.
    recursive   : Flag for allowing comparison of any subdirectories
                  which may exist in the current directory. Defaults
                  to True
    _dir1_cont  : The names of the entries in the first directory
    _dir2_cont  : The names of the entries in the second directory


    Class Properties
    -------------------------------------------------------------------
    dir1_contents : The names of the entries in the first directory
    dir2_contents : The names of the entries in the second directory
    dir1_unique   : The names of the entries in the first directory
                    which are not in the second directory
    dir2_unique   : The names of the entries in the second directory
                    which are not in the first directory
    common        : The names of the entries found in both directories
    """
    def __init__(self, dir1, dir2, shallow=True, buffer_size=BUFFER_SIZE, recursive=False):
        super(DCompare, self).__init__(dir1, dir2, shallow, buffer_size)
        self.recursive = recursive

        if not stat.S_ISDIR(self.sig1[0]) or not stat.S_ISDIR(self.sig2[0]):
            raise DirectoryCompareException('Argument(s) are not directories.')

        self._dir1_cont = None
        self._dir2_cont = None

    @property
    def dir1_contents(self):
        """
        Names of the entries in the first directory.

        :return: List of file/directory names
        :rtype: list
        """
        if not self._dir1_cont:
            self._dir1_cont = sorted(os.listdir(self.path1))
        return self._dir1_cont

    @property
    def dir2_contents(self):
        """
        Names of the entries in the second directory.

        :return: List of file/directory names
        :rtype: list
        """
        if not self._dir2_cont:
            self._dir2_cont = sorted(os.listdir(self.path2))
        return self._dir2_cont

    @property
    def dir1_unique(self):
        """
        Names of the entries in the first directory which are not in the
        second directory.

        :return: List of file/directory names
        :rtype: list
        """
        return list(set(self._dir1_cont).difference(self._dir2_cont))

    @property
    def dir2_unique(self):
        """
        Names of the entries in the second directory which are not in the
        first directory.

        :return: List of file/directory names
        :rtype: list
        """
        return list(set(self._dir2_cont).difference(self._dir1_cont))

    @property
    def common(self):
        """
        Names of the entries found in both directories.

        :return: List of file/directory names
        :rtype: list
        """
        return filter(set(self.dir1_contents).__contains__, self.dir2_contents)

    def compare(self):
        """
        Compare the two directories for equality.

        :return: True if all contents in the directory are the same. False otherwise.
        :rtype: bool
        """
        if self.shallow:
            return self.dir1_contents == self.dir2_contents
        else:
            for _file in self.dir1_contents:
                if _file not in self.dir2_contents:
                    return False
                if not deep_fcmp(os.path.join(self.path1, _file), os.path.join(self.path2, _file)):
                    return False
            return True


class FCompare(Compare):
    """
    FCompare compares two files for equality by comparing the signature and/or the
    file contents.

    Class Members:
    -------------------------------------------------------------------
    path1       : The first file to be used in the comparison
    path2       : The second file to be used in the comparison
    sig1        : The signature corresponding to path1
    sig2        : The signature corresponding to path2
    shallow     : Flag determining whether to perform a shallow
                  compare or deep compare. Defaults to True.
    buffer_size : The buffer_size to read from files while
                  performing a deep copy. Defaults to the global
                  BUFFER_SIZE value.
    """
    def __init__(self, file1, file2, shallow=True, buffer_size=BUFFER_SIZE):
        super(FCompare, self).__init__(file1, file2, shallow, buffer_size)
        self.buffer_size = buffer_size

        if not stat.S_ISREG(self.sig1[0]) or not stat.S_ISREG(self.sig2[0]):
            raise FileCompareException('Argument(s) are not files.')

    def compare(self):
        """
        Compare the two files for equality.

        :return: True if the files are the same. False otherwise.
        :rtype: bool
        """
        if self.shallow:
            return shallow_fcmp(self.sig1, self.sig2)
        else:
            return deep_fcmp(self.path1, self.path2)