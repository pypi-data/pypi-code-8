# -*- coding: utf-8 -*-

"""
.. module:: prodiguer/ops/jobs/api/metric/run_fetch_file.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Fetches a set of metrics and saves them to local file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from tornado.options import define, options
import prodiguer_client as prodiguer



# Define command line options.
define("group",
       help="ID of a metrics group")
define("filter",
       default=None,
       help="Path to a metrics filter to be applied")
define("output_dir",
       type=str,
       help="Path to which downloaded metrics files will be written.")



def _main():
    """Main entry point.

    """
    filepath = prodiguer.metrics.fetch_file(options.group, options.filter)
    prodiguer.log("fetch-file :: {}".format(filepath), module="METRICS")


# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
