PythonAny = any
PythonAll = all
from numpy import isscalar, ndarray, asscalar
from oologfcn import OpenOptException

    
def formDictOfFixedFuncs(oof, dictOfFixedFuncs, areFixed, startPoint):
    from FuncDesigner.distribution import stochasticDistribution
    dep = oof.Dep#set([oof]) if oof.is_oovar else oof._getDep()
    # TODO: rework it as mixein of fixed and stoch variables
    if PythonAll((isinstance(startPoint[t], stochasticDistribution) or areFixed(set([t]))) for t in dep):
        dictOfFixedFuncs[oof] = oof(startPoint)#TODO: add fixity ID as additional argument to the func

def linear_render(f, D, Z):
    import FuncDesigner as fd
    if len(D) == 0:
        raise OpenOptException('probably you try to optimize a fixed constant')
    if f.is_oovar: 
        return f
    ff = f(Z)
    name, tol, _id = f.name, f.tol, f._id
    tmp = [(v if isscalar(val) and val == 1.0 else v * (val if type(val) != ndarray or val.ndim < 2 else val.flatten())) \
    for v, val in D.items()]

    c = ff if isscalar(ff) or ff.ndim <= 1 else asscalar(ff)
    if c != 0: tmp.append(c)
    f = tmp[0] if len(tmp) == 1 else tmp[0]+tmp[1] if len(tmp) == 2 else fd.sum(tmp)
    
    f.name, f.tol, f._id = name, tol, _id
    
    return f



def hasStochDep(s, x0):
    from FuncDesigner import oofun, ooarray
    from FuncDesigner.distribution import stochasticDistribution
#    print [isinstance(t, stochasticDistribution) for t in s.Dep]
    cond1 = (isinstance(s, oofun) and PythonAny(isinstance(x0[t], stochasticDistribution) for t in s.Dep))
    cond2 = (isinstance(s, ooarray) and PythonAny(hasStochDep(t, x0) for t in s.view(ndarray)))
    return cond1 or cond2
#    (isinstance(s, ooarray) and PythonAny(hasStochDep(t) for t in s.view(ndarray)))
    

def formDictOfRedirectedFuncs(elem, p):
    from FuncDesigner.overloads import prod as fd_prod
    from FuncDesigner import mean as fd_mean, oofun, abs as fd_abs, std as fd_std, var as fd_var
    x0 = p._x0
#    if not isinstance(elem, oofun):# for more safety
#        return 
    #!!!!!!!!!!!! TODO: handle ooarray
    
    if not hasStochDep(elem, x0):
        return
    Iterator = elem.input if not elem._isSum else elem._summation_elements
    for elem_ in Iterator:
        if not isinstance(elem_, oofun):
            continue
        if elem_.engine in ('mean', 'std', 'var'):
            assert len(elem_.input) == 1, 'bug in FD kernel'
            inp = elem_.input[0]
            if inp._isProd:
                stochElems = [s for s in inp._prod_elements if hasStochDep(s, x0)]
                ordinaryElems = [s for s in inp._prod_elements if not hasStochDep(s, x0)]
                
                newElem = \
                fd_prod(ordinaryElems) * fd_mean(fd_prod(stochElems)) if elem_.engine == 'mean' else \
                fd_abs(fd_prod(ordinaryElems)) * fd_std(fd_prod(stochElems)) if elem_.engine == 'std' else \
                fd_prod(ordinaryElems)**2 * fd_var(fd_prod(stochElems)) # for elem_.engine == 'var'
                
                p._dictOfRedirectedFuncs[elem_] = newElem
                elem_.input = [newElem]
        else:
            pass
     
# TODO: redirection for linear rest of sum
