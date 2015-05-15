from __future__ import absolute_import, print_function, division
import datetime
from pathlib import Path
from .constants import CONVERSIONS


# string format for creating a script for hfss.
# need to supply kwargs:
#   datetime
#   project
#   project_name
#   dxfout
#   frequency
#   frequency_units
#   material
#   design
_template = """\
\"\"\"
Script automatically generated on {datetime}
for command line usage.
Opens a project in HFSS, changes the antenna dimensions,
and runs an analysis if applicable.
\"\"\"

# conversion table for converting from MHz, kHz, etc. to Hz
conversions = {
    'THz': 1E12,
    'GHz': 1E9,
    'MHz': 1E6,
    'kHz': 1E3,
    'Hz': 1.0
}


frequency = {frequency} # {frequency_units}
project = r'{project}'
project_name = r'{project_name}'
frequency_units = r'{frequency_units}'
wavelength = 3E8 / frequency

try:
    # Newer HFSS needs to import ScriptEnv; older doesn't.
    import ScriptEnv
    ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
except ImportError:
    pass
oDesktop.OpenProject(project)
oProject = oDesktop.SetActiveProject(project_name)
oDesign = oProject.SetActiveDesign(r'{design}')

oEditor = oDesign.SetActiveEditor('3D Modeler')
oEditor.AssignMaterial(
    [
        "NAME:Selections",
        "Selections:=", "Box1"
    ],
    [
        "NAME:Attributes",
        "MaterialValue:=", "\\\"{material}\\\"",
        "SolveInside:=", True
])
oProject.Save()

# export a dxf file
oEditor.Export(
    [
        "NAME:ExportParameters",
        "File Name:=", r'{dxfout}',
        "Major Version:=", -1,
        "Minor Version:=", -1
    ]
)

""".format

# The base of any HFSS script
# needs to be formatted with
# * datetime
# * frequency (float)
# * frequency_units (str)
# * project (str) path to the new HFSS project
# * project_name (str) usually just the project name with an extension
# * design (str) The name of the design.
_base = """\
\"\"\"
Script automatically generated on {datetime}
for command line usage.
Opens a project in HFSS, changes the antenna dimensions,
and runs an analysis if applicable.
\"\"\"

# conversion table for converting from GHz, MHz, etc. to Hz
conversions = {""" + repr(CONVERSIONS) + """}

def change_var(varname, value):
    oDesign.ChangeProperty([
        "NAME:AllTabs",
        [
            "NAME:LocalVariableTab",
            [
                "NAME:PropServers",
                "LocalVariables"
            ],
            [
                "NAME:ChangedProps",
                ["NAME:{{varname}}".format(varname=varname), "ReadOnly:=", False],
                ["NAME:{{varname}}".format(varname=varname), "Value:=", "{{value}}".format(value=value)]
            ]
        ]
    ])

def change_sweep_value(setup_name, sweep_name, value_name, value):
    \"\"\"
    Change a sweep's value.
    \"\"\"
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:HfssTab",
                [
                    "NAME:PropServers",
                    "AnalysisSetup:{{setup_name}}:{{sweep_name}}".format(
                        setup_name=setup_name, sweep_name=sweep_name)
                ],
                [
                    "NAME:ChangedProps",
                    ["NAME:{{0}}".format(value_name),
                     "MustBeInt:=", False,
                     "Value:=", "{{value}}".format(value=value)],
                ]
            ]
        ])


frequency = {frequency} # {frequency_units}
project = r'{project}'
project_name = r'{project_name}'
frequency_units = r'{frequency_units}'
frequency_hz = frequency * conversions[frequency_units]
wavelength = 3E8 / frequency_hz

try:
    # Newer HFSS needs to import ScriptEnv; older doesn't.
    import ScriptEnv
    ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
except ImportError:
    pass

oDesktop.OpenProject(project)
oProject = oDesktop.SetActiveProject(project_name)
oDesign = oProject.SetActiveDesign(r'{design}')
analysisModule = oDesign.GetModule("AnalysisSetup")"""


def _save():
    """Save the HFSS file."""

    return "oProject.Save()"


def _change_var(varname, value):
    """Change a single HFSS design variable

    Args:
        varname (str) the name of the variable to change
        value (str) the name of the value to change.  This should include units.
    """
    return "change_var(r'{0}', r'{1}')".format(varname, value)


def _change_sweep_value(setup_name, sweep_name, value_name, value):
    """Return a string that can be inserted into an HFSS script to
    change a sweep value.  It must be inserted after the `_base` string."""
    return "change_sweep_value(r'{0}', r'{1}', r'{2}', r'{3}')".format(
        setup_name,
        sweep_name,
        value_name,
        value)


def _change_setup_frequency(setup_name, frequency, units):
    return 'analysisModule.EditSetup(r"{0}", ["NAME:{0}", "Frequency:=", "{1}{2}"])'.format(
        setup_name, frequency, units)


def _run_sweep(sweep):
    """
    Args:
        sweep (.hfss.Sweep): sweep to run.
    """
    return 'oDesign.Analyze("{} : {}")'.format(sweep.setup.name, sweep.name)


class ScriptWriter(object):
    """Writes a script based on an HFSSChanger instance."""

    def __init__(self, hfss_changer):
        """
        Args:
            hfss_changer (HFSSChanger): an HFSSChanger instance to
              write a script based on.

        """
        self.hfss_changer = hfss_changer
        self.f = hfss_changer.frequency
        self.script_parts = []
        project_name = Path(hfss_changer.new).stem
        base = _base.format(datetime=datetime.datetime.now(),
                            frequency=self.f.value,
                            frequency_units=self.f.units,
                            project=hfss_changer.new,
                            project_name=project_name,
                            design=hfss_changer.design_name)

        self.script_parts.append(base)
        for varname, value in hfss_changer.variables_to_change.items():
            self.script_parts.append(_change_var(varname=varname, value=value))

        # Iterate through setups to change sweep
        for setup in hfss_changer.setups.values():
            self.script_parts.extend(self.setup_changes(setup))
        # Iterate over them _again_ to see what sweeps to run
        for setup in hfss_changer.setups.values():
            for sweep in setup.sweeps.values():
                if sweep.run:
                    self.script_parts.append(_run_sweep(sweep))
        self.script_parts.append(_save())

    def _change_sweep(self, setup, sweep):
        """Change a sweep whose values are set absolutely.

        Args:
            setup (.hfss.Setup): The setup the sweep belongs to
            sweep (.hfss.Sweep): The sweep that needs to be changed.
        """

        start = _change_sweep_value(setup.name, sweep.name, 'Start', sweep.start)
        stop = _change_sweep_value(setup.name, sweep.name, 'Stop', sweep.stop)
        step = _change_sweep_value(setup.name, sweep.name, 'Step Size', sweep.step)
        return start, stop, step

    def setup_changes(self, setup):
        """
        Args:
            setup (.hfss.Setup): The setup to do
        """
        setup_changes = []
        for sweep in setup.sweeps.values():
            start, stop, step = self._change_sweep(setup, sweep)
            setup_changes.extend([start, stop, step])
        setup_f = _change_setup_frequency(setup.name,
                                          self.f.value,
                                          self.f.units)
        setup_changes.append(setup_f)
        return setup_changes

    def __str__(self):
        return '\n'.join(self.script_parts)


