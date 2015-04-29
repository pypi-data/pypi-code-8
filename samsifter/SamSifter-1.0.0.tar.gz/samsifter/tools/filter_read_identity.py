# -*- coding: utf-8 -*-
"""Wrapper for PMDtools identity filter functionality.

.. moduleauthor:: Florian Aldehoff <samsifter@biohazardous.de>
"""

# custom libraries
from samsifter.models.filter import FilterItem
from samsifter.models.parameter import (FilterParameter, FilterThreshold)

# global variables
TEXT = "[PMDtools] Filter reads by % identity"
DESC = ("Filtering reads with insufficient identity to their respective "
        "reference. Identity calculated according to PMDtools, activating all "
        "options will calculate identity according to MALT")


def item():
    """Create item representing this tool in list and tree views.

    Returns
    -------
    FilterItem
        Item for use in item-based list and tree views.
    """
    filter_item = FilterItem(text=TEXT, desc=DESC)
    filter_item.set_command('pmdtools_mod --dry --writesamfield --header')

    filter_item.add_parameter(FilterThreshold(
        text="min. identity",
        desc="minimum identity of read to reference",
        cli_name="--perc_identity",
        default=0.95,
        maximum=1.00,
        required=True,
        active=True
    ))

    filter_item.add_parameter(FilterParameter(
        text="include indels",
        desc="treat insertions and deletions as mismatches",
        cli_name="--include_indels",
        default=False
    ))

    filter_item.add_parameter(FilterParameter(
        text="include deamination",
        desc="treat possibly deaminated T>C and A>G pairs as mismatches",
        cli_name="--include_deamination",
        default=False
    ))

    filter_item.add_parameter(FilterParameter(
        text="include unknown",
        desc="treat Ns in either read or reference as mismatch",
        cli_name="--include_unknown",
        default=False
    ))

    filter_item.add_parameter(FilterParameter(
        text="verbose",
        desc="print additional information to STDERR",
        cli_name="--verbose",
        default=True,
        active=True
    ))

    filter_item.add_parameter(FilterParameter(
        text="statistics",
        desc="output summarizing statistics to STDERR",
        cli_name="--stats",
        default=False
    ))

    return filter_item
