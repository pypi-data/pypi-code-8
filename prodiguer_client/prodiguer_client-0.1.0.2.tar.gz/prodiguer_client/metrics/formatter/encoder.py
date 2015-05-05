# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client/metrics/formatter/encoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encodes metrics prior to being written to file system.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
from prodiguer_client.metrics.formatter import encoder_blocks



# Map of supported encoders.
_ENCODERS = {
    'blocks': encoder_blocks.encode
}


def encode(blocks, output_format, timestamp):
    """Encodes blocks of metrics.

    :param list blocks: Blocks of metrics for encoding.
    :param str output_format: Type of output to be emitted.
    :param int timestamp: Formatting timestamp useful for grouping.

    :returns: Encoded metrics.
    :rtype: list

    """
    encoder = _ENCODERS[output_format]

    return encoder(blocks, timestamp)
