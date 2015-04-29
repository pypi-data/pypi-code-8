# -*- coding: utf-8 -*-
"""
Wrapper for BetterRMDup

.. moduleauthor:: Florian Aldehoff <samsifter@biohazardous.de>
"""

# custom libraries
from samsifter.models.filter import FilterItem

# global variables
TEXT = "[BetterRMDup] Remove duplicates"
DESC = ("Removes duplicate reads with identical start and stop coordinates.")


def item():
    """Create item representing this tool in list and tree views.

    Returns
    -------
    FilterItem
        Item for use in item-based list and tree views.
    """
    filter_item = FilterItem(text=TEXT, desc=DESC)
#    filter_item.set_command('java -jar BetterRMDupv0.9.jar -')
    filter_item.set_command('betterrmdup -')

    # input/output is not default (SAM sorted by queryname)
    filter_item.set_input_format('BAM')
    filter_item.set_input_sorting('coordinate')
    filter_item.set_output_format('BAM')
    filter_item.set_output_sorting('coordinate')

    return filter_item
