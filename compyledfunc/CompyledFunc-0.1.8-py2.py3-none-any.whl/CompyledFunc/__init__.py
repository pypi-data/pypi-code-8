from HelpyFuncs.Dicts import combine_dict_and_kwargs
from HelpyFuncs.SymPy import FLOAT_TYPES, is_non_atomic_sympy_expr, sympy_to_float

# ref: http://docs.sympy.org/dev/modules/numeric-computation.html
try:
    from sympy.printing.theanocode import theano_function
    use_theano = True
except:
    use_theano = False
    from sympy.utilities.autowrap import ufuncify


class CompyledFunc:
    def __init__(self, var_names_and_syms={}, dict_or_expr={}):
        if hasattr(dict_or_expr, 'keys'):
            for k, v in dict_or_expr.items():
                dict_or_expr[k] = CompyledFunc(var_names_and_syms=var_names_and_syms, dict_or_expr=v)
            self.Compiled = dict_or_expr
        elif is_non_atomic_sympy_expr(dict_or_expr):
            self.Vars = tuple(var for var, symbol in var_names_and_syms.items()
                              if symbol and not(isinstance(symbol, FLOAT_TYPES)))
            inputs = (var_names_and_syms[var] for var in self.Vars)
            if use_theano:
                self.Compiled = theano_function(inputs, (dict_or_expr,), allow_input_downcast=True)
            else:
                self.Compiled = ufuncify(inputs, dict_or_expr)
        else:
            self.Compiled = sympy_to_float(dict_or_expr)

    def __call__(self, var_names_and_values={}, **kw_var_names_and_values):
        if isinstance(self.Compiled, float):
            return self.Compiled
        else:
            var_names_and_values = combine_dict_and_kwargs(var_names_and_values, kw_var_names_and_values)
            if hasattr(self.Compiled, 'keys'):
                d = self.Compiled.copy()
                for k, v in d:
                    d[k] = v(var_names_and_values=var_names_and_values)
                return d
            else:
                return self.Compiled(*(var_names_and_values[var] for var in self.Vars))
