import re
from rambutan3.string.RPatternText import RPatternText


class RVariableName(RPatternText):
    """
    Wraps a {@link str} value that is a valid C programming language variable:
    (1) Starts with [A-Za-z_]
    (2) Followed by zero or more [0-9A-Za-z_]

    Examples: email_address, telephone_number123, or __something_very_private

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)
    """

    __TOKEN_PATTERN = re.compile(r"^[A-Za-z_][0-9A-Za-z_]*$")

    # noinspection PyMissingConstructor
    def __init__(self, value: str):
        # Insane: We call RPatternText.new() only to validate argument 'value'.
        # We do not save the result, and allow the implicit ctor to be called.
        # Magic!
        RPatternText.new(value, self.__TOKEN_PATTERN)
        # Crazy, crazy, crazy.  Do not call super().__init__()!  No idea how this magic works.
        # super().__init__(value)
        # super().__init__()
