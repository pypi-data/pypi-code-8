# -*- coding: utf-8 -*-

"""
.. module:: prodiguer/ops/jobs/api/metric/run_rename.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Renames a group of metrics.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from tornado.options import define, options
import prodiguer_client as prodiguer



# Define command line options.
define("group",
       type=str,
       help="Name of metrics group to be renamed (e.g. cmip5-1).")
define("new_name",
       type=str,
       help="New group name.")


def _main():
    """Main entry point.

    """
    prodiguer.metrics.rename(options.group, options.new_name)


# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
