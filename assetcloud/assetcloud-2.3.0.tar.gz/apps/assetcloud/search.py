# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Haystack utilities.

Can't call this 'haystack' because that name makes Haystack do special things
with it (try it and see - you'll get an error) so I've called it 'search'
instead.
"""


def assets_from_results(results):
    """
    Return the list of assets from a set of results.
    """
    return [result.object for result in results]


def pks_from_results(results):
    """
    Return the list of assets IDs from a set of results.
    """
    return [result.pk for result in results]
