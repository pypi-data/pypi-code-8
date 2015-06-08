from gi.repository import Cogl
import numpy as np
import pandas as pd


def to_array(mat):
    return np.array([[mat.xx, mat.xy, mat.xz, mat.xw],
                     [mat.yx, mat.yy, mat.yz, mat.yw],
                     [mat.zx, mat.zy, mat.zz, mat.zw],
                     [mat.wx, mat.wy, mat.wz, mat.ww]])


def from_array(transform_arr):
    mat = Cogl.Matrix()
    (mat.xx, mat.xy, mat.xz, mat.xw,
     mat.yx, mat.yy, mat.yz, mat.yw,
     mat.zx, mat.zy, mat.zz, mat.zw,
     mat.wx, mat.wy, mat.wz, mat.ww) = transform_arr.ravel()
    # __NB__ As stated [here][1], members of the `Cogl.Matrix` structure should
    # be treated as read-only.  However, we need to set the values of the
    # `xx`..`ww` attributes.
    #
    # As a workaround, transposing twice seems to update internal state of
    # structure.
    #
    # [1]: https://lazka.github.io/pgi-docs/Cogl-1.0/structs/Matrix.html#Cogl.Matrix
    mat.transpose()
    mat.transpose()
    return mat


def get_translation(mat):
    return pd.Series([mat.xw, mat.yw, mat.zw], index=['x', 'y', 'z'])


def get_scale(mat):
    return pd.Series([mat.xx, mat.yy, mat.zz], index=['x', 'y', 'z'])


def set_scale(mat, x, y, z=1):
    mat.xx, mat.yy, mat.zz = x, y, z


def set_translation(mat, x, y, z=0):
    mat.xw, mat.yw, mat.zw = x, y, z
