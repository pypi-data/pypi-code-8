# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client/metrics/formatter/constants.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Constants used across the package.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""

# Supported input formats.
INPUT_FORMAT_PCMDI = 'pcmdi'

# Set of supported input formats.
INPUT_FORMAT_SET = set([
	INPUT_FORMAT_PCMDI,
	])


# Supported output formats.
OUTPUT_FORMAT_BLOCKS = 'blocks'

# Set of supported output formats.
OUTPUT_FORMAT_SET = set([
	OUTPUT_FORMAT_BLOCKS,
	])
