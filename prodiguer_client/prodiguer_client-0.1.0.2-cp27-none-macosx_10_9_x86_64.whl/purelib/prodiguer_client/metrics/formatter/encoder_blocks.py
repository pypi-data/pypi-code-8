# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client/metrics/formatter/encoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encodes blocks of metrics.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
from collections import OrderedDict



# Collection of block sections.
_BLOCK_SECTIONS = ['masking', 'simulation', 'regridding', 'reference']

# Maps certain fields.
_FIELD_MAPPER = {
    "mipTable": "MIP",
    "trackingId": "trackingID"
}


def _get_section_field_name(section_name, field_name):
    """Returns a formatted block section field name.

    """
    if field_name in _FIELD_MAPPER:
        field_name = _FIELD_MAPPER[field_name]

    return "{0}{1}".format(
        section_name,
        field_name[0].upper() + field_name[1:])


def _encode_section(section, section_name):
    """Encodes a block section.

    """
    result = []
    for field_name in sorted(section.keys()):
        field_value = section[field_name]
        field_name = _get_section_field_name(section_name, field_name)
        result.append((field_name, field_value))

    return result


def _encode(block, timestamp):
    """Encodes an individual block.

    """
    result = []

    # Set sections.
    for section_name in _BLOCK_SECTIONS:
        section = block[section_name]
        result += _encode_section(section, section_name)

    # Set metrics.
    result += [(m['fullName'], m['result']) for m in block['metrics']]

    # Set variable.
    result.append(('variable', block['variable']))

    # Set metric creation date.
    result.append(('metricCreationDate', block['metricCreationDate']))

    # Return dictionary with sorted keys.
    return OrderedDict(sorted(result, key=lambda i: i[0]))


def encode(blocks, timestamp):
    """Encodes blocks of metrics.

    :param list blocks: Blocks of metrics for encoding.
    :param int timestamp: Formatting timestamp used to group uploads.

    :returns: Metrics encoded as blocks.
    :rtype: list

    """
    return [_encode(block, timestamp) for block in blocks]
