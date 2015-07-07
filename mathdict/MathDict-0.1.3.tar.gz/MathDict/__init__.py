# PyPI distribution reference: https://packaging.python.org/en/latest/distributing.html#uploading-your-project-to-pypi
# PyPI distribution reference: http://peterdowns.com/posts/first-time-with-pypi.html
# Python distribution reference:
# http://stackoverflow.com/questions/6344076/differences-between-distribute-distutils-setuptools-and-distutils2
# SetupTools reference: https://pythonhosted.org/setuptools/setuptools.html
# Python reference: https://docs.python.org/2/reference/datamodel.html
# Python reference: https://docs.python.org/2/library/operator.html


from __future__ import division
from collections import Mapping
from copy import deepcopy
from frozendict import frozendict
from HelpyFuncs.SymPy import sympy_allclose
from itertools import product
from operator import index, pos, neg, abs, lt, le, ge, gt, add, sub, mul, div, truediv, floordiv, mod, pow, xor
from pprint import pprint
from sympy import exp as e, log as ln, sqrt as square_root


class MathDict(Mapping):
    def __init__(self, *args, **kwargs):
        self.Mapping = dict(*args, **kwargs)
        self.Hash = None

    def __getitem__(self, k):   # need this to instantiate Abstract Base Class Mapping
        return self.Mapping[k]

    def __iter__(self):   # need this to instantiate Abstract Base Class Mapping
        return iter(self.Mapping)

    def __len__(self):   # need this to instantiate Abstract Base Class Mapping
        return len(self.Mapping)

    def __repr__(self):   # no need to define separate __str__ method
        return '<MathDict %s>' % repr(self.Mapping)

    def __setitem__(self, k, v):   # support item assignment
        self.Mapping[k] = v

    def __delitem__(self, k):   # support item deletion
        del self.Mapping[k]

#    NO NEED TO REDEFINE __CONTAINS__
#    def __contains__(self, item):
#        return item in self.Mapping

    def __hash__(self):
        if self.Hash is None:
            self.Hash = reduce(xor, map(hash, self.iteritems()), 0)
        return self.Hash

    # __call__: simply return Mapping
    def __call__(self):
        return self.Mapping

    def copy(self, deep=False):
        if deep:
            return deepcopy(self)
        else:
            math_dict = self
            math_dict.Mapping = math_dict.Mapping.copy()
            return math_dict

    def update(self, *args, **kwargs):   # add and/or update items
        self.Mapping.update(*args, **kwargs)

    def op(self, op=mul, other=None, r=False, **kwargs):
        math_dict = MathDict()
        if hasattr(other, 'keys'):
            for item_0, item_1 in product(self.items(), other.items()):
                vars_and_values_0___frozen_dict, func_value_0 = item_0
                vars_and_values_1___frozen_dict, func_value_1 = item_1
                same_vars_same_values = True
                for var in (set(vars_and_values_0___frozen_dict) & set(vars_and_values_1___frozen_dict)):
                    if vars_and_values_0___frozen_dict[var] != vars_and_values_1___frozen_dict[var]:
                        same_vars_same_values = False
                        break
                if same_vars_same_values:
                    if r:
                        value = op(func_value_1, func_value_0, **kwargs)
                    else:
                        value = op(func_value_0, func_value_1, **kwargs)
                    math_dict[frozendict(set(vars_and_values_0___frozen_dict.items()) |
                                         set(vars_and_values_1___frozen_dict.items()))] = value
        elif other is None:
            for k, v in self.items():
                math_dict[k] = op(v, **kwargs)
        elif r:
            for k, v in self.items():
                math_dict[k] = op(other, v, **kwargs)
        else:
            for k, v in self.items():
                math_dict[k] = op(v, other, **kwargs)
        return math_dict

    # Operations on Self alone:
    def __index__(self):
        return self.op(op=index)

    def __int__(self):
        return self.op(op=int)

    def __long__(self):
        return self.op(op=long)

    def __hex__(self):
        return self.op(op=hex)

    def __float__(self):
        return self.op(op=float)

    def __complex__(self):
        return self.op(op=complex)

    def __pos__(self):
        return self.op(op=pos)

    def __neg__(self):
        return self.op(op=neg)

    def __abs__(self):
        return self.op(op=abs)

    # Rich Comparisons
    def __lt__(self, other):
        return self.op(op=lt, other=other)

    def __le__(self, other):
        return self.op(op=le, other=other)

#    SKIP __EQ__ METHOD
#    def __eq__(self, other):
#        return self.op(op=eq, other=other)

#    SKIP __NE__ METHOD
#    def __ne__(self, other):
#        return self.op(op=ne, other=other)

    def __ge__(self, other):
        return self.op(op=ge, other=other)

    def __gt__(self, other):
        return self.op(op=gt, other=other)

    # Bit-Wise Operations
    # (SKIPPING ALL IN-PLACE METHODS)
    def __add__(self, other):
        return self.op(op=add, other=other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.op(op=sub, other=other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        return self.op(op=mul, other=other)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        return self.op(op=div, other=other)

    def __rdiv__(self, other):
        return self.op(op=div, other=other, r=True)

    def __truediv__(self, other):
        return self.op(op=truediv, other=other)

    def __rtruediv__(self, other):
        return self.op(op=truediv, other=other, r=True)

    def __floordiv__(self, other):
        return self.op(op=floordiv, other=other)

    def __rfloordiv__(self, other):
        return self.op(op=floordiv, other=other, r=True)

    def __mod__(self, other):
        return self.op(op=mod, other=other)

    def __rmod__(self, other):
        return self.op(op=mod, other=other, r=True)

    def __pow__(self, power):
        return self.op(op=pow, other=power)

    def __rpow__(self, other):
        return self.op(op=pow, other=other, r=True)

    def allclose(self, other, rtol=1e-5, atol=1e-8):
        return all(self.op(op=sympy_allclose, other=other, rtol=rtol, atol=atol).values())

    def pprint(self):
        pprint(repr(self))


def exp(math_dict):
    if isinstance(math_dict, MathDict):
        return math_dict.op(op=e)
    else:
        return e(math_dict)


def log(math_dict):
    if isinstance(math_dict, MathDict):
        return math_dict.op(op=ln)
    else:
        return ln(math_dict)


def sqrt(math_dict):
    if isinstance(math_dict, MathDict):
        return math_dict.op(op=square_root)
    else:
        return square_root(math_dict)
