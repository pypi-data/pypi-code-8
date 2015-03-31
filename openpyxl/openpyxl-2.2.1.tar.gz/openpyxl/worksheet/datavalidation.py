from __future__ import absolute_import
# Copyright (c) 2010-2015 openpyxl

from itertools import groupby, chain
import warnings

from openpyxl.descriptors import Strict, Bool, NoneSet, Set, String
from openpyxl.compat import OrderedDict, safe_string, deprecated
from openpyxl.cell import coordinate_from_string
from openpyxl.worksheet import cells_from_range
from openpyxl.xml.constants import SHEET_MAIN_NS
from openpyxl.xml.functions import Element, safe_iterator


def collapse_cell_addresses(cells, input_ranges=()):
    """ Collapse a collection of cell co-ordinates down into an optimal
        range or collection of ranges.

        E.g. Cells A1, A2, A3, B1, B2 and B3 should have the data-validation
        object applied, attempt to collapse down to a single range, A1:B3.

        Currently only collapsing contiguous vertical ranges (i.e. above
        example results in A1:A3 B1:B3).  More work to come.
    """
    keyfunc = lambda x: x[0]

    # Get the raw coordinates for each cell given
    raw_coords = [coordinate_from_string(cell) for cell in cells]

    # Group up as {column: [list of rows]}
    grouped_coords = OrderedDict((k, [c[1] for c in g]) for k, g in
                          groupby(sorted(raw_coords, key=keyfunc), keyfunc))
    ranges = list(input_ranges)

    # For each column, find contiguous ranges of rows
    for column in grouped_coords:
        rows = sorted(grouped_coords[column])
        grouped_rows = [[r[1] for r in list(g)] for k, g in
                        groupby(enumerate(rows),
                        lambda x: x[0] - x[1])]
        for rows in grouped_rows:
            if len(rows) == 0:
                pass
            elif len(rows) == 1:
                ranges.append("%s%d" % (column, rows[0]))
            else:
                ranges.append("%s%d:%s%d" % (column, rows[0], column, rows[-1]))

    return " ".join(ranges)


def expand_cell_ranges(range_string):
    """
    Expand cell ranges to a sequence of addresses.
    Reverse of collapse_cell_addresses
    Eg. converts "A1:A2 B1:B2" to (A1, A2, B1, B2)
    """
    cells = []
    for rs in range_string.split():
        cells.extend(cells_from_range(rs))
    return list(chain.from_iterable(cells))


class DataValidation(Strict):

    showErrorMessage = Bool()
    showDropDown = Bool(allow_none=True)
    showInputMessage = Bool()
    showErrorMessage = Bool()
    allowBlank = Bool()
    allow_blank = Bool()

    errorTitle = String(allow_none = True)
    error = String(allow_none = True)
    promptTitle = String(allow_none = True)
    prompt = String(allow_none = True)
    sqref = String(allow_none = True)
    formula1 = String(allow_none = True)
    formula2 = String(allow_none = True)

    type = NoneSet(values=("whole", "decimal", "list", "date", "time",
                           "textLength", "custom"))
    errorStyle = NoneSet(values=("stop", "warning", "information"))
    imeMode = NoneSet(values=("noControl", "off", "on", "disabled",
                              "hiragana", "fullKatakana", "halfKatakana", "fullAlpha","halfAlpha",
                              "fullHangul", "halfHangul"))
    operator = NoneSet(values=("between", "notBetween", "equal", "notEqual",
                               "lessThan", "lessThanOrEqual", "greaterThan", "greaterThanOrEqual"))

    def __init__(self,
                 type=None,
                 formula1=None,
                 formula2=None,
                 allow_blank=False,
                 showErrorMessage=True,
                 showInputMessage=True,
                 showDropDown=None,
                 allowBlank=None,
                 sqref=None,
                 promptTitle=None,
                 errorStyle=None,
                 error=None,
                 prompt=None,
                 errorTitle=None,
                 imeMode=None,
                 operator=None,
                 validation_type=None, # remove in future
                 ):

        self.showDropDown = showDropDown
        self.imeMode = imeMode
        self.operator = operator
        self.formula1 = formula1
        self.formula2 = formula2
        self.allowBlank = allow_blank
        if allowBlank is not None:
            self.allowBlank = allowBlank
        self.showErrorMessage = showErrorMessage
        self.showInputMessage = showInputMessage
        if validation_type is not None:
            warnings.warn("Use 'DataValidation(type={0})'".format(validation_type))
            if type is not None:
                self.type = validation_type
        self.type = type
        self.cells = set()
        self.ranges = []
        if sqref is not None:
            self.sqref = sqref
        self.promptTitle = promptTitle
        self.errorStyle = errorStyle
        self.error = error
        self.prompt = prompt
        self.errorTitle = errorTitle

    @deprecated("Use DataValidation.add()")
    def add_cell(self, cell):
        """Adds a openpyxl.cell to this validator"""
        self.add(cell)

    def add(self, cell):
        """Adds a openpyxl.cell to this validator"""
        self.cells.add(cell.coordinate)

    @deprecated("Set DataValidation.ErrorTitle and DataValidation.error")
    def set_error_message(self, error, error_title="Validation Error"):
        """Creates a custom error message, displayed when a user changes a cell
           to an invalid value"""
        self.errorTitle = error_title
        self.error = error

    @deprecated("Set DataValidation.PromptTitle and DataValidation.prompt")
    def set_prompt_message(self, prompt, prompt_title="Validation Prompt"):
        """Creates a custom prompt message"""
        self.promptTitle = prompt_title
        self.prompt = prompt

    @property
    def sqref(self):
        return collapse_cell_addresses(self.cells, self.ranges)

    @sqref.setter
    def sqref(self, range_string):
        self.cells = expand_cell_ranges(range_string)

    def __iter__(self):
        for attr in ('type', 'allowBlank', 'operator', 'sqref',
                     'showInputMessage', 'showErrorMessage', 'errorTitle', 'error',
                     'errorStyle',
                     'promptTitle', 'prompt'):
            value = getattr(self, attr)
            if value is not None:
                yield attr, safe_string(value)


@deprecated("Class descriptors check values")
class ValidationType(object):
    NONE = "none"
    WHOLE = "whole"
    DECIMAL = "decimal"
    LIST = "list"
    DATE = "date"
    TIME = "time"
    TEXT_LENGTH = "textLength"
    CUSTOM = "custom"


@deprecated("Class descriptors check values")
class ValidationOperator(object):
    BETWEEN = "between"
    NOT_BETWEEN = "notBetween"
    EQUAL = "equal"
    NOT_EQUAL = "notEqual"
    LESS_THAN = "lessThan"
    LESS_THAN_OR_EQUAL = "lessThanOrEqual"
    GREATER_THAN = "greaterThan"
    GREATER_THAN_OR_EQUAL = "greaterThanOrEqual"


@deprecated("Class descriptors check values")
class ValidationErrorStyle(object):
    STOP = "stop"
    WARNING = "warning"
    INFORMATION = "information"


def writer(data_validation):
    """
    Serialse a data validation
    """
    attrs = dict(data_validation)
    el = Element("{%s}dataValidation" % SHEET_MAIN_NS, attrs)
    for attr in ("formula1", "formula2"):
        value = getattr(data_validation, attr, None)
        if value is not None:
            f = Element("{%s}%s" % (SHEET_MAIN_NS, attr))
            f.text = value
            el.append(f)
    return el


def parser(element):
    """
    Parse dataValidation tag
    """
    dv = DataValidation(**element.attrib)
    for attr in ("formula1", "formula2"):
        for f in safe_iterator(element, "{%s}%s" % (SHEET_MAIN_NS, attr)):
            setattr(dv, attr, f.text)
    return dv
