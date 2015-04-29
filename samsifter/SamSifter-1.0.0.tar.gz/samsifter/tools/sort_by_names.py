# -*- coding: utf-8 -*-
"""Wrapper for SAMtools sort functionality for sorting reads by queryname.

.. moduleauthor:: Florian Aldehoff <samsifter@biohazardous.de>
"""

# custom libraries
from samsifter.models.filter import FilterItem

# global variables
TEXT = "[SAMtools] Sort by query names"
DESC = ("Resorts entries in a BAM file by their names.")


def item():
    """Create item representing this tool in list and tree views.

    Returns
    -------
    FilterItem
        Item for use in item-based list and tree views.
    """
    filter_item = FilterItem(text=TEXT, desc=DESC, icon=FilterItem.ICON_SORTER)
    filter_item.set_command('samtools sort -n - tmp -o')

    # input/output is not default (SAM sorted by queryname)
    filter_item.set_input_format('BAM')
    filter_item.set_input_sorting('coordinate')
    filter_item.set_output_format('BAM')
    filter_item.set_output_sorting('queryname')

    return filter_item
