from __future__ import print_function
from CompyledFunc import CompyledFunc
from copy import copy as shallowcopy, deepcopy
from frozendict import frozendict
from HelpyFuncs.Dicts import combine_dict_and_kwargs, merge_dicts_ignoring_dup_keys_and_none_values
from HelpyFuncs.SymPy import sympy_allclose, sympy_xreplace
from MathDict import MathDict
from operator import index, pos, neg, abs, lt, le, eq, ne, ge, gt, add, sub, mul, div, truediv, floordiv, mod, pow
from pprint import pprint
from sympy import exp as e, log as ln, pprint as sympy_print, sqrt as square_root


class MathFunc:
    def __init__(self, var_names_and_syms={}, mapping={}, param={}, cond={}, scope={}, compile=False):
        self.Vars = var_names_and_syms   # {var_name: var_symbol} dict
        self.Param = param
        self.Cond = cond   # {var_name: var_value} dict, var_value can be None if conditioning is generic
        self.Scope = dict.fromkeys(set(var_names_and_syms) - set(cond))
        vars_with_fixed_scope_values = {}   # to keep track of scope variables with fixed values (i.e. points in space)
        for var, value in scope.items():
            if (var in self.Scope) and (value is not None):
                self.Scope[var] = value    # "points-in-space"
                vars_with_fixed_scope_values[var] = value
        s0 = set(vars_with_fixed_scope_values.items())
        if hasattr(mapping, 'keys'):
            self.Mapping = MathDict()
            self.CondInstances = {}
            for vars_and_values___frozen_dict, func_value in mapping.items():
                if set(vars_and_values___frozen_dict.items()) >= s0:
                    self.Mapping[vars_and_values___frozen_dict] = func_value
                    condition_instance = {}
                    for var in (set(vars_and_values___frozen_dict) & set(cond)):
                        condition_instance[var] = vars_and_values___frozen_dict[var]
                    self.CondInstances[vars_and_values___frozen_dict] = frozendict(condition_instance)
        else:
            self.Mapping = mapping

        if compile:
            self.compile()
        else:
            self.CompyledFunc = None

    def __repr__(self):
        return 'MathFunc %s' % repr(self.Mapping)

    def copy(self, deep=False):
        if deep:
            return deepcopy(self)
        else:
            return shallowcopy(self)

    def at(self, vars_and_values___dict={}, **kw_vars_and_values___dict):
        vars_and_values___dict = combine_dict_and_kwargs(vars_and_values___dict, kw_vars_and_values___dict)
        for var in (set(self.Vars) & set(vars_and_values___dict)):
            vars_and_values___dict[self.Vars[var]] = vars_and_values___dict[var]
        conds = self.Cond.copy()
        scope = self.Scope.copy()
        for var, value in vars_and_values___dict.items():
            if var in conds:
                conds.update({var: value})
            if var in scope:
                scope.update({var: value})
        conds = sympy_xreplace(conds, vars_and_values___dict)
        scope = sympy_xreplace(scope, vars_and_values___dict)
        if hasattr(self.Mapping, 'keys'):
            mapping = {}
            for vars_and_values___frozen_dict, func_value in self.Mapping.items():
                other_items___dict = dict(set(vars_and_values___frozen_dict.items()) -
                                          set(vars_and_values___dict.items()))
                if not (set(other_items___dict) and set(vars_and_values___dict)):
                    mapping[frozendict(set(vars_and_values___frozen_dict.items()) - set(conds.items()))] =\
                        sympy_xreplace(func_value, vars_and_values___dict)
        else:
            mapping = sympy_xreplace(self.Mapping, vars_and_values___dict)
        return MathFunc(self.Vars.copy(), mapping, cond=conds, scope=scope)

    def compile(self):
        self.CompyledFunc = CompyledFunc(merge_dicts_ignoring_dup_keys_and_none_values(self.Vars, self.Param),
                                         self.Mapping)

    def __call__(self, var_and_param_names_and_values={}, **kw_var_and_param_names_and_values):
        var_and_param_names_and_values = combine_dict_and_kwargs(var_and_param_names_and_values,
                                                                 kw_var_and_param_names_and_values)
        if var_and_param_names_and_values:
            if not self.CompyledFunc:
                self.compile()
            return self.CompyledFunc(var_and_param_names_and_values)
        elif isinstance(self.Mapping, MathDict):
            return self.Mapping()
        else:
            return self.Mapping

    def optim(self, max_or_min=max, leave_unoptimized=None):
        if max_or_min is max:
            comp = ge
        else:
            comp = le
        if leave_unoptimized:
            comparison_bases = {}
            conditioned_and_unoptimized_vars = set(self.Cond) | set(leave_unoptimized)
            for vars_and_values___frozen_dict in self.Mapping:
                comparison_basis = {}
                for var in (set(vars_and_values___frozen_dict) & conditioned_and_unoptimized_vars):
                    comparison_basis[var] = vars_and_values___frozen_dict[var]
                comparison_bases[vars_and_values___frozen_dict] = frozendict(comparison_basis)
        else:
            comparison_bases = self.CondInstances
        optim_values = {}
        for vars_and_values___frozen_dict, func_value in self.Mapping.items():
            comparison_basis = comparison_bases[vars_and_values___frozen_dict]
            if comparison_basis in optim_values:
                optim_values[comparison_basis] = max_or_min(optim_values[comparison_basis], func_value)
            else:
                optim_values[comparison_basis] = func_value
        optims = {}
        for vars_and_values___frozen_dict, func_value in self.Mapping.items():
            if comp(func_value, optim_values[comparison_bases[vars_and_values___frozen_dict]]):
                optims[vars_and_values___frozen_dict] = func_value
        return MathFunc(self.Vars.copy(), optims, cond=self.Cond.copy(), scope=self.Scope.copy())

    def marg(self, *marginalized_vars, **kwargs):
        itself = lambda x: x
        if 'transf' in kwargs:
            transf_func = kwargs['transf']
        else:
            transf_func = itself
        if 'reduce_func' in kwargs:
            reduce_func = kwargs['reduce_func']
        else:
            reduce_func = add
        if 'rev_transf' in kwargs:
            rev_transf_func = kwargs['rev_transf']
        else:
            rev_transf_func = itself
        var_names_and_symbols___dict = self.Vars.copy()   # just to be careful
        scope = self.Scope.copy()   # just to be careful
        mapping = self.Mapping.copy()   # just to be careful
        for marginalized_var in marginalized_vars:
            del var_names_and_symbols___dict[marginalized_var]
            del scope[marginalized_var]
            d = {}
            for vars_and_values___frozen_dict, func_value in mapping.items():
                marginalized_var_value = vars_and_values___frozen_dict[marginalized_var]
                fd = frozendict(set(vars_and_values___frozen_dict.items()) -
                                {(marginalized_var, marginalized_var_value)})
                if fd in d:
                    d[fd] = reduce_func(d[fd], transf_func(func_value))
                else:
                    d[fd] = transf_func(func_value)
            mapping = {k: rev_transf_func(v) for k, v in d.items()}
        return MathFunc(var_names_and_symbols___dict, mapping, cond=self.Cond.conds(), scope=scope)

    def cond(self, conds={}, **kw_conds):
        conds = combine_dict_and_kwargs(conds, kw_conds)
        mapping = {}
        s0 = set(conds.items())
        for vars_and_values___frozen_dict, func_value in self.Mapping().items():
            s = set(vars_and_values___frozen_dict.items())
            if s >= s0:
                mapping[frozendict(s - s0)] = func_value
        new_conds = self.Cond.copy()
        new_conds.update(conds)
        new_scope = self.Scope.copy()
        for var in conds:
            del new_scope[var]
        return MathFunc(self.Vars.copy(), mapping, cond=new_conds, scope=new_scope)

    def op(self, op=mul, other=None, r=False, **kwargs):
        if isinstance(other, MathFunc):
            conds = merge_dicts_ignoring_dup_keys_and_none_values(self.Cond, other.Cond)
            scope = merge_dicts_ignoring_dup_keys_and_none_values(self.Scope, other.Scope)
            for var in (set(conds) & set(scope)):
                del conds[var]
            var_names_and_symbols = merge_dicts_ignoring_dup_keys_and_none_values(self.Vars, other.Vars)
            other_mapping = other.Mapping
        else:
            var_names_and_symbols = self.Vars.copy()
            conds = self.Cond.copy()
            scope = self.Scope.copy()
            other_mapping = other
        if isinstance(self.Mapping, MathDict):
            mapping = self.Mapping.op(op, other_mapping, r=r, **kwargs)
        elif isinstance(other_mapping, MathDict):
            mapping = other_mapping.op(op, self.Mapping, r=not r, **kwargs)
        else:
            mapping = op(self.Mapping, other_mapping, **kwargs)
        return MathFunc(var_names_and_symbols, mapping, conds, scope)

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

    def __eq__(self, other):
        return self.op(op=eq, other=other)

    def __ne__(self, other):
        return self.op(op=ne, other=other)

    def __ge__(self, other):
        return self.op(op=ge, other=other)

    def __gt__(self, other):
        return self.op(op=gt, other=other)

    # Bit-Wise Operations
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
        return all(self.op(op=sympy_allclose, other=other, rtol=rtol, atol=atol).Mapping.values())

    def pprint(self):
        print('MATHEMATICAL FUNCTION')
        print('_____________________')
        print("VARIABLES' SYMBOLS:")
        pprint(self.Vars)
        print('conds:')
        pprint(self.Cond)
        print('SCOPE:')
        pprint(self.Scope)
        print('MAPPING:')
        sympy_print(self.Mapping)


def exp(math_func):
    if isinstance(math_func, MathFunc):
        return math_func.op(op=e)
    else:
        return e(math_func)


def log(math_func):
    if isinstance(math_func, MathFunc):
        return math_func.op(op=ln)
    else:
        return ln(math_func)


def sqrt(math_dict):
    if isinstance(math_dict, MathDict):
        return math_dict.op(op=square_root)
    else:
        return square_root(math_dict)
