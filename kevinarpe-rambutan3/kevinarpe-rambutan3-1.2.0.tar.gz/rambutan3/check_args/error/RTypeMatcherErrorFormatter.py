"""Format exception messages for {@link RAbstractTypeMatcher#check()}

@author Kevin Connor ARPE (kevinarpe@gmail.com)
"""

import inspect


# Trick to satisfy Python compiler about RAbstractTypeMatcher being undefined without an import statement.
from rambutan3.string import RStrUtil

try:
    eval('RAbstractTypeMatcher')
except:
    RAbstractTypeMatcher = None


class RTypeMatcherErrorFormatter:
    """Used by {@link RAbstractTypeMatcher#check()} to format exception messages"""

    def format(self, matcher: RAbstractTypeMatcher, value, *args, **kwargs) -> str:
        """Creates an exception message for a failed value matcher check

        @param matcher (RAbstractTypeMatcher)
               value matcher associated with failed check
        @param value
               value associated with failed check
        @param *args
               unused, but exists for signature override compatibility
        @param **kwargs
               unused, but exists for signature override compatibility

        @return exception message
        """
        if value is None:
            value_desc = "'None'"
        else:
            if inspect.isfunction(value):
                value_str = "def {}{}".format(value.__qualname, inspect.signature(value))
            else:
                value_str = RStrUtil.auto_quote(value)
            value_desc = "value of type '{}': {}".format(type(value).__name__, value_str)

        x = "Expected type '{}', but found {}".format(matcher, value_desc)
        return x
