# -*- coding: utf-8 -*-

from ctypes import cdll, c_float, Structure, c_int32, c_void_p, cast, c_size_t, POINTER
from sys import platform
import os

if platform == "darwin":
    ext = "dylib"
else:
    ext = "so"

__author__ = u"Stephan Hügel"
__version__ = "0.1.10"


# hacky: http://stackoverflow.com/a/30789980/416626
class Int32_2(Structure):
    _fields_ = [("array", c_int32 * 2)]


# liblonlat_bng.dylib
file_path = os.path.dirname(__file__)
lib = cdll.LoadLibrary(os.path.join(file_path, 'liblonlat_bng.' + ext))
rust_bng = lib.convert
rust_bng.argtypes = [c_float, c_float]
rust_bng.restype = Int32_2

def convertbng(lon, lat):
    """ Simple wrapper around the linked Rust function """
    return tuple(r for r in rust_bng(lon, lat).array)


class FFITuple(Structure):
    _fields_ = [("a", c_int32),
                ("b", c_int32)]


class FFIArray(Structure):
    _fields_ = [("data", c_void_p),
                ("len", c_size_t)]

rust_bng_c = lib.convert_vec_c
rust_bng_c.argtypes = (FFIArray, FFIArray)
rust_bng_c.restype = FFIArray

def convertbng_list(lons, lats):
    """
    Performs the same conversion, but on iterables
    Returns a list of Easting, Northing tuples
    """
    lons2 = (c_float * len(lons))(*lons)
    lats2 = (c_float * len(lats))(*lats)

    lon_array = FFIArray(cast(lons2, c_void_p), len(lons2))
    lat_array = FFIArray(cast(lats2, c_void_p), len(lats2))
    result = rust_bng_c(lon_array, lat_array)

    results = cast(result.data, POINTER(FFITuple))
    res = []
    for i in xrange(result.len):
        tupl = results[i]
        res.append((tupl.a, tupl.b))
    return res
