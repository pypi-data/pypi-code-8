# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""This module implements a configuration value source comprising a stream of
textual key/value pairs.  The implementation uses a ContextManger to iterate
through the stream.  The ContextManager can represent any number of sources,
like files or database results.  If supplied with a simple string rather than
a ContextManager, the value source will assume it is a file pathname and try
to open it.
"""

import functools
import sys

from configman import namespace
from configman.option import (
    Option,
)
from configman.value_sources.source_exceptions import (
    ValueException,
    CantHandleTypeException
)
from configman.dotdict import DotDict
from configman.memoize import memoize

function_type = type(lambda x: x)  # TODO: just how do you express the Fuction
                                   # type as a constant?
                                   # (peter: why not use inspect.isfunction()?)

# the list of types that the contstuctor can handle.
can_handle = (
    basestring,
    function_type  # this is to say that this ValueSource is willing
                   # to try a function that will return a
                   # context manager
)

file_name_extension = 'conf'


#==============================================================================
class NotAConfigFileError(ValueException):
    pass


#==============================================================================
class ValueSource(object):

    #--------------------------------------------------------------------------
    def __init__(self, candidate, the_config_manager=None):
        if (
            isinstance(candidate, basestring) and
            candidate.endswith(file_name_extension)
        ):
            # we're trusting the string represents a filename
            opener = functools.partial(open, candidate)
        elif isinstance(candidate, function_type):
            # we're trusting that the function when called with no parameters
            # will return a Context Manager Type.
            opener = candidate
        else:
            raise CantHandleTypeException()
        self.values = {}
        try:
            with opener() as f:
                previous_key = None
                for line in f:
                    if line.strip().startswith('#') or not line.strip():
                        continue
                    if line[0] in ' \t' and previous_key:
                        line = line[1:]
                        self.values[previous_key] = (
                            '%s%s' % (self.values[previous_key],line.rstrip())
                        )
                        continue
                    try:
                        key, value = line.split("=", 1)
                        self.values[key.strip()] = value.strip()
                        previous_key = key
                    except ValueError:
                        self.values[line] = ''
        except Exception, x:
            raise NotAConfigFileError(
                "Conf couldn't interpret %s as a config file: %s"
                % (candidate, str(x))
            )

    #--------------------------------------------------------------------------
    @memoize()
    def get_values(self, config_manager, ignore_mismatches, obj_hook=DotDict):
        """the 'config_manager' and 'ignore_mismatches' are dummy values for
        this implementation of a ValueSource."""
        if isinstance(self.values, obj_hook):
            return self.values
        return obj_hook(initializer=self.values)

    #--------------------------------------------------------------------------
    @staticmethod
    def write(source_dict, namespace_name=None, output_stream=sys.stdout):
        options = [
            value
            for value in source_dict.values()
            if isinstance(value, Option)
        ]
        options.sort(cmp=lambda x, y: cmp(x.name, y.name))
        namespaces = [
            (key, value)
            for key, value in source_dict.items()
            if isinstance(value, namespace.Namespace)
        ]
        for an_option in options:
            if namespace_name:
                option_name = "%s.%s" % (namespace_name, an_option.name)
            else:
                option_name = an_option.name
            print >>output_stream, "# name: %s" % option_name
            print >>output_stream, "# doc: %s" % an_option.doc
            option_value = str(an_option)
            if isinstance(option_value, unicode):
                option_value = option_value.encode('utf8')

            if an_option.likely_to_be_changed:
                option_format = '%s=%r\n'
            else:
                option_format = '# %s=%r\n'
            print >>output_stream, option_format % (
              option_name,
              option_value
            )
        for key, a_namespace in namespaces:
            if namespace_name:
                namespace_label = ''.join((namespace_name, '.', key))
            else:
                namespace_label = key
            print >> output_stream, '#%s' % ('-' * 79)
            print >> output_stream, '# %s - %s\n' % (
                namespace_label,
                a_namespace._doc
            )
            ValueSource.write(
              a_namespace,
              namespace_name=namespace_label,
              output_stream=output_stream
            )
