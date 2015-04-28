"""
Core components for str2type
"""


import codecs
import json

from .pycompat import string_types


def str2type(string, decode_escape=True):

    """
    Convert a string representation of an int, float, None, True, False, or JSON
    to its native type.  For None, True, and False, case is irrelevant.  The
    primary use-case of this function is automatically parsing user-input from
    the commandline into Python types.  Argument parsers usually handle this no
    problem but if a flag can take multiple types then `str2type()` can serve
    as the decoder.

        >>> from str2type import str2type
        >>> print(str2type("1.23"))
        1.23
        >>> print(str2type("1.")
        1.0
        >>> print(str2type(".2"))
        0.2
        >>> print(str2type("NonE"))
        None
        >>> print(str2type("String"))
        "String"

    Parameters
    ----------
    string : str
        Input string to transform.
    decode_escape : bool, optional
        Use `codecs.decode(string, 'unicode_escape')` to handle escaped strings
        like \n being passed in from the commandline.  Escape characters end up
        doubly escaped, which is especially annoying for newline characters.

    Returns
    -------
    str
        The input string if it could not be converted to another type or is
        actually just a string.
    list
        If input is JSON.
    dict
        If input is JSON.
    int
        "123" -> 123
    float
        "1.23" -> 1.23
    True
        "TrUe" -> True
    False
        "FaLsE" -> False
    None
        "NoNe" -> None
    """

    if not (isinstance(string, string_types) or isinstance(string, bytes)):
        raise TypeError("Input string is a '%s' - must be a str or unicode instance" % type(string))

    if decode_escape:
        string = codecs.decode(string, 'unicode_escape')

    processing_string = string.strip()

    # Integers are really easy to grab and must happen before floats otherwise '1' becomes '1.0'
    if processing_string.isdigit():
        return int(processing_string)
    else:

        # Casting to float can just be blindly tried
        try:
            return float(processing_string)
        except ValueError:

            # True, False, and None are evaluated individually to check for mixed case (TrUe, FALse, etc.)
            string_lower = processing_string.lower()
            if string_lower == 'none':
                return None
            elif string_lower == 'true':
                return True
            elif string_lower == 'false':
                return False
            else:

                # Try to decode a JSON object if everything else failed
                try:
                    return json.loads(processing_string)

                # Input must actually just be a string - return the input object
                except ValueError:
                    return string