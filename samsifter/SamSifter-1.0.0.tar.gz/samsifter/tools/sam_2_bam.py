#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrapper for SAMtools view functionality to convert SAM to BAM files.

.. moduleauthor:: Florian Aldehoff <samsifter@biohazardous.de>
"""

# custom libraries
from samsifter.models.filter import FilterItem
from samsifter.models.parameter import FilterParameter

# global variables
TEXT = "[SAMtools] Convert SAM to BAM format"
DESC = ("Converts the text-based SAM format to the binary BAM format.")


def item():
    """Create item representing this tool in list and tree views.

    Returns
    -------
    FilterItem
        Item for use in item-based list and tree views.
    """
    filter_item = FilterItem(text=TEXT, desc=DESC,
                             icon=FilterItem.ICON_CONVERTER)
    filter_item.set_command('samtools view -S -b -')

    filter_item.add_parameter(FilterParameter(
        text="uncompressed BAM output",
        desc=("skip compression of the binary format to speed up following "
              "SAMtools steps"),
        cli_name='-u',
        default=False,
        required=False,
        active=False
    ))

    # input/output is not default (SAM sorted by queryname)
    filter_item.set_input_format('SAM')
    filter_item.set_input_sorting('any')
    filter_item.set_output_format('BAM')
    filter_item.set_output_sorting('as_input')

    return filter_item
