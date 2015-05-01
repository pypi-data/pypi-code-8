import os
import getpass
from ConfigParser import (SafeConfigParser, _Chainmap, _default_dict,
                          DEFAULTSECT, NoSectionError, NoOptionError)
from path import path


DEFAULTS = {
    "cluspro": {
        # Change these if the location/hostkey of the cluspro server changes
        "hostname": "japetus.bu.edu",
        "hostkey": "AAAAB3NzaC1yc2EAAAABIwAAAIEAniNBIR5dM+fG8L8H84JqYKEPHbRNgx/2oT6Hga/hmhI9KyYiw55mxqUrSjjmYZZJw/rO4fYcrx+lHgemcpU0t5wCbiUeZpRJjnp4jfYiXwF7wNuJQtRbMHu+HDpdfCQCyrj+1SGdGSr0qV3SrjXimN4K9NAaLUiG5bQyjgoq0Xk=",
        "port": "22",
        "username": getpass.getuser()
    },
    "scc": {
        "hostname": "scc1.bu.edu",
        "username": getpass.getuser()
    }
}


class SectionDefaultsConfigParser(SafeConfigParser):
    """
    Allow user to specify section specific defaults.
    """
    def __init__(self, section_defaults, dict_type=_default_dict,
                 allow_no_value=False):
        SafeConfigParser.__init__(self, dict_type=dict_type,
                                  allow_no_value=allow_no_value)
        self._section_defaults = section_defaults
        for section in section_defaults:
            self.add_section(section)

    def get(self, section, option, raw=False, vars=None):
        section_defaults = {}
        if section in self._section_defaults:
            section_defaults = self._section_defaults[section]
        sectiondict = {}
        try:
            sectiondict = self._sections[section]
        except KeyError:
            if section != DEFAULTSECT and section not in self._section_defaults:
                raise NoSectionError(section)
        vardict = {}
        if vars:
            for key, value in vars.items():
                vardict[self.optionxform(key)] = value
        d = _Chainmap(vardict, sectiondict, section_defaults)
        option = self.optionxform(option)
        try:
            value = d[option]
        except KeyError:
            raise NoOptionError(option, section)

        if raw or value is None:
            return value
        else:
            return self._interpolate(section, option, value, d)

    def items(self, section, raw=False, vars=None):
        d = {}
        if section in self._section_defaults:
            d.update(self._section_defaults[section])
        try:
            d.update(self._sections[section])
        except KeyError:
            if section != DEFAULTSECT and section not in self._section_defaults:
                raise NoSectionError(section)

        if vars:
            for key, value in vars.items():
                d[self.optionxform(key)] = value
        options = d.keys()
        if "__name__" in options:
            options.remove("__name__")

        if raw:
            return [(option, d[option])
                    for option in options]
        else:
            return [(option, self._interpolate(section, option, d[option], d))
                    for option in options]


def get_config():
    config = SectionDefaultsConfigParser(DEFAULTS)

    config_file = path("~/.sblurc").expand()
    if config_file.exists():
        config.read(config_file)

    return config


CONFIG = get_config()
