# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import pprint
import ConfigParser

from .utils import cached_property


class Configuration(ConfigParser.ConfigParser):
    DEFAULT_CONFIG_FILES = [
        os.path.join(os.environ['HOME'], '.config', 'chandler.conf'),
        os.path.join('/etc', 'oar', 'chandler.conf'),
        os.path.join(os.path.abspath(os.path.dirname(__file__)),
                     'default_chandler.conf'),
    ]

    def __init__(self):
        if os.environ.get('CHANDLER_CONF_FILE', None):
            env_file = os.environ['CHANDLER_CONF_FILE']
            self.DEFAULT_CONFIG_FILES.insert(0, env_file)
        ConfigParser.ConfigParser.__init__(self, allow_no_value=False)
        for config_file in self.DEFAULT_CONFIG_FILES[:-1]:
            if self.load_file(config_file, silent=True):
                break
        else:
            self.load_file(self.DEFAULT_CONFIG_FILES[-1], silent=False)

    def load_file(self, filename, silent=False):
        """Updates the values in the config from a config file.
        :param filename: the filename of the config.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        """
        try:
            with open(filename) as f:
                self.readfp(f)
        except IOError as e:
            if silent:
                return False
            e.strerror = ('Unable to load configuration file. \n\n'
                          'The configuration file is searched into %s or in '
                          'the location given by the $CHANDLER_CONF_FILE '
                          'environement variable' % self.DEFAULT_CONFIG_FILES)
            raise
        return True

    @cached_property
    def nodename_regex(self):
        return self.get('output', 'nodename_regex')

    @cached_property
    def col_size(self):
        return self.getint('output', 'col_size')

    @cached_property
    def col_span(self):
        return self.getint('output', 'col_span')

    @cached_property
    def max_cols(self):
        return self.getint('output', 'max_cols')

    @cached_property
    def users_stats_by_default(self):
        return self.getboolean('output', 'users_stats_by_default')

    @cached_property
    def nodes_usage_by_default(self):
        return self.getboolean('output', 'nodes_usage_by_default')

    @cached_property
    def nodes_header(self):
        return self.get('output', 'nodes_header')

    @cached_property
    def nodes_format(self):
        return self.get('output', 'nodes_format')

    @cached_property
    def comment_property(self):
        try:
            return self.get('output', 'comment_property')
        except:
            pass

    @cached_property
    def separations(self):
        try:
            return self.get('output', 'separations').split(',')
        except:
            return []

    @cached_property
    def cols(self):
        cols = self.getint('output', 'columns')
        # Compute the number of columns depending on the COLUMNS environment
        # variable
        try:
            rows, columns = os.popen('stty size', 'r').read().split()
            cols = int(int(columns) / self.col_size)
        except:
            pass
        if cols == 0:
            cols = 1
        if cols > self.max_cols:
            cols = self.max_cols
        return cols

    @cached_property
    def ignore_proxy(self):
        return self.getboolean('misc', 'ignore_proxy')

    @cached_property
    def cache(self):
        info = {
            'resources': {},
            'jobs': {},
        }
        info['enabled'] = self.getboolean('oarapi', 'caching')
        if info['enabled']:
            for view in ('resources', 'jobs'):
                cache_file = self.get('oarapi', 'caching_%s_file' % view)
                info[view] = {
                    'file': os.path.expanduser(cache_file),
                    'delay': self.getint('oarapi', 'caching_%s_delay' % view)
                }
        return info

    def __str__(self):
        return pprint.pprint(self._sections)
