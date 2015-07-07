from __future__ import division, print_function
from copy import deepcopy
from frozendict import frozendict
from HelpyFuncs.SymPy import is_non_atomic_sympy_expr, sympy_xreplace, sympy_xreplace_doit_explicit,\
    sympy_xreplace_doit_explicit_eval
from HelpyFuncs.Dicts import combine_dict_and_kwargs, merge_dicts_ignoring_duplicate_keys_and_none_values
from HelpyFuncs.zzz import shift_time_subscripts
from itertools import product
from MathDict import exp as exp_math_dict, MathDict
from MathFunc import MathFunc
from pprint import pprint
from scipy.stats import uniform, multivariate_normal
from sympy import exp, log, pi, sympify
from sympy.matrices import BlockMatrix, det

class PDF(MathFunc):
    def __init__(self, family_name, var_names_and_symbols___dict, params___dict, neg_log_density_func,
                 normalization_func, max_func, marginalization_func, conditioning_func, sampling_func,
                 conds={}, scope={}):
        self.Family = family_name
        neg_log_density = neg_log_density_func(var_names_and_symbols___dict, params___dict)
        if self.is_discrete_finite():
            density = exp_math_dict(-neg_log_density)
        else:
            density = exp(-neg_log_density)
        MathFunc.__init__(self, var_names_and_symbols___dict, density, conds=conds, scope=scope)
        self.Params = params___dict
        self.NegLogDensFunc = neg_log_density_func
        self.NormFunc = normalization_func
        self.MaxFunc = max_func
        self.MargFunc = marginalization_func
        self.CondFunc = conditioning_func
        self.SampleFunc = sampling_func

    def copy(self, deep=False):
        if deep:
            return PDF(self.Family, deepcopy(self.Vars), deepcopy(self.Params),
                       self.NegLogDensFunc, self.NormFunc, self.MaxFunc,
                       self.MargFunc, self.CondFunc, self.SampleFunc,
                       deepcopy(self.Conds), deepcopy(self.Scope))
        else:
            return PDF(self.Family, self.Vars.copy(), self.Params.copy(),
                       self.NegLogDensFunc, self.NormFunc, self.MaxFunc,
                       self.MargFunc, self.CondFunc, self.SampleFunc,
                       self.Conds.copy(), self.Scope.copy())

    def is_discrete_finite(self):
        return self.Family == 'DiscreteFinite'

    def is_one(self):
        return self.Family == 'One'

    def is_uniform(self):
        return self.Family == 'Uniform'

    def is_gaussian(self):
        return self.Family == 'Gaussian'

    def at(self, var_and_param_values___dict={}, **kw_var_and_param_values___dict):
        var_and_param_values___dict =\
            combine_dict_and_kwargs(var_and_param_values___dict, kw_var_and_param_values___dict)
        for var in (set(self.Vars) & set(var_and_param_values___dict)):
            var_and_param_values___dict[self.Vars[var]] = var_and_param_values___dict[var]
        pdf = self.copy()
        for var, value in var_and_param_values___dict.items():
            if var in pdf.Conds:
                pdf.Conds.update({var: value})
            if var in pdf.Scope:
                pdf.Scope.update({var: value})
        pdf.Conds = sympy_xreplace(pdf.Conds, var_and_param_values___dict)
        pdf.Scope = sympy_xreplace(pdf.Scope, var_and_param_values___dict)
        if pdf.is_discrete_finite():
            neg_log_probs = {}
            for var_values___frozen_dict, mapping_value in pdf.Params['NegLogProb'].items():
                other_items___dict = dict(set(var_values___frozen_dict.items()) -
                                          set(var_and_param_values___dict.items()))
                if not (set(other_items___dict) & set(var_and_param_values___dict)):
                    neg_log_probs[frozendict(set(var_values___frozen_dict.items()) - set(pdf.Conds.items()))] =\
                        sympy_xreplace(mapping_value, var_and_param_values___dict)
            return DiscreteFinitePMF(pdf.Vars, neg_log_probs, pdf.Conds, pdf.Scope, prob=False)
        else:
            pdf.Params = sympy_xreplace(pdf.Params, var_and_param_values___dict)
            return pdf

    def __call__(self, var_and_param_values___dict={}, prob=True):
        scope_vars = deepcopy(self.Vars)
        for var in self.Vars:
            if var not in self.Scope:
                del scope_vars[var]
            elif self.Scope[var] is not None:
                scope_vars[var] = self.Scope[var]
        if var_and_param_values___dict:
            symbols_and_values___dict = {}
            for var_or_parameter, value in var_and_param_values___dict.items():
                if var_or_parameter in self.Vars:
                    symbols_and_values___dict[self.Vars[var_or_parameter]] = value
                elif var_or_parameter in self.Params:
                    symbols_and_values___dict[self.Params[var_or_parameter]] = value
            if prob:
                return sympy_xreplace_doit_explicit_eval(
                    probs_from_neg_log_probs(self.NegLogDensFunc(scope_vars, self.Params)),
                    symbols_and_values___dict)
            else:
                return sympy_xreplace_doit_explicit_eval(self.NegLogDensFunc(scope_vars, self.Params),
                                                          symbols_and_values___dict)
        elif prob:
            return probs_from_neg_log_probs(self.NegLogDensFunc(scope_vars, self.Params))
        else:
            return self.NegLogDensFunc(scope_vars, self.Params)

    def norm(self):
        return self.NormFunc(self)

    def max(self, **kwargs):
        return self.MaxFunc(self, **kwargs)

    def marg(self, *marginalized_vars):
        return self.MargFunc(self, *marginalized_vars)

    def cond(self, conds={}, **kw_conds):
        conds = combine_dict_and_kwargs(conds, kw_conds)
        return self.CondFunc(self, conds)

    def sample(self, num_samples=1):
        return self.SampleFunc(self, num_samples)

    def __mul__(self, probability_density_function_to_multiply):
        return product_of_2_probability_density_functions(self, probability_density_function_to_multiply)

    def __rmul__(self, probability_density_function_to_multiply):
        return product_of_2_probability_density_functions(probability_density_function_to_multiply, self)

    def __imul__(self, other):
        self /= other

    def multiply(self, *probability_density_functions_to_multiply):
        pdf = self.copy()
        for pdf_to_multiply in probability_density_functions_to_multiply:
            pdf = pdf.__mul__(pdf_to_multiply)
        return pdf

    def pprint(self):
        discrete = self.is_discrete_finite()
        print('\n')
        if discrete:
            print('MASS FUNCTION')
            print('_____________')
        else:
            print('DENSITY FUNCTION')
            print('________________')
            print('FAMILY:', self.Family)
        print("VARIABLES' SYMBOLS:")
        pprint(self.Vars)
        print('conds:')
        pprint(self.Conds)
        print('SCOPE:')
        pprint(self.Scope)
        if not discrete:
            print('PARAMETERS:')
            pprint(self.Params)
            print('DENSITY:')
        else:
            print('MASS:')
        d = self()
        pprint(d)
        if discrete:
            print('   sum =', sum(d.values()))
        print('\n')

    def shift_time_subscripts(self, t):
        pdf = self.copy()
        pdf.Vars = shift_time_subscripts(pdf.Vars, t)
        pdf.Conds = shift_time_subscripts(pdf.Conds, t)
        pdf.Scope = shift_time_subscripts(pdf.Scope, t)
        pdf.Params = shift_time_subscripts(pdf.Params, t)
        return pdf


def probs_from_neg_log_probs(expr_or_dict):
    if hasattr(expr_or_dict, 'keys'):
        probs___math_dict = MathDict(())
        for k, v in expr_or_dict.items():
            probs___math_dict[k] = exp(-v)
        return probs___math_dict
    else:
        return exp(-expr_or_dict)


def product_of_2_probability_density_functions(pdf_1, pdf_2):
    families = (pdf_1.Family, pdf_2.Family)
    if families == ('DiscreteFinite', 'DiscreteFinite'):
        return product_of_2_DiscreteFinitePMFs(pdf_1, pdf_2)
    elif pdf_1.is_discrete_finite():
        return product_of_discrete_finite_probability_mass_function_and_continuous_probability_density_function(
            pdf_1, pdf_2)
    elif pdf_2.is_discrete_finite():
        return product_of_discrete_finite_probability_mass_function_and_continuous_probability_density_function(
            pdf_2, pdf_1)
    elif families == ('One', 'Gaussian'):
        return product_of_one_probability_density_function_and_gaussian_probability_density_function(
            pdf_1, pdf_2)
    elif families == ('Gaussian', 'One'):
        return product_of_one_probability_density_function_and_gaussian_probability_density_function(
            pdf_2, pdf_1)
    elif families == ('Gaussian', 'Gaussian'):
        return product_of_2_gaussian_probability_density_functions(pdf_1, pdf_2)


def one_density_function(var_symbols={}, conds={}):
    return PDF('One', var_symbols.copy(), {}, one, one, one, one, one,
                                      lambda *args, **kwargs: None, deepcopy(conds))


def one(*args, **kwargs):
    return sympify(0.)



class DiscreteFinitePMF(PDF):
    def __init__(self, var_names_and_symbols, neg_log_probs___dict, conds={}, scope={}, prob=True):
        non_none_scope = {var: value for var, value in scope.items() if value is not None}
        if prob:
            f = lambda x: -log(x)
        else:
            f = lambda x: x
        neg_log_probs___dict = MathDict({var_values___frozen_dict: f(func_value)
                                        for var_values___frozen_dict, func_value in neg_log_probs___dict.items()
                                        if set(var_values___frozen_dict.items()) >= set(non_none_scope.items())})
        PDF.__init__(self, 'DiscreteFinite', var_names_and_symbols.copy(), dict(NegLogProb=neg_log_probs___dict),
                     discrete_finite_neg_log_mass, discrete_finite_normalization, discrete_finite_max,
                     discrete_finite_marginalization, discrete_finite_conditioning,
                     lambda *args, **kwargs: None, deepcopy(conds), non_none_scope)

    def copy(self, deep=False):
        if deep:
            return DiscreteFinitePMF(deepcopy(self.Vars), deepcopy(self.Params['NegLogProb']),
                                     conds=deepcopy(self.Conds), scope=deepcopy(self.Scope), prob=False)
        else:
            return DiscreteFinitePMF(self.Vars.copy(), self.Params['NegLogProb'].copy(),
                                     conds=self.Conds.copy(), scope=self.Scope.copy(), prob=False)

    def allclose(self, *PMFs, **kwargs):
        for pmf in PMFs:
            if not ((self.Vars == pmf.Vars) and (self.Conds == pmf.Conds) and (self.Scope == pmf.Scope) and
                    self.Params['NegLogProb'].allclose(pmf.Params['NegLogProb'], **kwargs)):
                return False
        return True


def discrete_finite_neg_log_mass(var_values___dict, parameters):
    v = var_values___dict.copy()
    for var, value in var_values___dict.items():
        if (value is None) or is_non_atomic_sympy_expr(value):
            del v[var]
    s0 = set(v.items())
    d = MathDict(())
    mappings = parameters['NegLogProb']
    for var_values___frozen_dict, mapping_value in mappings.items():
        spare_var_values = dict(s0 - set(var_values___frozen_dict.items()))
        s = set(spare_var_values.keys())
        if not(s) or (s and not(s & set(var_values___frozen_dict))):
            d[var_values___frozen_dict] = sympy_xreplace_doit_explicit(mapping_value, var_values___dict)
    return d


def discrete_finite_normalization(discrete_finite_pmf):
    pmf = discrete_finite_pmf.copy()
    pmf.Params['NegLogProb'] = pmf.Params['NegLogProb'].copy()
    mappings = pmf.Params['NegLogProb']
    cond_instances = pmf.CondInstances
    condition_sums = {}
    for var_values___frozen_dict, function_value in mappings.items():
        condition_instance = cond_instances[var_values___frozen_dict]
        if condition_instance in condition_sums:
            condition_sums[condition_instance] += exp(-function_value)
        else:
            condition_sums[condition_instance] = exp(-function_value)
    for var_values___frozen_dict in mappings:
        pmf.Params['NegLogProb'][var_values___frozen_dict] +=\
            log(condition_sums[cond_instances[var_values___frozen_dict]])
    return pmf


def discrete_finite_max(discrete_finite_pmf, leave_unoptimized=None):
    mappings = discrete_finite_pmf.Params['NegLogProb']
    if leave_unoptimized:
        comparison_bases = {}
        conditioned_and_unoptimized_vars = set(discrete_finite_pmf.Conds) | set(leave_unoptimized)
        for var_values___frozen_dict in mappings:
            comparison_basis = {}
            for var in (set(var_values___frozen_dict) & conditioned_and_unoptimized_vars):
                comparison_basis[var] = var_values___frozen_dict[var]
            comparison_bases[var_values___frozen_dict] = frozendict(comparison_basis)
    else:
        comparison_bases = discrete_finite_pmf.CondInstances
    minus_log_mins = {}
    for var_values___frozen_dict, mapping_value in mappings.items():
        comparison_basis = comparison_bases[var_values___frozen_dict]
        if comparison_basis in minus_log_mins:
            minus_log_mins[comparison_basis] = min(minus_log_mins[comparison_basis], mapping_value)
        else:
            minus_log_mins[comparison_basis] = mapping_value
    max_mappings = {}
    for var_values___frozen_dict, mapping_value in mappings.items():
        if mapping_value <= minus_log_mins[comparison_bases[var_values___frozen_dict]]:
            max_mappings[var_values___frozen_dict] = mapping_value
    return DiscreteFinitePMF(discrete_finite_pmf.Vars.copy(), max_mappings,
                             conds=deepcopy(discrete_finite_pmf.Conds),
                             scope=deepcopy(discrete_finite_pmf.Scope), prob=False)


def discrete_finite_marginalization(discrete_finite_pmf, *marginalized_vars):
    var_symbols = discrete_finite_pmf.Vars.copy()
    mappings = discrete_finite_pmf.Params['NegLogProb'].copy()
    for marginalized_var in marginalized_vars:
        del var_symbols[marginalized_var]
        d = {}
        for var_values___frozen_dict, mapping_value in mappings.items():
            marginalized_var_value = var_values___frozen_dict[marginalized_var]
            fd = frozendict(set(var_values___frozen_dict.items()) - {(marginalized_var, marginalized_var_value)})
            if fd in d:
                d[fd] += exp(-mapping_value)
            else:
                d[fd] = exp(-mapping_value)
        mappings = {k: -log(v) for k, v in d.items()}
    return DiscreteFinitePMF(var_symbols, mappings,
                             conds=deepcopy(discrete_finite_pmf.Conds),
                             scope=deepcopy(discrete_finite_pmf.Scope), prob=False)


def discrete_finite_conditioning(discrete_finite_pmf, conds={}, **kw_conds):
    conds = combine_dict_and_kwargs(conds, kw_conds)
    mappings = discrete_finite_pmf.Params['NegLogProb'].copy()
    d = {}
    s0 = set(conds.items())
    for var_values___frozen_dict, mapping_value in mappings.items():
        s = set(var_values___frozen_dict.items())
        if s >= s0:
            d[frozendict(s - s0)] = mapping_value
    new_conds = deepcopy(discrete_finite_pmf.Conds)
    new_conds.update(conds)
    scope = deepcopy(discrete_finite_pmf.Scope)
    for var in conds:
        del scope[var]
    return DiscreteFinitePMF(discrete_finite_pmf.Vars.copy(), d, conds=new_conds, scope=scope, prob=False)


def uniform_density_function(var_symbols, parameters, conds={}, scope={}):
    return PDF('Uniform', deepcopy(var_symbols), deepcopy(parameters),
                                      uniform_density, uniform_normalization, lambda *args, **kwargs: None,
                                      uniform_marginalization, uniform_conditioning, uniform_sampling,
                                      deepcopy(conds), deepcopy(scope))


def uniform_density(var_symbols, parameters):
    d = 1.
    return d


def uniform_normalization():
    return 0


def uniform_marginalization():
    return 0


def uniform_conditioning():
    return 0


def uniform_sampling():
    return 0


def one_mass_function(var_symbols, frozen_dicts___set=set(), conds={}):
    mappings = {item: 1. for item in frozen_dicts___set}
    return DiscreteFinitePMF(var_symbols, mappings, conds=conds, scope={})


def gaussian_density_function(var_symbols, parameters, conds={}, scope={}):
    return PDF('Gaussian', var_symbols.copy(), deepcopy(parameters),
                                      gaussian_density, lambda *args, **kwargs: None, gaussian_max,
                                      gaussian_marginalization, gaussian_conditioning, gaussian_sampling,
                                      deepcopy(conds), deepcopy(scope))


def gaussian_density(var_row_vectors___dict, parameters___dict):
    var_names = tuple(var_row_vectors___dict)
    num_vars = len(var_names)
    x = []
    m = []
    S = [num_vars * [None] for _ in range(num_vars)]   # careful not to create same mutable object
    d = 0
    for i in range(num_vars):
        x += [var_row_vectors___dict[var_names[i]]]
        d += var_row_vectors___dict[var_names[i]].shape[1]
        m += [parameters___dict[('mean', var_names[i])]]
        for j in range(i):
            if ('cov', var_names[i], var_names[j]) in parameters___dict:
                S[i][j] = parameters___dict[('cov', var_names[i], var_names[j])]
                S[j][i] = S[i][j].T
            else:
                S[j][i] = parameters___dict[('cov', var_names[j], var_names[i])]
                S[i][j] = S[j][i].T
        S[i][i] = parameters___dict[('cov', var_names[i])]
    x = BlockMatrix([x])
    m = BlockMatrix([m])
    S = BlockMatrix(S)
    return (d * log(2 * pi) + log(det(S)) + det((x - m) * S.inverse() * (x - m).T)) / 2


def gaussian_max(gaussian_pdf):
    pdf = gaussian_pdf.copy()
    for var, value in gaussian_pdf.Scope.items():
        if value is None:
            pdf.Scope[var] = pdf.Params[('mean', var)]
    return pdf


def gaussian_marginalization(gaussian_pdf, *marginalized_vars):
    var_symbols = gaussian_pdf.Vars.copy()
    var_scope = deepcopy(gaussian_pdf.Scope)
    parameters = deepcopy(gaussian_pdf.Params)
    for marginalized_var in marginalized_vars:
        del var_symbols[marginalized_var]
        del var_scope[marginalized_var]
        p = deepcopy(parameters)
        for key in p:
            if marginalized_var in key:
                del parameters[key]
    if var_scope:
        return gaussian_density_function(var_symbols, parameters, deepcopy(gaussian_pdf.Conds), var_scope)
    else:
        return one_density_function(var_symbols, deepcopy(gaussian_pdf.Conds))


def gaussian_conditioning(gaussian_pdf, conds={}, **kw_conds):
    conds = combine_dict_and_kwargs(conds, kw_conds)
    new_conds = deepcopy(gaussian_pdf.Conds)
    new_conds.update(conds)
    scope = deepcopy(gaussian_pdf.Scope)
    for var in conds:
        del scope[var]
    point_conds = {}
    for var, value in conds.items():
        if value is not None:
            point_conds[gaussian_pdf.Vars[var]] = value
    condition_var_names = list(conds)
    num_condition_vars = len(condition_var_names)
    scope_var_names = list(set(gaussian_pdf.Scope) - set(conds))
    num_scope_vars = len(scope_var_names)
    x_c = []
    m_c = []
    m_s = []
    S_c = [num_condition_vars * [None] for _ in range(num_condition_vars)]   # careful not to create same mutable object
    S_s = [num_scope_vars * [None] for _ in range(num_scope_vars)]   # careful not to create same mutable object
    S_cs = [num_scope_vars * [None] for _ in range(num_condition_vars)]   # careful not to create same mutable object
    for i in range(num_condition_vars):
        x_c += [gaussian_pdf.Vars[condition_var_names[i]]]
        m_c += [gaussian_pdf.Params[('mean', condition_var_names[i])]]
        for j in range(i):
            if ('cov', condition_var_names[i], condition_var_names[j]) in gaussian_pdf.Params:
                S_c[i][j] = gaussian_pdf.Params[('cov', condition_var_names[i], condition_var_names[j])]
                S_c[j][i] = S_c[i][j].T
            else:
                S_c[j][i] = gaussian_pdf.Params[('cov', condition_var_names[j], condition_var_names[i])]
                S_c[i][j] = S_c[j][i].T
        S_c[i][i] = gaussian_pdf.Params[('cov', condition_var_names[i])]
    for i in range(num_scope_vars):
        m_s += [gaussian_pdf.Params[('mean', scope_var_names[i])]]
        for j in range(i):
            if ('cov', scope_var_names[i], scope_var_names[j]) in gaussian_pdf.Params:
                S_s[i][j] = gaussian_pdf.Params[('cov', scope_var_names[i], scope_var_names[j])]
                S_s[j][i] = S_s[i][j].T
            else:
                S_s[j][i] = gaussian_pdf.Params[('cov', scope_var_names[j], scope_var_names[i])]
                S_s[i][j] = S_s[j][i].T
        S_s[i][i] = gaussian_pdf.Params[('cov', scope_var_names[i])]
    for i, j in product(range(num_condition_vars), range(num_scope_vars)):
        if ('cov', condition_var_names[i], scope_var_names[j]) in gaussian_pdf.Params:
            S_cs[i][j] = gaussian_pdf.Params[('cov', condition_var_names[i], scope_var_names[j])]
        else:
            S_cs[i][j] = gaussian_pdf.Params[('cov', scope_var_names[j], condition_var_names[i])].T
    x_c = BlockMatrix([x_c])
    m_c = BlockMatrix([m_c])
    m_s = BlockMatrix([m_s])
    S_c = BlockMatrix(S_c)
    S_s = BlockMatrix(S_s)
    S_cs = BlockMatrix(S_cs)
    S_sc = S_cs.T
    m = (m_s + (x_c - m_c) * S_c.inverse() * S_cs).xreplace(point_conds)
    S = S_s - S_sc * S_c.inverse() * S_cs
    parameters = {}
    index_ranges_from = []
    index_ranges_to = []
    k = 0
    for i in range(num_scope_vars):
        l = k + gaussian_pdf.Vars[scope_var_names[i]].shape[1]
        index_ranges_from += [k]
        index_ranges_to += [l]
        parameters[('mean', scope_var_names[i])] = m[0, index_ranges_from[i]:index_ranges_to[i]]
        for j in range(i):
            parameters[('cov', scope_var_names[j], scope_var_names[i])] =\
                S[index_ranges_from[j]:index_ranges_to[j], index_ranges_from[i]:index_ranges_to[i]]
        parameters[('cov', scope_var_names[i])] =\
            S[index_ranges_from[i]:index_ranges_to[i], index_ranges_from[i]:index_ranges_to[i]]
        k = l
    return gaussian_density_function(deepcopy(gaussian_pdf.Vars), parameters,
                                     new_conds, scope)


def gaussian_sampling(gaussian_pdf, num_samples):
#    scope_vars
#    for scope
#
#    scope_vars = tuple(gaussian_pdf.Scope)
#
#    num_scope_vars = len(scope_vars)
#    m = []
#    S = [num_scope_vars * [None] for _ in range(num_scope_vars)]   # careful not to create same mutable object
#    for i in range(num_scope_vars):
#        m += [gaussian_pdf.Params[('mean', scope_vars[i])]]
#        for j in range(i):
#            if ('cov', scope_vars[i], scope_vars[j]) in gaussian_pdf.Params:
#                S[i][j] = gaussian_pdf.Params[('cov', scope_vars[i], scope_vars[j])]
#                S[j][i] = S[i][j].T
#            else:
#                S[j][i] = gaussian_pdf.Params[('cov', scope_vars[j], scope_vars[i])]
#                S[i][j] = S[j][i].T
#        S[i][i] = gaussian_pdf.Params[('cov', scope_vars[i])]
#    m = BlockMatrix([m]).as_explicit().tolist()[0]
#    S = BlockMatrix(S).as_explicit().tolist()
#    X = multivariate_normal(m, S)
#    samples = X.rvs(num_samples)
#    densities = X.pdf(samples)
#    mappings = {}
#    for i in range(num_samples):
#        fd = {}
#        k = 0
#        for j in range(num_scope_vars):
#            scope_var = scope_vars[j]
#            l = k + gaussian_pdf.Vars[scope_var].shape[1]
#            fd[scope_var] = samples[i, k:l]
#        mappings[FrozenDict(fd)] = densities[i]
    return 0 #discrete_finite_mass_function(deepcopy(gaussian_pdf.Vars), dict(NegLogProb=mappings),
#                                         deepcopy(gaussian_pdf.Conds))


def product_of_2_DiscreteFinitePMFs(pmf_1, pmf_2):
    conds = merge_dicts_ignoring_duplicate_keys_and_none_values(pmf_1.Conds, pmf_2.Conds)
    scope = merge_dicts_ignoring_duplicate_keys_and_none_values(pmf_1.Scope, pmf_2.Scope)
    for var in (set(conds) & set(scope)):
        del conds[var]
    var_symbols = merge_dicts_ignoring_duplicate_keys_and_none_values(pmf_1.Vars, pmf_2.Vars)
    mappings_1 = pmf_1.Params['NegLogProb'].copy()
    mappings_2 = pmf_2.Params['NegLogProb'].copy()
    mappings = {}
    for item_1, item_2 in product(mappings_1.items(), mappings_2.items()):
        var_values_1___frozen_dict, mapping_value_1 = item_1
        var_values_2___frozen_dict, mapping_value_2 = item_2
        same_vars_same_values = True
        for var in (set(var_values_1___frozen_dict) & set(var_values_2___frozen_dict)):
            same_vars_same_values &= (var_values_1___frozen_dict[var] == var_values_2___frozen_dict[var])
        if same_vars_same_values:
            mappings[frozendict(set(var_values_1___frozen_dict.items()) | set(var_values_2___frozen_dict.items()))] =\
                mapping_value_1 + mapping_value_2
    return DiscreteFinitePMF(var_symbols, mappings, conds=conds, scope=scope, prob=False)


def product_of_discrete_finite_probability_mass_function_and_continuous_probability_density_function(pmf, pdf):
    conds = merge_dicts_ignoring_duplicate_keys_and_none_values(pmf.Conds, pdf.Conds)
    scope = merge_dicts_ignoring_duplicate_keys_and_none_values(pmf.Scope, pdf.Scope)
    for var in (set(conds) & set(scope)):
        del conds[var]
    var_symbols = merge_dicts_ignoring_duplicate_keys_and_none_values(pmf.Vars, pdf.Vars)
    mappings = {}
    for var_values___frozen_dict, mapping_value in pmf.Params['NegLogProb'].items():
        mappings[var_values___frozen_dict] = mapping_value + pdf.density_lambda(pdf.Vars)
    return DiscreteFinitePMF(var_symbols, mappings, conds=conds, scope=scope)


def product_of_one_probability_density_function_and_gaussian_probability_density_function(one_pdf, gaussian_pdf):
    conds = merge_dicts_ignoring_duplicate_keys_and_none_values(gaussian_pdf.Conds, one_pdf.Conds)
    scope = deepcopy(gaussian_pdf.Scope, one_pdf.Scope)
    for var in (set(conds) & set(scope)):
        del conds[var]
    var_symbols = merge_dicts_ignoring_duplicate_keys_and_none_values(gaussian_pdf.Vars, one_pdf.Vars)
    return gaussian_density_function(var_symbols, deepcopy(gaussian_pdf.Params), conds, scope)


def product_of_2_gaussian_probability_density_functions(gaussian_pdf_1, gaussian_pdf_2):
    conds = merge_dicts_ignoring_duplicate_keys_and_none_values(gaussian_pdf_1.Conds, gaussian_pdf_2.Conds)
    scope = merge_dicts_ignoring_duplicate_keys_and_none_values(gaussian_pdf_1.Scope, gaussian_pdf_2.Scope)
    for var in (set(conds) & set(scope)):
        del conds[var]
    var_symbols = merge_dicts_ignoring_duplicate_keys_and_none_values(gaussian_pdf_1.Vars, gaussian_pdf_2.Vars)
    parameters = {}
    return gaussian_density_function(var_symbols, parameters, conds, scope)
