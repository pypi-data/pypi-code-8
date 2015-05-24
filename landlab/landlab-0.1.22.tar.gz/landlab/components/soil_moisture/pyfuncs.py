import numpy as np


def sai_loop_0(sini, fc, sc, wp, beta, mu, nu, nuw, tfc, tsc, twp):
    i = np.where(sini >= fc)
    tfc[i] = (
      (1. / (beta[i] * (mu[i] - nu[i]))) *
      (beta[i] * (fc[i] - sini[i]) +
       np.log((nu[i] - mu[i] +
               mu[i] * np.exp(beta[i] * (sini[i] - fc[i]))) / nu[i])))
    tsc[i] = ((fc[i] - sc[i]) / nu[i]) + tfc[i]
    twp[i] = (((sc[i] - wp[i]) / (nu[i] - nuw[i])) *
              np.log(nu[i] / nuw[i]) + tsc[i])
