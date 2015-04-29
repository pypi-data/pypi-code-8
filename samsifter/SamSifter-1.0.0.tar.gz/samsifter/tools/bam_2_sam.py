# -*- coding: utf-8 -*-
"""Wrapper for SAMtools view functionality converting BAM to SAM files.

.. moduleauthor:: Florian Aldehoff <samsifter@biohazardous.de>
"""

# custom libraries
from samsifter.models.filter import FilterItem
from samsifter.models.parameter import FilterParameter

# global variables
TEXT = "[SAMtools] Convert BAM to SAM format"
DESC = ("Converts the binary BAM format to the text-based SAM format.")


def item():
    """Create item representing this tool in list and tree views.

    Returns
    -------
    FilterItem
        Item for use in item-based list and tree views.
    """
    filter_item = FilterItem(text=TEXT, desc=DESC,
                             icon=FilterItem.ICON_CONVERTER)
    filter_item.set_command('samtools view -')

    filter_item.add_parameter(FilterParameter(
        text="print header",
        desc="include header in output",
        cli_name='-h',
        default=True,
        active=True
    ))

    # input/output is not default (SAM sorted by queryname)
    filter_item.set_input_format('BAM')
    filter_item.set_input_sorting('any')
    filter_item.set_output_format('SAM')
    filter_item.set_output_sorting('as_input')

    return filter_item
