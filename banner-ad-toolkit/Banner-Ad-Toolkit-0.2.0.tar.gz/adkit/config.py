# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Config loader."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import os

# 3rd Party
import six.moves.configparser as configparser

# App
from bashutils import logmsg

# -----------------------------------------------------------------------------


class Config(object):

    """Config loader."""

    def __init__(self):
        self.config = None

    def load(self, config_file="adkit.ini"):
        """Load config."""
        if os.path.exists(config_file):
            try:
                self.config = configparser.SafeConfigParser()
                self.config.read(config_file)
            except (configparser.Error) as err:
                logmsg.log_error("Error parsing config file: " + config_file)
                logmsg.log_error(str(err))
        else:
            logmsg.log_warning("No config file: " + config_file)

    def update_defaults(self, defaults, section):
        """Update defaults."""
        # if the config was not loaded just move on as it may not exist
        if not self.config:
            return defaults

        # get config items from section
        if not self.config.has_section(section):
            return defaults

        config_items = dict(self.config.items(section))

        # overwrite any existing defaults
        defaults.update(config_items)

        # coerce boolan values into their proper form
        defaults = Config.coerce_booleans(defaults)

        return defaults

    @staticmethod
    def coerce_booleans(defaults):
        """
        Ensure config values that should be treated as booleans really
        are valid boolean values.
        """
        # coerce boolean and none types
        for _key in defaults:
            item = defaults[_key]
            if item.lower() == 'true':
                defaults[_key] = True
            elif item.lower() == 'false':
                defaults[_key] = False
            elif item.lower() == 'none':
                defaults[_key] = None

        return defaults
