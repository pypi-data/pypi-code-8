from testconf import *

@pytest.mark.add_on
class TestAddonModels(StandardTypeTest):
    '''Test the abaqus model wrappers'''
    temp = (75, 95)
    time_f = 50
    E, Nu = 500, .45

    def setup(self):
        '''Set up test to allow abaqus models to run'''
        remove(join(LIB_D, 'umat.so'))

    @pytest.mark.visco
    def test_visco(self):
        mps = MaterialPointSimulator('visco_addon', initial_temperature=75,
                                     d=this_directory, verbosity=0)
        parameters = [self.E, self.Nu]
        expansion = Expansion('isotropic', [1.E-5])
        prony_series =  np.array([[.35, 600.], [.15, 20.], [.25, 30.],
                                  [.05, 40.], [.05, 50.], [.15, 60.]])
        viscoelastic = Viscoelastic('prony', prony_series)
        trs = TRS('wlf', [75, 35, 50])
        mps.Material('umat', parameters, source_files=['neohooke.f90'],
                     source_directory=os.path.join(MAT_D, 'abaumats'),
                     expansion=expansion, viscoelastic=viscoelastic, trs=trs)
        mps.MixedStep(components=(.1, 0., 0.), descriptors='ESS', increment=1.,
                      temperature=75., frames=10)
        mps.StrainRateStep(components=(0., 0., 0.), increment=50.,
                           temperature=95., frames=50)
        try:
            # test passes if it runs
            mps.run()
        except BaseException:
            raise Exception('visco_addon failed to run')
        self.completed_jobs.append('visco_addon')

    @pytest.mark.expansion
    def test_expansion(self):
        mps = MaterialPointSimulator('expansion_addon', verbosity=0,
                                     d=this_directory)
        parameters = [self.E, self.Nu]
        expansion = Expansion('isotropic', [1.E-5])
        mps.Material('umat', parameters, source_files=['neohooke.f90'],
                     source_directory=os.path.join(MAT_D, 'abaumats'),
                     expansion=expansion)
        mps.MixedStep(components=(.1,0,0), descriptors='ESS',
                      temperature=75., frames=10)
        mps.StrainRateStep(components=(0,0,0), temperature=95., frames=10)
        try:
            # test passes if it runs
            mps.run()
        except BaseException:
            raise Exception('expansion_addon failed to run')
        self.completed_jobs.append('expansion_addon')

