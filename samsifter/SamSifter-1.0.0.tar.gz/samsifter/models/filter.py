# -*- coding: utf-8 -*-
"""
Abstraction of filters and other tools usable in POSIX pipelines.

.. moduleauthor:: Florian Aldehoff <samsifter@biohazardous.de>
"""

# Qt4 libraries
from PyQt4.QtGui import QStandardItem, QIcon

# custom libraries
from samsifter.gui.widgets import FilterWidget
from samsifter.resources import resources
assert resources  # silence pyflakes

SUPPORTED_FORMATS = ('SAM', 'BAM', 'any', 'as_input')
SUPPORTED_SORTINGS = ('unsorted', 'queryname', 'coordinate', 'any', 'as_input')
SUPPORTED_COMPRESSIONS = ('uncompressed', 'gzip', 'any', 'as_input')


class FilterItem(QStandardItem):
    """Representation of filter tool in item-based views.

    This class can abstract any tool that takes line-based input from STDIN,
    logs messages to STDERR and writes output to STDOUT. It is used to
    represent this tool in item-based views by means of an icon and
    descriptive text.

    Each item has a list of parameters as well as input and output requirements
    in terms file format, sort order and compression.
    """
    # icon paths correspond to resource entries
    ICON_ANALYZER = ":/x-office-spreadsheet.png"
    ICON_CONVERTER = ":/applications-other.png"
    ICON_FILTER = ":/view-filter.png"
    ICON_SORTER = ":/view-sort-ascending.png"

    def __init__(self, text=None, desc=None, icon=ICON_FILTER):
        """Initialize new instance of a FilterItem.

        By default the new filter item both accepts and outputs only
        uncompressed SAM files ordered by queryname.

        Parameters
        ----------
        text : str
            Short label for tool, should not exceed one line.
        desc : str
            Longer description of tool, should explain basic functionality.
        icon : str
            Path to icon resource, defaults to filter icon.
        """
        if icon is None:
            super(FilterItem, self).__init__(text)
        else:
            super(FilterItem, self).__init__(QIcon(icon), text)
        self.desc = desc
        self.icon_path = icon
        self.command = "tester"
        self.input_format = 'SAM'
        self.input_sorting = 'queryname'
        self.input_compression = 'uncompressed'
        self.output_format = 'SAM'
        self.output_sorting = 'queryname'
        self.output_compression = 'uncompressed'
        self.parameters = []
        self.valid = True
        self.setEditable(False)

    def clone(self):
        """Creates new instance with identical settings.

        Returns
        -------
        FilterItem
            Exact clone of this filter item.
        """
        clone = FilterItem(self.text(), self.desc, self.icon_path)
        clone.set_command(self.command)
        clone.set_input_format(self.input_format)
        clone.set_input_sorting(self.input_sorting)
        clone.set_input_compression(self.input_compression)
        clone.set_output_format(self.output_format)
        clone.set_output_sorting(self.output_sorting)
        clone.set_output_compression(self.output_compression)
        for param in self.parameters:
            clone.add_parameter(param.clone())
        return clone

    def commandline(self, basenames=False):
        """Prints full bash command line for filter with all parameters.

        Parameters
        ----------
        basenames : bool
            Shorten file paths to filename only, defaults to False.

        Returns
        -------
        str
            Command to execute filter with all parameters.
        """
        cline = self.command
        for param in self.parameters:
            if param.is_active() or param.is_required():
                cline += " " + param.cli(basenames)
        return cline

    def make_widget(self):
        """Creates a FilterWidget visualizing all parameters of this filter.

        Returns
        -------
        FilterWidget
            Qt4 widget visualizing all parameters of this filter.
        """
        return FilterWidget(self)

    def __str__(self):
        return self.text()

    def __repr__(self):
        rep = "\n%s" % self.text()
        rep += "\n- command:\t\t%s" % self.command
        rep += "\n- description:\t%s" % self.desc
        for param in self.parameters:
            rep += repr(param)
        return rep

    # Getters & Setters

    def add_parameter(self, parameter):
        """Append parameter to list of parameters.

        Parameters
        ----------
        parameter : FilterParameter
            Parameter to be added to this filter.
        """
        self.parameters.append(parameter)

    def get_parameters(self):
        return self.parameters

    def set_command(self, command):
        """Set command executed by filter.

        Parameters
        ----------
        command : str
            Command of tool in PATH, absolute path to binary or Python entry
            point to main method.
        """
        self.command = command

    def get_description(self):
        return self.desc

    def set_description(self, desc):
        """Set description of filter shown in GUI.

        Parameters
        ----------
        description : str
            Longer description of tool, should explain basic functionality.
        """
        self.desc = desc

    def get_icon_path(self):
        return self.icon_path

    def set_icon_path(self, icon_path):
        """Set resource path to icon representing the filter.

        Parameters
        ----------
        icon_path : str
            Path to icon in resource file. Use any of the FilterItem constants
            ICON_FILTER, ICON_ANALYZER, ICON_CONVERTER or ICON_SORTER.
        """
        self.icon_path = icon_path

    def set_input_format(self, fileformat):
        """Set the expected input format.

        Parameters
        ----------
        fileformat : str
            Expected file format. Use any of the formats supported by
            FilterItem ('SAM', 'BAM', 'any').
        """
        if fileformat in SUPPORTED_FORMATS:
            self.input_format = fileformat

    def get_input_format(self):
        return self.input_format

    def set_output_format(self, fileformat):
        """Set the provided output format.

        Parameters
        ----------
        fileformat : str
            Provided file format. Use any of the formats supported by
            FilterItem ('SAM', 'BAM', 'as_input').
        """
        if fileformat in SUPPORTED_FORMATS:
            self.output_format = fileformat

    def get_output_format(self):
        return self.output_format

    def set_input_sorting(self, sorting):
        """Set the expected input sort order.

        Parameters
        ----------
        sorting : str
            Expected read sort order. Use any of the sort orders supported by
            FilterItem ('unsorted', 'queryname', 'coordinate', 'any').
        """
        if sorting in SUPPORTED_SORTINGS:
            self.input_sorting = sorting

    def get_input_sorting(self):
        return self.input_sorting

    def set_output_sorting(self, sorting):
        """Set the provided output sort order.

        Parameters
        ----------
        sorting : str
            Provided read sort order. Use any of the sort orders supported by
            FilterItem ('unsorted', 'queryname', 'coordinate', 'as_input').
        """
        if sorting in SUPPORTED_SORTINGS:
            self.output_sorting = sorting

    def get_output_sorting(self):
        return self.output_sorting

    def set_input_compression(self, compression):
        """Set the expected input compression.

        Parameters
        ----------
        compression : str
            Expected input compression. Use any of the compressions supported
            by FilterItem ('uncompressed', 'gzip', 'any').
        """
        if compression in SUPPORTED_COMPRESSIONS:
            self.input_compression = compression

    def get_input_compression(self):
        return self.input_compression

    def set_output_compression(self, compression):
        """Set the provided output compression.

        Parameters
        ----------
        compression : str
            Provided output compression. Use any of the compressions supported
            by FilterItem ('uncompressed', 'gzip', 'as_input').
        """
        if compression in SUPPORTED_COMPRESSIONS:
            self.output_compression = compression

    def get_output_compression(self):
        return self.output_compression

    def is_valid(self):
        return self.valid

    def set_valid(self, boolean):
        self.valid = boolean
