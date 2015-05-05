from testconf import *
from matmodlab import *
from matmodlab.mmd.simulator import StrainStep

@pytest.mark.abaqus
class TestAbaqusModels(StandardTypeTest):
    '''Test the abaqus model wrappers'''
    E = 500
    Nu = .45
    C10 = E / (4. * (1. + Nu))
    D1 = 6. * (1. - 2. * Nu) / E
    def setup(self):
        '''Set up test to allow abaqus models to run'''
        # by removing the abaqus libs, they will be rebuilt for each test
        for lib in ('umat', 'uhyper', 'uanisohyper_inv'):
            remove(join(LIB_D, lib + '.so'))

    @pytest.mark.uhyper
    def test_uhyper(self):
        mps = MaterialPointSimulator('uhyper', verbosity=0,
                                     d=this_directory)
        param_names = ('C10', 'D1')
        parameters = dict(zip(param_names, (self.C10, self.D1)))
        depvar = ['MY_SDV_1', 'MY_SDV_2']
        mps.Material('uhyper', parameters, source_files=['uhyper.f90'],
                     source_directory='{0}/materials/abaumats'.format(ROOT_D),
                     param_names=param_names, depvar=depvar)
        mps.GenSteps(StrainStep, components=(1,0,0), increment=2*pi,
                     steps=200, frames=1, scale=.1, amplitude=(np.sin,))
        mps.run(termination_time=1.8*pi)
        status = self.compare_with_baseline(mps)
        assert status == 0
        self.completed_jobs.append(mps.runid)

    @pytest.mark.uanisohyper_inv
    @pytest.mark.skipif(True, reason='baseline not established')
    def test_uanisohyper_inv(self):
        mps = MaterialPointSimulator('uanisohyper_inv', verbosity=0,
                                     d=this_directory)
        C10, D, K1, K2, Kappa = 7.64, 1.e-8, 996.6, 524.6, 0.226
        parameters = np.array([C10, D, K1, K2, Kappa])
        a = np.array([[0.643055,0.76582,0.0]])
        mps.Material('uanisohyper_inv', parameters, fiber_dirs=a,
                     source_files=['uanisohyper_inv.f'],
                     source_directory='{0}/materials/abaumats'.format(ROOT_D))
        mps.GenSteps(StrainStep, components=(1,0,0), increment=2*pi,
                     steps=200, frames=1, scale=.1, amplitude=(np.sin,))
        mps.run(termination_time=1.8*pi)

    @pytest.mark.umat
    @pytest.mark.thermoelastic
    #@pytest.mark.skipif(True, reason='Test is incompatible with other umats')
    def test_umat_thermoelastic(self):
        # This test clashes with other umat's so it is disabled.  When I can
        # figure out how to reliably reload umats, it'll be added back.
        # Issue: once a module is loaded, I can't figure out how to delete it
        # from sys.modules and reload it reliably. This is important for umat
        # materials since many umats share the common library name lib.umat.
        # Once lib.umat is loaded for one umat, it would have to be wiped,
        # rebuilt, and reloaded for another. The problem is trivially avoided
        # by only running one umat per interpreter session. But, when testing,
        # we want to test several umats - so this isn't an option.
        E0, NU0, T0 = 29.E+06, .33, 298.E+00
        E1, NU1, T1 = 29.E+06, .33, 295.E+00
        TI, ALPHA = 298., 1.E-5
        mps = MaterialPointSimulator('umat_thermoelastic', verbosity=0,
                                     d=this_directory, initial_temperature=TI)
        parameters = np.array([E0, NU0, T0, E1, NU1, T1, ALPHA, TI])
        mps.Material('umat', parameters, depvar=12,
                     source_files=['thermoelastic.f90'],
                     source_directory=os.path.join(MAT_D, 'abaumats'))
        mps.MixedStep(components=(.2, 0, 0), descriptors='ESS',
                      temperature=500, frames=100)
        mps.run()
        out = mps.get('TEMP', 'STRAIN_XX', 'STRESS_XX')
        for (i, row) in enumerate(out[1:], start=1):
            temp, eps, sig = row
            dtemp = temp - out[0,0]
            ee = eps - ALPHA * dtemp
            diff = E0 * ee - sig
            assert abs(diff) <= 1.e-8
        self.completed_jobs.append(mps.runid)
