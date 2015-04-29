# -*- coding: utf-8 -*-
"""
Wrapper for SAMtools rmdup

.. moduleauthor:: Florian Aldehoff <samsifter@biohazardous.de>
"""

# custom libraries
from samsifter.models.filter import FilterItem
from samsifter.models.parameter import FilterParameter

# global variables
TEXT = "[SAMtools] Remove duplicates"
DESC = ("Removes duplicate reads with identical start coordinates.")


def item():
    """Create item representing this tool in list and tree views.

    Returns
    -------
    FilterItem
        Item for use in item-based list and tree views.
    """
    filter_item = FilterItem(text=TEXT, desc=DESC)
    filter_item.set_command('samtools rmdup - -')

    filter_item.add_parameter(FilterParameter(
        text="rmdup for SE reads",
        desc="remove duplicate single-end reads",
        cli_name='-s',
        default=True,
        required=False,
        active=True
    ))

    filter_item.add_parameter(FilterParameter(
        text="treat PE as SE",
        desc="treat paired-end reads as single-end reads",
        cli_name='-S',
        default=False,
        required=False,
        active=False))

    # input/output is not default (SAM sorted by queryname)
    filter_item.set_input_format('BAM')
    filter_item.set_input_sorting('coordinate')
    filter_item.set_output_format('BAM')
    filter_item.set_output_sorting('coordinate')

    return filter_item
