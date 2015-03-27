# coding=utf-8
# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.35
#
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _CKDTree
import new

new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static) or hasattr(self, name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError(name)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


import types

try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object:
        pass

    _newclass = 0
del types


class KDTree(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KDTree, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KDTree, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _CKDTree.new_KDTree(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _CKDTree.delete_KDTree
    __del__ = lambda self: None

    def set_data(*args):
        return _CKDTree.KDTree_set_data(*args)

    def search_center_radius(*args):
        return _CKDTree.KDTree_search_center_radius(*args)

    def get_count(*args):
        return _CKDTree.KDTree_get_count(*args)

    def neighbor_search(*args):
        return _CKDTree.KDTree_neighbor_search(*args)

    def neighbor_simple_search(*args):
        return _CKDTree.KDTree_neighbor_simple_search(*args)

    def neighbor_get_count(*args):
        return _CKDTree.KDTree_neighbor_get_count(*args)

    def get_indices(*args):
        return _CKDTree.KDTree_get_indices(*args)

    def get_radii(*args):
        return _CKDTree.KDTree_get_radii(*args)

    def neighbor_get_indices(*args):
        return _CKDTree.KDTree_neighbor_get_indices(*args)

    def neighbor_get_radii(*args):
        return _CKDTree.KDTree_neighbor_get_radii(*args)


KDTree_swigregister = _CKDTree.KDTree_swigregister
KDTree_swigregister(KDTree)
