# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client/metrics/formatter/io.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Decodes metrics.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
import glob
import json
import os



def init_output_dir(output_dir):
    """Initializes output directory into which metrics will be written.

    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        for fpath in glob.glob(os.path.join(output_dir, "*.json")):
            os.remove(fpath)


def write(data, output_dir, output_format, output_file_name):
    """Writes formatted metrics data to file system.

    :param dict data: Data (dictionary format) to be written to file system.
    :param str output_dir: Path to output directory.
    :param str output_file: Name of output file.

    """
    fname = "{}.json".format(output_file_name)
    fpath = os.path.join(output_dir, fname)
    with open(fpath, 'w') as f:
        f.write(json.dumps(data, indent=4))


def get_input_files(input_dir):
    """Returns set of input files for processing.

    """
    result = glob.glob(os.path.join(input_dir, "*.json"))
    for sub_dir in next(os.walk(input_dir))[1]:
        result += get_input_files(os.path.join(input_dir, sub_dir))

    return result
