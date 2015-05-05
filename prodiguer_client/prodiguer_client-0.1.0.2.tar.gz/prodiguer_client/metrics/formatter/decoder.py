# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client/metrics/formatter/decoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Decodes metrics.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
import json

from prodiguer_client.metrics.formatter import decoder_pcmdi



# Map of supported decoders keyed by file format.
_DECODERS = {
    'pcmdi': decoder_pcmdi.decode
}


def _get_data(input_file):
    """Returns raw metrics data from an input file.

    """
    with open(input_file, 'r') as input_file:
        return json.loads(input_file.read())


def decode(input_file, input_format):
    """Decodes set of metrics files.

    :param str input_file: An input file to be decoded.
    :param str input_format: Metrics format of input file.

    :returns: Input data to be processed.
    :rtype: list

    """
    decoder = _DECODERS[input_format]

    return decoder(input_file, _get_data(input_file))
