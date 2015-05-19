# Copyright 2015 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of cifparser.  cifparser is BSD-licensed software;
# for copyright information see the LICENSE file.

from cifparser.converters import *

def or_default(default, fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except KeyError:
        return default

class Namespace(object):
    """
    """
    def __init__(self, values):
        """
        :param values:
        :type values: cifparser.valuetree.ValueTree
        """
        self.values = values

    def get_container(self, path):
        return self.values.get_container(path)

    def get_container_or_default(self, path, default=None):
        return or_default(default, self.get_container, path)

    def contains_container(self, path):
        """
        """
        return self.values.contains_container(path)

    def get_raw(self, path, name):
        return self.values.get_field(path, name)

    def get_raw_or_default(self, path, name, default=None):
        return or_default(default, self.get_raw, path, name)

    def get_raw_list(self, path, name):
        return self.values.get_field_list(path, name)

    def get_raw_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_raw_list, path, name)

    def get_str(self, path, name):
        return str_to_stripped(self.get_raw(path, name))

    def get_str_or_default(self, path, name, default=None):
        return or_default(default, self.get_str, path, name)

    def get_str_list(self, path, name):
        return map(lambda x: str_to_stripped(x), self.values.get_field_list(path, name))

    def get_str_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_str_list, path, name)

    def get_flattened(self, path, name):
        return str_to_flattened(self.get_raw(path, name))

    def get_flattened_or_default(self, path, name, default=None):
        return or_default(default, self.get_str, path, name)

    def get_flattened_list(self, path, name):
        return map(lambda x: str_to_flattened(x), self.values.get_field_list(path, name))

    def get_flattened_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_flattened_list, path, name)

    def get_int(self, path, name):
        return str_to_int(self.get_flattened(path, name))

    def get_int_or_default(self, path, name, default=None):
        return or_default(default, self.get_int, path, name)

    def get_int_list(self, path, name):
        return map(lambda x: str_to_int(x), self.get_flattened_list(path, name))

    def get_int_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_int_list, path, name)

    def get_bool(self, path, name):
        return str_to_bool(self.get_flattened(path, name))

    def get_bool_or_default(self, path, name, default=None):
        return or_default(default, self.get_bool, path, name)

    def get_bool_list(self, path, name):
        return map(lambda x: str_to_bool(x), self.get_flattened_list(path, name))

    def get_bool_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_bool_list, path, name)

    def get_float(self, path, name):
        return str_to_float(self.get_flattened(path, name))

    def get_float_or_default(self, path, name, default=None):
        return or_default(default, self.get_float, path, name)

    def get_float_list(self, path, name):
        return map(lambda x: str_to_float(x), self.get_flattened_list(path, name))

    def get_float_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_float_list, path, name)

    def get_timedelta(self, path, name):
        return str_to_timedelta(self.get_flattened(path, name))

    def get_timedelta_or_default(self, path, name, default=None):
        return or_default(default, self.get_timedelta, path, name)

    def get_timedelta_list(self, path, name):
        return map(lambda x: str_to_timedelta(x), self.get_flattened_list(path, name))

    def get_timedelta_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_timedelta_list, path, name)

    def get_size(self, path, name):
        return str_to_size(self.get_flattened(path, name))

    def get_size_or_default(self, path, name, default=None):
        return or_default(default, self.get_size, path, name)

    def get_size_list(self, path, name):
        return map(lambda x: str_to_size(x), self.get_flattened_list(path, name))

    def get_size_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_size_list, path, name)

    def get_percentage(self, path, name):
        return str_to_percentage(self.get_flattened(path, name))

    def get_percentage_or_default(self, path, name, default=None):
        return or_default(default, self.get_percentage, path, name)

    def get_percentage_list(self, path, name):
        return map(lambda x: str_to_percentage(x), self.get_flattened_list(path, name))

    def get_percentage_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_percentage_list, path, name)

    def get_throughput(self, path, name):
        return str_to_throughput(self.get_flattened(path, name))

    def get_throughput_or_default(self, path, name, default=None):
        return or_default(default, self.get_throughput, path, name)

    def get_throughput_list(self, path, name):
        return map(lambda x: str_to_throughput(x), self.get_flattened_list(path, name))

    def get_throughput_list_or_default(self, path, name, default=None):
        return or_default(default, self.get_throughput_list, path, name)

    def contains_field(self, path, name):
        """
        Returns True if the specified name exists, otherwise False.

        :param name: The name.
        :type name: str
        :returns: True or False.
        :rtype: [bool]
        """
        return self.values.contains_field(path, name)

    def contains_field_list(self, path, name):
        """
        Returns True if the specified name exists, otherwise False.

        :param name: The name.
        :type name: str
        :returns: True or False.
        :rtype: [bool]
        """
        return self.values.contains_field_list(path, name)

    def contains(self, path, name):
        return self.contains_field(path, name) or self.contains_field_list(path, name)
