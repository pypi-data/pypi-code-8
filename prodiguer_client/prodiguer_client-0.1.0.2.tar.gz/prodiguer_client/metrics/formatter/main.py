# -*- coding: utf-8 -*-
"""
.. module:: prodiguer_client/metrics/formatter/formatter.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Simulation metrics formatter.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
import os
import re

import arrow

from prodiguer_client.metrics.formatter import constants
from prodiguer_client.metrics.formatter import io
from prodiguer_client.metrics.formatter import encoder
from prodiguer_client.metrics.formatter import decoder
from prodiguer_client.metrics.formatter import hashifier
from prodiguer_client.metrics.formatter import transformer



# Regular expression for validating group name.
_GROUP_ID_REGEX = '[^a-zA-Z0-9_-]'

# Min/max length of group name.
_GROUP_ID_MIN_LENGTH = 4
_GROUP_ID_MAX_LENGTH = 256

# Size of output chunk.
_CHUNK_SIZE = 50


class _ProcessingContextInfo(object):
    """Encapsulates processing context information.

    """
    def __init__(self,
        group_id,
        input_dir,
        input_format,
        output_dir,
        output_format
        ):
        """Object constructor.

        """
        self.group_id = unicode(group_id).lower()
        self.input_dir = input_dir
        self.input_files = []
        self.input_format = input_format
        self.output_dir = output_dir
        self.output_count = 0
        self.output_format = output_format
        self.set_input_file(None)
        self.timestamp = unicode(arrow.now())


    def set_input_file(self, input_file):
        """Sets input file prior to processing.

        """
        self.input_data = None
        self.input_file = input_file
        self.input_blocks = []
        self.output_chunks = []
        self.output_columns = []
        self.output_data = []


    @property
    def output_fname(self):
        """Gets filename of current output.

        """
        return "metrics-{0}-{1}".format(self.output_format, self.output_count)


def _log(msg=None):
    """Outputs a message to log.

    """
    # Format.
    if msg is not None:
        msg = "IPSL PRODIGUER INFO METRICS > {}".format(str(msg).strip())
    else:
        msg = "-------------------------------------------------------------------------------"

    # TODO output to logs.
    print msg


def _init_output_dirs(ctx):
    """Initializes output directories.

    """
    io.init_output_dir(ctx.output_dir)


def _init_input_files(ctx):
    """Initializes input files.

    """
    ctx.input_files = io.get_input_files(ctx.input_dir)


def _set_input_data(ctx):
    """Sets raw input data to be transformed into metrics.

    """
    _log("formatting input file: {}".format(ctx.input_file))

    ctx.input_data = decoder.decode(ctx.input_file, ctx.input_format)


def _set_input_blocks(ctx):
    """Transforms raw input data into blocks.

    """
    ctx.input_blocks = transformer.transform(ctx.input_data, ctx.input_format)


def _set_output_data(ctx):
    """Transforms raw input data into blocks.

    """
    ctx.output_data = encoder.encode(ctx.input_blocks, ctx.output_format, ctx.timestamp)
    for data in ctx.output_data:
        data['_formatting_timestamp'] = ctx.timestamp


def _set_hash_identifiers(ctx):
    """Sets hash identifiers.

    """
    hashifier.set_identifiers(ctx.group_id, ctx.output_data)


def _set_output_columns(ctx):
    """Assigns the output columns to be written to file system.

    """
    if ctx.output_data:
        ctx.output_columns = ctx.output_data[0].keys()


def _set_output_chunks(ctx):
    """Transforms blocks into chunks of data for output.

    """
    if not ctx.output_data:
        return

    ctx.output_chunks = [
        ctx.output_data[i:i + _CHUNK_SIZE]
        for i in xrange(0, len(ctx.output_data), _CHUNK_SIZE)
        ]


def _write_output_chunks(ctx):
    """Writes chunks of output data to file system.

    """
    # Escape if there is no output data to write.
    if not ctx.output_data:
        return

    # Write an output file per chunk.
    for output_chunk in ctx.output_chunks:
        ctx.output_count += 1
        io.write({
            'group': ctx.group_id,
            'columns': ctx.output_columns,
            'metrics': [r.values() for r in output_chunk]
        }, ctx.output_dir, ctx.output_format, ctx.output_fname)


def _validate(group_id, input_dir, input_format, output_dir, output_format):
    """Validate input parameters passed from command line.

    """
    if re.compile(_GROUP_ID_REGEX).search(group_id):
        raise ValueError("Invalid metric group id: {0}".format(group_id))
    if len(group_id) < _GROUP_ID_MIN_LENGTH or \
       len(group_id) > _GROUP_ID_MAX_LENGTH:
        raise ValueError("Invalid metric group id: {0}".format(group_id))

    if not os.path.isdir(input_dir):
        raise ValueError("Invalid input directory.")

    if input_format not in constants.INPUT_FORMAT_SET:
        err = "Invalid input format. Supported formats = {}"
        err = err.format(" | ".join(constants.INPUT_FORMAT_SET))
        raise ValueError(err)

    if not os.path.isdir(output_dir):
        raise ValueError("Invalid output directory {}.")

    if output_format not in constants.OUTPUT_FORMAT_SET:
        err = "Invalid output format. Supported formats = {}"
        err = err.format(" | ".join(constants.OUTPUT_FORMAT_SET))
        raise ValueError(err)


def execute(
    group_id,
    input_dir,
    output_dir,
    input_format=constants.INPUT_FORMAT_PCMDI,
    output_format=constants.OUTPUT_FORMAT_BLOCKS
    ):
    """Reformats metrics.

    :param str group_id: ID of metrics group to be written.
    :param str input_dir: Path to a directory containing unformateed metrics files.
    :param str input_format: Format of input files.
    :param str output_dir: Path to a directory to which reformatted metrics will be written.
    :param str output_format: Format of output files.

    """
    # Validate inputs.
    _validate(group_id, input_dir, input_format, output_dir, output_format)

    # Instantiate processing context wrapper.
    ctx = _ProcessingContextInfo(group_id,
                                 input_dir,
                                 input_format,
                                 output_dir,
                                 output_format)

    # Initialise.
    _init_output_dirs(ctx)
    _init_input_files(ctx)

    # Process each file.
    for input_file in ctx.input_files:
        ctx.set_input_file(input_file)
        for func in (
            _set_input_data,
            _set_input_blocks,
            _set_output_data,
            _set_hash_identifiers,
            _set_output_columns,
            _set_output_chunks,
            _write_output_chunks
            ):
            func(ctx)

    _log("formatted {} files".format(len(ctx.input_files)))
