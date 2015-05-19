import numpy as np
import os
import pymcmc.mcmc as mcmc
import pymcmc.regtools as regtools
import pylab
import pyssm.ssm as ssm

""" Get the path for the data. If this was
installed using setup.py it will be in the
data directory of the module"""

datadir = os.path.join(os.path.dirname(ssm.__file__), 'data')


def update_tt(store):
    system = store['simsm'].get_system()
    tt = system.tt()
    tt[2, 2] = store['rho'] * np.cos(store['lambda'])
    tt[2, 3] = store['rho'] * np.sin(store['lambda'])
    tt[3, 2] = -tt[2, 3]
    tt[3, 3] = tt[2, 2]
    system.update_tt(tt)


def update_p1(store):
    system = store['simsm'].get_system()
    p1 = system.p1()
    p1[2, 2] = store['sigma_cycle'] ** 2 / \
               (1. - store['rho'] ** 2)
    p1[3, 3] = p1[2, 2]
    system.update_p1(p1)


def update_qt(store):
    system = store['simsm'].get_system()
    qt = np.zeros((3, 3))
    qt[0, 0] = store['sigma_level'] ** 2
    qt[1, 1] = store['sigma_cycle'] ** 2
    qt[2, 2] = qt[1, 1]
    system.update_qt(qt)


def simstate(store):
    update_tt(store)
    update_qt(store)
    update_p1(store)
    return store['simsm'].sim_smoother()


def simht(store):
    residual = store['simsm'].get_meas_residual()
    ht = np.linalg.inv(
        store['scale_sampler'].sample(residual.T)
        )
    system = store['simsm'].get_system()
    system.update_ht(ht)
    
    return ht


def simsig_level(store):
    update_tt(store)
    residual = store['simsm'].get_state_residual(
        state_index=[0])
    sigma_level = store['scale_sampler2'].sample(
        residual.T)
    return sigma_level


def posterior_sig_cycle(store):
    if store['sigma_cycle'] > 0:
        update_tt(store)
        update_qt(store)
        update_p1(store)
        probstate = store['simsm'].log_probability_state()
        #probstate = store['simsm'].log_likelihood()
        return probstate + prior_sig(store['sigma_cycle'])
    else:
        return -1E256


def prior_sig(sig):
    nu = -1.
    S = 0.0
    return -(nu + 1) * np.log(sig) - S / (2.0 * sig ** 2)


def posterior_lambda(store):
    update_tt(store)
    lnpr = store['simsm'].log_probability_state()
    #lnpr = store['simsm'].log_likelihood()
    return lnpr + prior_lambda(store)


def prior_lambda(store):
    """flat prior restricting the period of the cycle to be between 10
    months and 14 months"""
    if store['lambda'] > np.pi / 20. and store['lambda'] < 2 * np.pi / 4.:
        return 0.0
    else:
        return -1E256


def posterior_rho(store):
    if store['rho'] > 0 and store['rho'] < 1.0:
        update_tt(store)
        update_p1(store)
        lnpr = store['simsm'].log_probability_state()
        #lnpr = store['simsm'].log_likelihood()
        return lnpr + prior_rho(store)
    else:
        return -1E256


def prior_rho(store):
    rho1 = 15.0
    rho2 = 1.5
    return (rho1 - 1.0) * np.log(store['rho']) + (rho2 - 1.) * \
           np.log(1. - store['rho'])


def main():
    np.random.seed(12345)
    filename = os.path.join(datadir, 'farmb.txt')
    ymat = np.loadtxt(filename).T / 1000.
    nseries, nobs = ymat.shape
    data = {'ymat': ymat}

    nstate = 4
    rstate = 3
    ht = np.eye(nseries)
    zt = np.column_stack([np.ones(nseries), np.zeros(nseries),
                          np.ones(nseries), np.zeros(nseries)])
    rt = np.ones(nseries)
    tt = np.zeros((nstate, nstate))
    rho = 0.9
    lamb = 2. * np.pi / 20.
    tt[0, 0] = 1.0
    tt[0, 1] = 1.0
    tt[1, 1] = 1.0
    tt[2, 2] = rho * np.cos(lamb)
    tt[2, 3] = rho * np.sin(lamb)
    tt[3, 2] = -tt[2, 3]
    tt[3, 3] = tt[2, 2]

    sig_cycle = 0.3
    sig_level = 0.3
    qt = np.diag(np.array([sig_level, sig_cycle, sig_cycle]) ** 2)
    gt = np.zeros((nstate, rstate))
    gt[0, 0] = 1.0
    gt[2:, 1:] = np.eye(2)
    a1 = np.array([7.5, 0.000, 0.0, 0.0])
    p1 = np.zeros((nstate, nstate))
    p1[0, 0] = 10.
    p1[1, 1] = 10.
    p1[2, 2] = qt[2, 2] / (1 - rho ** 2)
    p1[3, 3] = p1[2, 2]

    timevar = False
    data['simsm'] = ssm.SimSmoother(ymat, nstate, rstate, timevar,
                                properties={'rt': 'eye'})
    data['simsm'].initialise_system(a1, p1, zt, ht, tt, gt, qt, rt)

    prior_wishart = ['wishart', 10 * np.ones(nseries), 0.1 * np.eye(nseries)]
    data['scale_sampler'] = regtools.CondScaleSampler(prior=prior_wishart)
    data['scale_sampler2'] = regtools.CondScaleSampler(
        prior=['inverted_gamma', 10, 0.1])

    samplestate = mcmc.CFsampler(simstate,
                                 np.zeros((nstate, nobs)),
                                 'state', store='none')
    sampleht = mcmc.CFsampler(simht, ht, 'ht')
    samplesig_level = mcmc.CFsampler(simsig_level,
                                     sig_level, 'sigma_level')
    samplesig_cycle = mcmc.RWMH(posterior_sig_cycle, 0.05,
                                sig_cycle ** 2, 'sigma_cycle',
                                adaptive='GFS')
    samplerho = mcmc.RWMH(posterior_rho, 0.09, rho, 'rho', adaptive='GFS')
    samplelambda = mcmc.RWMH(posterior_lambda, 1.03, lamb,
                             'lambda', adaptive='GFS')

    blocks = [samplestate, sampleht, samplesig_cycle,
              samplesig_level, samplerho, samplelambda]
    mcmcobj = mcmc.MCMC(8000, 3000, data, blocks, runtime_output=True)
    mcmcobj.sampler()
    mcmcobj.output(parameters=['rho', 'lambda', 'sigma_level', 'sigma_cycle'])

    means, vars = mcmcobj.get_mean_var('state')

    pylab.subplot(2, 1, 1)
    pylab.title("Trend Cycle Model")
    pylab.plot(ymat.T, color='k')
    pylab.plot(means[0], color='k')
    pylab.subplot(2, 1, 2)
    pylab.plot(means[2], color='k')
    pylab.savefig('trendcycle.pdf')
    pylab.close("all")
    
if __name__ == '__main__':
    main()
