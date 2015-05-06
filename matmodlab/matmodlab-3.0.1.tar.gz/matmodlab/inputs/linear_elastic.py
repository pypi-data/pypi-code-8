#!/usr/bin/env mmd
import random
from matmodlab import *
from StringIO import StringIO

RUNID = 'linear_elastic'
K = 9.980040E+09
G = 3.750938E+09
LAM = K - 2.0 / 3.0 * G
E   = 9.0 * K * G / (3.0 * K + G)
NU  = (3.0 * K - 2.0 * G) / (2.0 * (3.0 * K + G))


def run_biax_strain_ext_stressc():
    runid = RUNID + '_biax_strain_ext_stressc'
    mps = MaterialPointSimulator(runid)

    # set up the material
    parameters = {'K': K, 'G': G}
    mps.Material('pyelastic', parameters)

    # set up the driver
    path = '''
      0           0.0                0.0                0.0
      1 11230352666.666668 11230352666.666668  7479414666.666667
      2 22460705333.333336 22460705333.333336 14958829333.333334
      3 11230352666.666668 11230352666.666668  7479414666.666667
      4           0.0                0.0                0.0
      '''
    mps.DataSteps(StringIO(path), frames=50, descriptors='SSS')

    # run the model
    mps.run()


def run_biax_strain_comp_stressc():

    runid = RUNID + '_biax_strain_comp_stressc'

    # set up and the model
    mps = MaterialPointSimulator(runid)

    # set up the material
    parameters = {'K': K, 'G': G}
    mps.Material('pyelastic', parameters)

    # set up the driver
    path = '''
      0            0.0                 0.0                 0.0
      1 -11230352666.666668 -11230352666.666668  -7479414666.666667
      2 -22460705333.333336 -22460705333.333336 -14958829333.333334
      3 -11230352666.666668 -11230352666.666668  -7479414666.666667
      4            0.0                 0.0                 0.0
      '''
    mps.DataSteps(StringIO(path), frames=50, descriptors='SSS')

    # run the model
    mps.run()

def run_biax_strain_ext_strainc():

    runid = RUNID + '_biax_strain_ext_strainc'

    # set up the model
    mps = MaterialPointSimulator(runid)

    # set up the material
    parameters = {'K': K, 'G': G}
    mps.Material('pyelastic', parameters)

    # set up the driver
    path = '''
      0 0 0 0
      1 1 1 0
      2 2 2 0
      3 1 1 0
      4 0 0 0
      '''
    mps.DataSteps(StringIO(path), frames=50, descriptors='EEE', scale=.5)

    # set up and run the model
    mps.run()

def run_biax_strain_comp_strainc():

    runid = RUNID + '_biax_strain_comp_strainc'

    # set up the model
    mps = MaterialPointSimulator(runid)

    # set up the material
    parameters = {'K': K, 'G': G}
    mps.Material('pyelastic', parameters)

    # set up the driver
    path = '''
      0 0 0 0
      1 1 1 0
      2 2 2 0
      3 1 1 0
      4 0 0 0
      '''
    mps.DataSteps(StringIO(path), frames=50, descriptors='EEE', scale=-.5)

    # run the model
    mps.run()


def run_uniax_strain_comp_strainc():

    runid = RUNID + '_uniax_strain_comp_strainc'

    # set up the model
    mps = MaterialPointSimulator(runid)

    # set up the material
    parameters = {'K': K, 'G': G}
    mps.Material('pyelastic', parameters)

    # set up the driver
    path = '''
      0 0 0 0
      1 1 0 0
      2 2 0 0
      3 1 0 0
      4 0 0 0
      '''
    mps.DataSteps(StringIO(path), frames=50, scale=-.5, descriptors='EEE')

    # run the model
    mps.run()

def run_uniax_strain_ext_strainc():

    runid = RUNID + '_uniax_strain_ext_strainc'

    # set up the model
    mps = MaterialPointSimulator(runid)

    # set up the material
    parameters = {'K': K, 'G': G}
    mps.Material('pyelastic', parameters)

    # set up the driver
    path = '''
      0 0 0 0
      1 1 0 0
      2 2 0 0
      3 1 0 0
      4 0 0 0
      '''
    mps.DataSteps(StringIO(path), frames=50, scale=.5, descriptors='EEE')

    # run the model
    mps.run()

def run_uniax_strain_comp_stressc():

    runid = RUNID + '_uniax_strain_comp_stressc'

    # set up the model
    mps = MaterialPointSimulator(runid)

    # set up the material
    parameters = {'K': K, 'G': G}
    mps.Material('pyelastic', parameters)

    # set up the driver
    path = '''
      0            0.0                 0.0                 0.0
      1  -7490645333.333334 -3739707333.3333335 -3739707333.3333335
      2 -14981290666.666668 -7479414666.6666667 -7479414666.6666667
      3  -7490645333.333334 -3739707333.3333335 -3739707333.3333335
      4            0.0                 0.0                 0.0
      '''
    mps.DataSteps(StringIO(path), frames=50, descriptors='SSS')

    # run the model
    mps.run()


def run_uniax_strain_ext_stressc():

    runid = RUNID + '_uniax_strain_ext_stressc'

    # set up the model
    mps = MaterialPointSimulator(runid)

    # set up the material
    parameters = {'K': K, 'G': G}
    mps.Material('pyelastic', parameters)

    # set up the driver
    path = '''
      0           0.0               0.0                0.0
      1  7490645333.333334 3739707333.3333335 3739707333.3333335
      2 14981290666.666668 7479414666.6666667 7479414666.6666667
      3  7490645333.333334 3739707333.3333335 3739707333.3333335
      4           0.0               0.0                0.0
      '''
    mps.DataSteps(StringIO(path), frames=50, descriptors='SSS')

    # run the model
    mps.run()

if __name__ == '__main__':
    #run_biax_strain_ext_strainc()
    #run_biax_strain_comp_strainc()
    #run_biax_strain_ext_stressc()
    #run_biax_strain_comp_stressc()
    #run_uniax_strain_ext_stressc()
    #run_uniax_strain_comp_stressc()
    pass
