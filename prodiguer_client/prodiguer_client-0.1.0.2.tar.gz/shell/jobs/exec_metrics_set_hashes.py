# -*- coding: utf-8 -*-

"""
.. module:: prodiguer/ops/jobs/api/metric/run_set_hashes.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Reassigns hash identifiers for a group of metrics.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from tornado.options import define, options
import prodiguer_client as prodiguer



# Define command line options.
define("group",
       type=str,
       help="Name of metrics group whose hash identifiers are to be reset (e.g. cmip5-1).")


def _main():
    """Main entry point.

    """
    prodiguer.metrics.set_hashes(options.group)


# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
