"""
This contains the :class:`HFSSChanger` class, which provides an object-oriented
way to make changes to HFSS files.

"""

from __future__ import division, print_function, absolute_import

# stdlib imports
import collections
import logging
import os
import re
import shutil
import subprocess
import tempfile
try:
    import _winreg as winreg
except ImportError:  # just winreg on Py3
    import winreg

from .hfss_writer import ScriptWriter
from .constants import c, CONVERSIONS
# third-party imports
from pathlib import Path

__all__ = ['HFSSChanger', 'Frequency']

# Location of the base ansoft key in the Windows registry
HFSS_2015_BASE = r'SOFTWARE\Ansoft\ElectronicsDesktop'
HFSS_2014_BASE = r'SOFTWARE\Ansoft\HFSS'
HFSS_2015_EXE = r'ansysedt.exe'
HFSS_2014_EXE = r'hfss.exe'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Setup(object):
    """A representation of an HFSS Analysis setup.

    It has a solution frequency and a number of sweeps.

    """

    def __init__(self, name, frequency):
        self.name = name
        self.frequency = Frequency(frequency)
        self.sweeps = collections.OrderedDict()

    def add_sweep(self, sweep):
        self.sweeps[sweep.name] = sweep

    def __getattr__(self, name):
        try:
            return self.sweeps[name]
        except:
            msg = 'Setup {} has no sweep with the name {}'.format(
                  self.name, name)
            raise AttributeError(msg)

    def run(self):
        for sweep in self.sweeps.values():
            sweep.run = True

    def __repr__(self):
        return "{} with sweeps {}".format(self.name, list(self.sweeps.values()))


class Sweep(object):
    """A representation of an HFSS Sweep.

    It has a name, start frequency, stop frequency, and step frequency.

    """
    def __init__(self, setup, name, start, stop, step):
        """

        Args:
            setup (Setup): The :class:`Setup` this sweep belongs to.
            name (str): The name of this sweep.
            start (str | float | Frequency): The starting frequency for this sweep.
            stop (str | float | Frequency): The stopping frequency for this sweep.
            step (str | float | Frequency): The step frequency for this sweep.
        """
        self.setup = setup
        self.name = name
        self.start = Frequency(start)
        self.stop = Frequency(stop)
        self.step = Frequency(step)
        self.run = False

    def __repr__(self):
        format_str = '{}: {} to {}, {} interval'
        return format_str.format(self.name, self.start, self.stop, self.step)

    def change_by_fraction(self, fraction_below, fraction_above, fraction_step):
        """Set the new sweep frequency range based on the solution frequency.

        Args:
            fraction_below (float): The fraction below the solution frequency
              you want to sweep. For example, a value of ``0.1`` will set the
              starting frequency to ``frequency - frequency*0.1`` (10% below
              the solution frequency).
            fraction_above (float): The fraction above the solution frequency
              you want to sweep. For example, a value of ``0.1`` will set the
              starting frequency to ``frequency + frequency*0.1`` (10% below
              the solution frequency).
            fraction_step (float): The fraction of the solution frequency the
              sweep step size will be.  For example, a value of 0.01 will set
              the step frequency to ``frequency * 0.01`` (1% of the solution
              frequency)

        """
        if None in (fraction_below, fraction_above, fraction_step):
            raise ValueError('fraction_below, fraction_above, and fraction_step '
                             'must not be None')

        freq = self.setup.frequency.value
        units = self.setup.frequency.units

        start = freq - freq * fraction_below
        stop = freq + freq * fraction_above
        step = freq * fraction_step
        self.start = Frequency(start, units)
        self.stop = Frequency(stop, units)
        self.step = Frequency(step, units)


class HFSSChanger(object):
    """This class provides a way to modify HFSS projects based on solution frequency.

    You can access setups and variables defined in the template project.

    Examples:
      If you have a project named "TemplateProject.aedt", with a setup with
      2 sweeps you need to change, and a couple variables you want to change.
      You can accomplish that like this:

      >>> # Say you want a new project with setup frequencies at 900 MHZ:
      >>> new_project = HFSSChanger('TemplateProject.aedt', 'NewFile.aedt', 900, 'MHz')
      >>> # same as new_project = HFSSChanger('TemplateProject.aedt', 'NewFile.aedt', 900E6)
      >>> # Change sweeps!
      >>> # Setup8's sweep 1 to -25%, +15%, and step by 3% increments
      >>> new_project.Setup8.Sweep1.change_by_fraction(0.25, 0.15, 0.03)
      >>> # Setup8's sweep 2 to +- 5%, by 1% steps.
      >>> new_project.Setup8.Sweep2.change_by_fraction(0.05, 0.05, 0.01)
      >>> # Change some design variable (example: Lair) to 2/5 of a wavelength
      >>> new_project.Lair = new_project.wavelength * 2 / 5
      >>> # Actually make the changes:
      >>> new_project.make_changes()

    """
    def __init__(self, template, new, frequency, frequency_units='Hz'):
        """
        Args:
            template (str): The template HFSS file.  It must exist.
            new (str): The name of the new HFSS file.  It must be a different
              file from `template`.  This file will be created whenever `run`
              is called.
            frequency (float | str): The new file's solution frequency.  If
              `frequency` is a str, it will be parsed to determine the units.
              If `frequency` is a number, and `frequency_units` is not given,
              it is assumed that frequency is given in Hz.
            frequency_units (str): The units associated with frequency.
              If `frequency_units` is not given, it will be parsed from
              `frequency`, and if it is not given in `frequency`, "Hz" will
              be aassumed.

        """
        # Gotta set `self.setups` in a terrible way, because trying to set
        # it the normal way causes an infinite loop, since `self.setups` is
        # referenced in both __getattr__ and __setattr__.
        object.__setattr__(self, 'setups', collections.OrderedDict())
        # Initialize _all_variables similarly since it also is in __setattr__.
        object.__setattr__(self, '_all_variables', [])

        # input validation:
        # * template must exist
        # * template and new must not be the same file
        # * frequency and frequency_units must be something that _Frequency can understand.
        if not os.path.exists(template) or not os.path.isfile(template):
            raise ValueError("The file {} does not exist".format(template))
        if template == new:
            raise ValueError("template and new must be different files.")

        self.frequency = Frequency(frequency, frequency_units)

        self.template = template
        self.new = new
        self._file_data = parse_hfss_file(template)
        project = self._file_data.AnsoftProject
        self._hfss_model = project.HFSSModel
        self.design_name = self._hfss_model.Name
        self.__add_setups()
        self.variables_to_change = collections.OrderedDict()
        self._all_variables = self._hfss_model.ModelSetup.Properties
        self._script_parts = []
        self.wavelength = c / (self.frequency.value * CONVERSIONS[self.frequency.units])

    def __add_setups(self):
        """Find setups in HFSS file"""
        analysis = self._hfss_model.AnalysisSetup
        solve_setups = analysis.SolveSetups
        for setup_name, setup in self.__valid_setups(solve_setups):
            sweeps = setup.Sweeps
            frequency = '{0}{1}'.format(self.frequency.value, self.frequency.units)
            new_setup = Setup(setup.name, frequency)
            self.setups[setup_name] = new_setup
            for sweep_name, sweep in self.__valid_sweeps(sweeps):
                start = sweep.RangeStart
                stop = sweep.RangeEnd
                step = sweep.RangeStep
                new_setup.add_sweep(Sweep(new_setup, sweep_name, start, stop, step))

    def __valid_setups(self, solve_setups):
        """Yield the valid setups from the SolveSetups :class:`HFSSNode`."""
        for setup_name, setup in solve_setups.items():
            if isinstance(setup, HFSSNode) and 'Sweeps' in setup:
                yield setup_name, setup

    def __valid_sweeps(self, sweeps):
        for sweep_name, sweep in sweeps.items():
            if isinstance(sweep, HFSSNode) and \
                    'RangeStart' in sweep and \
                    'RangeEnd' in sweep and \
                    'RangeStep' in sweep:
                yield sweep_name, sweep

    def __getattr__(self, name):
        for place_to_look in self.setups, self.variables_to_change, self._all_variables:
            if name in place_to_look:
                return place_to_look[name]
        else:
            raise AttributeError("{} has no attribute or setup named {}".format(self.template, name))

    def __setattr__(self, name, value):
        """Make it convenient to change HFSS variables, and not override setups."""
        if name in self.setups:
            raise AttributeError('Cannot override setup "{}"'.format(name))
        elif name in self._all_variables:
            self.variables_to_change[name] = value
        else:
            super(HFSSChanger, self).__setattr__(name, value)

    def get_script(self):
        """Get the script (as a string) that will be sent to HFSS."""

        script_writer = ScriptWriter(self)
        return str(script_writer)

    def make_changes(self, keep_open=False):
        """Run HFSS.

        Args:
            keep_hfss_open (bool): if True, keep HFSS open after running.
        """
        prefix = Path(self.new).stem + '_'
        exe = get_hfss()
        shutil.copy(self.template, self.new)
        with tempfile.NamedTemporaryFile('w+', prefix=prefix, suffix='.py', delete=False) as f:
            script = self.get_script()
            f.write(script)
            f.close()
            script_name = f.name

            if keep_open:
                runscript = '-RunScript'
            else:
                runscript = '-RunScriptAndExit'
            cmd = [exe, runscript, script_name]

            logger.info('running command from list %s', cmd)
            try:
                p = subprocess.Popen(cmd)
                p.wait()
            except WindowsError:
                raise
            finally:
                os.remove(script_name)


class HFSSNode(object):
    """This class is useful for reading the HFSS materials file."""
    # A line of the form `simple('permittivity', 3.4)`
    simple = re.compile(r"simple\('(\w+)', ?([0-9eE\.\+\-]+)\)")
    # A line of the form `ModTime=1132068241`
    modtime = re.compile(r"(ModTime)=(\d+)")
    # A line of the form `thermal_conductivity='0.4'`
    keyval = re.compile(r"'?([\w\s]+)'?='?([^']+)'?")
    # design property variables
    variable_prop = re.compile(r"VariableProp\('([^']+)', '.*?', '.*?', '([^']+)'")

    _value_regexes = [simple, modtime, keyval, variable_prop]

    del simple, modtime, keyval, variable_prop

    _ignore_regexes = [
        # Parenthesized expressions
        re.compile(r'(\'?[\w_\d\s]+\'?)\(.*\)'),
        # Don't know what to do with the bracketed things
        re.compile(r"''()"),
        re.compile(r'global:[xyz][xyz]'),
        re.compile(r'relativecs\d:'),
        re.compile(r'Sim\. Setups'),
        re.compile(r'\'Mesh line color\''),
        re.compile(r'SweptValues'),
        # Don't know what to do with anything having a bracket
        re.compile(r'\['),

    ]

    def __init__(self, name, value, parent=None):
        """
        Args:
            name (str): name of the node
            value (str): value to assign the node
            parent (Node): parent of this node.

        """
        self.name = name
        self.value = value or collections.OrderedDict()
        self.parent = parent
        self.children = []
        if self.parent:
            self.parent.add_child(self)

    def add_child(self, node):
        self.children.append(node)

    @classmethod
    def _from_file(cls, line, f, parent=None):
        assert line.startswith('$begin')
        # matches the word begin, a space, optionally a single quote, up to
        # the next single quote.
        name = re.search(r"begin '?([^']*)'?", line)
        name = name.group(1)
        value = collections.OrderedDict()
        self = cls(name, value, parent)
        if parent is not None:
            parent.value[name] = self
        for line in f:
            line = line.strip()
            if line.startswith('$begin'):
                cls._from_file(line, f, self)
            elif line.startswith('$end'):
                return self
            else:
                found = False
                for regex in self._value_regexes:
                    match = regex.search(line)
                    if match:
                        name, value = match.groups()
                        # If value can be a number, it should be stored as one.
                        try:
                            value = float(value)
                        except ValueError:
                            # if it can't be stored as a number, just store the string.
                            pass
                        self.value[name] = value
                        found = True
                        break

                if found:
                    continue

                for regex in self._ignore_regexes:
                    if regex.search(line):
                        break

                else:
                    if name == "Thumbnail64" or name == 'Image64':
                        continue
                    print(name)
                    print(line)
                    raise ValueError('No match for "{}"'.format(line))

    def child(self, name):
        """Select a child by name"""
        return self.value[name]

    @classmethod
    def from_file(cls, f, parent=None):
        """Construct an HFSSNode from an hfss file."""
        return cls._from_file(next(f).strip(), f, parent)

    def __repr__(self):
        return 'HFSSNode: {}'.format(self.name)

    def __getitem__(self, item):
        return self.value[item]

    def __iter__(self):
        return iter(self.value)

    def items(self):
        return self.value.items()

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError('The node "{}" does not have the attribute "{}"'.format(self, item))


class Frequency(object):
    """A class for better working with frequencies.

    """
    def __init__(self, value, units='Hz'):
        """

        Args:
            value (str | float | Frequency)
        """
        if isinstance(value, str):
            value, units = self._parse_str(value)
        elif isinstance(value, Frequency):
            value, units = value.value, value.units
        self.value = value
        self.units = units

    def _parse_str(self, frequency):
        """Allow frequency to be a string (including units) or just a float."""
        # search for a floating point number, optional whitespace,
        # and units in Hz.
        regex_float = r'([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)'
        regex_hz = r'(.?Hz)'
        # first try to match a number _and_ units.  If that fails, try to
        # just match a number, and assume Hz.
        both = re.search(regex_float + r'\s*' + regex_hz, frequency)
        if both:
            freq_str, units = both.groups()
            freq = float(freq_str)
        else:
            freq = float(frequency)
            units = 'Hz'

        return freq, units

    def __str__(self):
        return '{}{}'.format(self.value, self.units)

    def __repr__(self):
        return '_Frequency("{}{}")'.format(self.value, self.units)

    def __eq__(self, other):
        if not isinstance(other, Frequency):
            return NotImplemented
        return CONVERSIONS[self.units] * self.value == CONVERSIONS[other.units] * other.value


def _subkeys(key):
    """
    Yield registry subkeys of specified key.

    :param key: A handle on a registry key (using winreg.OpenKey())
    :return collections.Iterable[str]: Yields subkeys of a key.

    """
    index = 0
    while True:
        try:
            yield winreg.EnumKey(key, index)
        except WindowsError:
            return
        index += 1


def parse_hfss_file(fname):
    """Parses the open HFSS materials file and returns a dict of materials"""

    with open(fname) as f:
        root = HFSSNode(Path(fname).stem, None)
        while True:
            try:
                HFSSNode.from_file(f, root)
            except StopIteration:
                break
    return root


def _get_latest_release(releases):
    """Given a list of the releases of hfss, return the latest."""
    # TODO: This is probably a pretty silly implementation
    return releases[-1]


def _get_installation_dir(desktop_key):
    """
    Get the installation directory of hfss.  desktop_key is the key found in
    the registry at, e.g.,
    "HKLM\Software\Ansoft\ElectronicsDesktop\2015.0\Desktop".

    Args:
        desktop_key: A handle to a Windows registry key

    Returns:
        str: The installation directory of hfss.
    """
    index = 0
    while True:
        try:
            name, value, _ = winreg.EnumValue(desktop_key, index)
            if name == 'InstallationDirectory':
                return value
        except WindowsError:
            raise
        index += 1


def get_hfss():
    """
    Finds hfss executable by querying the registry.
    Returns:
        str: path to the hfss executable

    """
    mode = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, HFSS_2015_BASE, 0, mode)
        exe = HFSS_2015_EXE
    except WindowsError:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, HFSS_2014_BASE, 0, mode)
        exe = HFSS_2014_EXE
    releases = list(_subkeys(key))
    latest = _get_latest_release(releases)
    release = winreg.OpenKey(key, latest)
    desktop_key = winreg.OpenKey(release, 'Desktop')
    installation_directory = _get_installation_dir(desktop_key)
    return str(Path(installation_directory) / exe)


def has_hfss():
    """Return True if the user has HFSS installed (and Python can find it) else False."""
    try:
        exe = get_hfss()
        if exe:
            return True
    except WindowsError:
        pass
    return False


def _get_unique_name(destination):
    """
    Return a path that does not exist, but has a name similar to `destination`.

    e.g., if destination == '/path/to/file.txt',  this will return
    '/path/to/file001.txt' if it doesn't exist, and keep increasing the
    number at the end of the path until it gets a file name that doesn't exist.

    Args:
        destination (pathlib.Path): A path to a file you would like to save.

    Returns:
        pathlib.Path: A saveable file.

    """
    new_destination = destination
    base = str(destination.parent / destination.stem)
    number = 1
    ext = destination.suffix
    while new_destination.exists():
        fname_template = '{base}{number:0>3d}{ext}'
        fname = fname_template.format(base=base, number=number, ext=ext)
        new_destination = Path(fname)
        number += 1

    return new_destination


if has_hfss():
    if get_hfss().endswith(HFSS_2015_EXE):
        EXE_NAME = HFSS_2015_EXE
    else:
        EXE_NAME = HFSS_2014_EXE

