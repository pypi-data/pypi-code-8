import numpy as np
import os
import pylab

import pymcmc.mcmc as mcmc
import pymcmc.regtools as regtools

import pyssm.ssm as ssm

""" Get the path for the data. If this was installed using setup.py
 it will be in the data directory of the module"""
datadir = os.path.join(os.path.dirname(ssm.__file__), 'data')


def update_gt(store):
    system = store['simsm'].get_system()
    gt = np.eye(2) * store['sigma']
    system.update_gt(gt)


def simstate(store):
    update_gt(store)
    #import pdb
    #pdb.set_trace()
    state = store['simsm'].sim_smoother()
    return state


def sim_ht(store):
    residual = store['simsm'].get_meas_residual()
    sqrtht = store['scale_sampler'].sample(residual.T)
    system = store['simsm'].get_system()
    ht = sqrtht ** 2
    system.update_ht(ht)
    return ht


def post_sigma(store):
    if store['sigma'] > 0:
        update_gt(store)
        lnpr = store['simsm'].log_likelihood()
        #lnpr = store['simsm'].log_probability_state(diffuse = True)

        return lnpr + prior_sigma(store['sigma'])
    else:
        return -1E256


def prior_sigma(sigma):
    nu = 10
    S = 0.1
    return -(nu + 1) * np.log(sigma) - 0.5 * S / sigma ** 2


def main():
    np.random.seed(1234)
    data = np.loadtxt(os.path.join(datadir, 'motorcycle.txt'))
    data = data[data[:, 1] > 0]
    yvec = data[:, 2]
    delta = data[:, 1]
    nobs = yvec.shape[0]
    nstate = 2
    rstate = 2
    data = {'yvec': yvec}

    sigeps = 0.9
    ht = sigeps ** 2
    rt = 1.
    zt = np.array([[1.0, 0.0]])
    tt = np.zeros((2, 2, nobs))
    tt[0, 0, :] = 1.
    tt[1, 1, :] = 1.
    tt[0, 1, :] = delta

    sigma = 0.3
    qt = np.zeros((2, 2, nobs))
    qt[0, 0, :] = delta ** 3 / 3.
    qt[0, 1, :] = qt[1, 0, :] = delta ** 2 / 2
    qt[1, 1, :] = delta

    gt = np.eye(nstate) * sigma
    a1 = np.zeros(2)
    p1 = np.eye(2)
    wmat = np.zeros((2, 2, nobs))

    data['simsm'] = ssm.SimSmoother(yvec, nstate, rstate,
                           timevar={'tt': True, 'qt': True},
                           properties={'rt': 'eye'}, wmat=wmat,
                           joint_sample=['diffuse', np.eye(2)])

    data['simsm'].initialise_system(a1, p1, zt, ht, tt, gt, qt, rt)
    data['scale_sampler'] = regtools.CondScaleSampler(
        prior=['inverted_gamma', 10, 0.1]
        )

    samplestate = mcmc.CFsampler(simstate, np.zeros((nstate, nobs)), 'state',
                                 store='none')
    sample_ht = mcmc.CFsampler(sim_ht, np.var(yvec), 'ht')
    sample_sigma = mcmc.RWMH(post_sigma, 1., 0.2, 'sigma', adaptive='GFS')

    blocks = [samplestate, sample_ht, sample_sigma]
    mcmcobj = mcmc.MCMC(8000, 3000, data, blocks, runtime_output=True)
    mcmcobj.sampler()
    mcmcobj.output(parameters=['ht', 'sigma'], filename='spline.out')

    means, vars = mcmcobj.get_mean_var('state')
    pylab.plot(np.cumsum(delta), yvec, '.', color='k')
    pylab.title("Smoothing spline for motorcycle acceleration data.")
    pylab.plot(np.cumsum(delta), means[0], color='k')
    pylab.savefig('spline.pdf')
    pylab.close("all")

if __name__ == '__main__':
    main()
