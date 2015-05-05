# -*- coding: utf-8 -*-

"""
.. module:: prodiguer-client/jobs/exec_ops_list_endpoints.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: List set of endpoints supported by remote API.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import prodiguer_client as prodiguer



def _main():
    """Main entry point.

    """
    endpoints = prodiguer.ops.list_endpoints()
    for endpoint in sorted(endpoints):
        prodiguer.log("list endpoints :: {}".format(endpoint), module="OPS")


# Main entry point.
if __name__ == '__main__':
    _main()
