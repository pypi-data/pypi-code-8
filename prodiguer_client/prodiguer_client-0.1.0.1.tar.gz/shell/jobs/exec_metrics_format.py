# -*- coding: utf-8 -*-

"""
.. module:: prodiguer/ops/jobs/api/metric/run_format.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Formats simulation metrics in readiness for upload.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from tornado.options import define, options
import prodiguer_client as prodiguer



# Define command line options.
define("group",
       type=str,
       help="Name of metrics group (e.g. cmip5-1).")
define("input_dir",
       type=str,
       help="Path to a directory containing unformatted metrics files.")
define("output_dir",
       type=str,
       help="Path to which reformatted metrics files will be written.")


def _main():
    """Main entry point.

    """
    prodiguer.metrics.format(options.group,
                             options.input_dir,
                             options.output_dir)


# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
