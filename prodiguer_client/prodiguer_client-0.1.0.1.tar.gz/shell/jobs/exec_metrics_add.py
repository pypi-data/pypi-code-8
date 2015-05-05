# -*- coding: utf-8 -*-

"""
.. module:: prodiguer/ops/jobs/api/metric/run_add.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Uploads simulation metrics to remote repository.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from tornado.options import define, options
import prodiguer_client as prodiguer



# Define command line options.
define("file",
       help="Path to a metrics file to be uploaded to server")
define("duplicate_action",
       help="Action to take when adding a metric with a duplicate hash identifier")


def _main():
    """Main entry point.

    """
    prodiguer.metrics.add(options.file, options.duplicate_action)


# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
