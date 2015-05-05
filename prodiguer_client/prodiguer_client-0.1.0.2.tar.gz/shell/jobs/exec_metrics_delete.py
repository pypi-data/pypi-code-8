# -*- coding: utf-8 -*-

"""
.. module:: prodiguer/ops/jobs/api/metric/run_delete.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Deletes simulation metrics from remote repository.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from tornado.options import define, options
import prodiguer_client as prodiguer



# Define command line options.
define("group",
       help="ID of a metrics group")
define("filter",
       default=None,
       help="Path to a metrics filter to be applied prior to deletion")


def _main():
    """Main entry point.

    """
    prodiguer.metrics.delete(options.group, options.filter)



# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
