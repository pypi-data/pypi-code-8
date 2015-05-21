"""Format exception messages for {@link RAbstractTypeMatcher#check()}

@author Kevin Connor ARPE (kevinarpe@gmail.com)
"""

from rambutan3.check_args.error.RTypeMatcherErrorFormatter import RTypeMatcherErrorFormatter


# Trick to satisfy Python compiler about RAbstractTypeMatcher being undefined without an import statement.
try:
    eval('RAbstractTypeMatcher')
except:
    RAbstractTypeMatcher = None


class RTypeMatcherErrorFormatterWithPrefix(RTypeMatcherErrorFormatter):
    """Used by {@link RAbstractTypeMatcher#check()} to format exception messages"""

    def format(self,
               matcher: RAbstractTypeMatcher,
               value,
               error_prefix_format: str="",
               *error_prefix_format_args,
               **kwargs):
        """Creates an exception message for a failed value matcher check,
        with a prefix formatted via {@link str#format()}

        @param matcher (RAbstractTypeMatcher)
               value matcher associated with failed check
        @param value
               value associated with failed check
        @param error_prefix_format (optional: str)
               format to be passed directly to {@link str#format()}
        @param *error_prefix_format_args
               zero or more format args to be passed directly to {@link str#format()}
        @param **kwargs
               unused, but exists for signature override compatibility

        @return exception message
        """
        x = super().format(matcher, value)
        prefix = error_prefix_format.format(*error_prefix_format_args)
        y = prefix + x
        return y
