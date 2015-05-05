# -*- coding: utf-8 -*-

"""
.. module:: prodiguer-client/jobs/exec_ops_heartbeat.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Tests to see if remote API is up and running.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import prodiguer_client as prodiguer



def _main():
    """Main entry point.

    """
    prodiguer.ops.heartbeat()


# Main entry point.
if __name__ == '__main__':
    _main()
