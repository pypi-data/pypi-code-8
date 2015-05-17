# Copyright 2015 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of cifparser.  cifparser is BSD-licensed software;
# for copyright information see the LICENSE file.

class CifError(Exception):
    "Base exception class for cifparser."
    pass

class ParserError(CifError):
    "Failed to parse the specified CIF file"
    def __init__(self, line, col, context, error):
        self.line = line
        self.col = col
        self.context = context
        self.error = error
    def __str__(self):
        return "line {}, col {}: {}".format(self.line, self.col, self.error)

class ConversionError(CifError):
    "Failed to convert to requested datatype."
    pass
