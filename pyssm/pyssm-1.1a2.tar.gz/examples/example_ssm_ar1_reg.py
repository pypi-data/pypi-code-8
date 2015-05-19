from numpy import log, ones, column_stack, hstack, mean
from numpy import random, zeros, sqrt
from pymcmc.mcmc import MCMC, CFsampler, IndMH
from pymcmc.regtools import LinearModel, CondScaleSampler
import pylab
from pyssm.ssm import Filter, SimSmoother


def simdata(nobs):
    ht = 1.0 ** 2
    zt = 1.0
    tt = 0.95
    qt = 0.3 ** 2
    gt = 1.0
    rt = 1.0
    mu = 5.0
    a1 = mu
    p1 = qt / (1. - tt ** 2)
    beta = mu * (1.0 - tt)
    wmat = ones((1, 1, nobs))

    filt = Filter(nobs, 1, 1, 1, False, wmat=wmat)
    filt.initialise_system(a1, p1, zt, ht, tt, gt, qt, rt, beta=beta)
    filt.simssm()

    yvec = filt.get_ymat().T.flatten()
    simstate = filt.get_state()
    return yvec, simstate


def simstate(store):
    system = store['simsm'].get_system()
    system.update_tt(store['rho'])

    p1 = system._qt() / (1.0 - store['rho'] ** 2)
    a1 = store['beta'] / (1.0 - store['rho'])

    system.update_a1(a1)
    system.update_p1(p1)

    system.update_beta(store['beta'])

    state = store['simsm'].sim_smoother()

    return state


def simht(store):
    system = store['simsm'].get_system()
    residual = store['simsm'].get_meas_residual()
    ht = store['scale_sampler'].sample(residual.T)
    system.update_ht(ht ** 2)

    return ht ** 2


def prior_rho(store):
    if store['rho'] < 1.0 and store['rho'] > 0.0:
        rho1 = 15.0
        rho2 = 1.5
        return (rho1 - 1.0) * log(store['rho']) + (rho2 - 1.0) * log(1.0 - store['rho'])
    else:
        return -1E256


def prior_sigma(store):
    nu = 10.0
    S = 0.01
    return -(nu + 1) * log(store['sigma']) - S / (2.0 * store['sigma'] ** 2)


def post_rho_sigma(store):
    if store['rho'] < 1.0 and store['rho'] > 0.0:
        system = store['simsm'].get_system()
        p1 = system._qt() / (1.0 - store['rho'] ** 2)
        a1 = store['beta'] / (1.0 - store['rho'])
        system.update_p1(p1)
        system.update_a1(a1)
        system.update_tt(store['rho'])
        system.update_beta(store['beta'])
        system.update_qt(store['sigma'] ** 2)
        lnpr = store['simsm'].log_probability_state()

        #lnpr =  store['simsm'].calc_log_likelihood()
        return lnpr + prior_rho(store) + prior_sigma(store)
    else:
        return -1E256


def cand_rho_sigma(store):
    nobs = store['state'].shape[1]
    store['bayes_reg'].update_yvec(store['state'][0, 1:nobs])
    xmat = column_stack([ones(nobs - 1), store['state'][0, 0:nobs - 1]])
    store['bayes_reg'].update_xmat(xmat)
    sig, beta = store['bayes_reg'].sample()
    return sig, beta[0], beta[1]


def cand_prob(store):
    beta = hstack([store['beta'], store['rho']])
    return store['bayes_reg'].log_posterior_probability(store['sigma'], beta)


def transform_beta(store):
    return store['beta'] / (1.0 - store['rho'])


def main():
    """
    The main routine.
    """

    random.seed(12345)
    nobs = 1000
    nstate = 1
    rstate = 1
    yvec, simulated_state = simdata(nobs)
    data = {'yvec': yvec}

    ht = 1.0
    tt = 0.9
    zt = 1.0
    qt = 0.4
    gt = 1.0
    rt = 1.0
    p1 = qt / (1. - tt ** 2)
    mu = mean(yvec)
    a1 = mu
    beta = mu * (1 - tt)
    wmat = 1.0

    data['simsm'] = SimSmoother(yvec, nstate, rstate,
                                False, properties={'gt': 'eye'},
                                wmat=wmat)
    data['simsm'].initialise_system(a1, p1, zt, ht, tt, gt, qt, rt, beta=beta)
    data['scale_sampler'] = CondScaleSampler(prior=['inverted_gamma', 10.0, 0.01])
    data['bayes_reg'] = LinearModel(yvec[1:nobs], column_stack([ones(nobs - 1), yvec[0:nobs - 1]]))
    samplestate = CFsampler(simstate, zeros((nstate, nobs)), 'state')
    sampleht = CFsampler(simht, ht, 'ht')
    samplesigbetarho = IndMH(cand_rho_sigma, post_rho_sigma,
                             cand_prob, [sqrt(qt), 0.1, tt],
                             ['sigma', 'beta', 'rho'])

    blocks1 = [samplestate, sampleht, samplesigbetarho]
    mcmc = MCMC(5000, 2000, data, blocks1,
                transform={'beta': transform_beta}, runtime_output = True)
    mcmc.sampler()
    mcmc.output(parameters=['ht', 'sigma', 'rho', 'beta'],
               filename='ar1out.txt')

    means, vars = mcmc.get_mean_var('state')
    pylab.plot(range(nobs), means[0], color='k')
    pylab.plot(range(nobs), simulated_state[0], color='k',)
    pylab.title('Simulated vs estimated state')
    pylab.savefig('AR1.pdf')
    pylab.close("all")
    
if __name__ == '__main__':
    main()
