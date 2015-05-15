from hfsslib import hfss

import pytest


# Use a fixture so that the parsing of the .aedt file only happens once.
# This saves time when running tests.
@pytest.fixture(scope='module')
def hfss_changer():
    return hfss.HFSSChanger('AntennaTemplate.aedt', 'AntennaTemplate2.aedt', '300MHz')


def test_parse_hfss_sweeps(hfss_changer):
    hfss_template = hfss_changer._file_data
    assert type(hfss_template) is hfss.HFSSNode
    assert type(hfss_template.AnsoftProject) == hfss.HFSSNode
    # as long as none of these raise, we're actually okay.  That's why
    # we don't need assertions.
    model = hfss_template.AnsoftProject.HFSSModel
    analysis_setup = model.AnalysisSetup
    solve_setups = analysis_setup.SolveSetups
    setup8 = solve_setups.Setup8
    sweeps = setup8.Sweeps
    sweep1 = sweeps.Sweep1
    with pytest.raises(KeyError):
        sweeps['Sweep8']
    with pytest.raises(AttributeError):
        sweeps.Sweep8


def test_parse_hfss_vars(hfss_changer):
    hfss_template = hfss_changer._file_data
    variables = hfss_template.AnsoftProject.HFSSModel.ModelSetup.Properties
    assert 'angle22' in variables
    assert 'hsub' in variables
    assert variables.ws == '1mm'


def test_setup_access_from_attribute(hfss_changer):
    assert type(hfss_changer.Setup8) is hfss.Setup
    sweep3 = hfss_changer.Setup8.Sweep3
    assert type(sweep3) is hfss.Sweep
    assert sweep3.start == hfss.Frequency('300MHz')
    assert sweep3.stop == hfss.Frequency('550MHz')
    assert sweep3.step == hfss.Frequency('1MHz')

    # Make sure it doesn't try to get a *setup* that doesn't exist.
    with pytest.raises(AttributeError):
        hfss_changer.Setup9

    # Make sure it doesn't get a *sweep* that doesn't exist.
    with pytest.raises(AttributeError):
        hfss_changer.Setup8.Sweep88


def test_var_access_from_attribute(hfss_changer):
    # should automatically access hfss variables.
    assert hfss_changer.hsub == '0.147mm'


def test_Frequency():
    # the following cases should result in 100 Hz frequency.
    for f in (hfss.Frequency('100'),
              hfss.Frequency(100),
              hfss.Frequency(100, 'Hz'),
              hfss.Frequency('100Hz')):
        assert f.value == 100
        assert f.units == 'Hz'

    for f in (hfss.Frequency('200MHz'),
              hfss.Frequency(200, 'MHz')):

        assert f.value == 200
        assert f.units == 'MHz'

    # better test some floating point values
    f = hfss.Frequency('200.3e-5GHz')
    assert f.value == 200.3e-5
    assert f.units == 'GHz'

    f1 = f
    f2 = hfss.Frequency('200.3e-2MHz')
    assert f1 == f2


def test_change_sweep():
    setup = hfss.Setup('Setup1', '1GHz')
    sweep = hfss.Sweep(setup, 'Sweep1', '200MHz', '400MHz', '20MHz')

    assert sweep.start == hfss.Frequency(200, 'MHz')
    assert sweep.stop == hfss.Frequency(400, 'MHz')
    assert sweep.step == hfss.Frequency(20, 'MHz')

    sweep.change_by_fraction(0.1, 0.2, 0.01)

    assert sweep.start == hfss.Frequency(900, 'MHz')
    assert sweep.stop == hfss.Frequency(1200, 'MHz')
    assert sweep.step == hfss.Frequency(10, 'MHz')

