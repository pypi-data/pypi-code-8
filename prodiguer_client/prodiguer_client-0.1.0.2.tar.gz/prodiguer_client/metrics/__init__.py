# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client.metrics.__init__.py

   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Prodiguer client metrics sub-package intializer.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)

"""
from prodiguer_client.metrics.api_proxy import add
from prodiguer_client.metrics.api_proxy import add_batch
from prodiguer_client.metrics.api_proxy import delete
from prodiguer_client.metrics.api_proxy import fetch
from prodiguer_client.metrics.api_proxy import fetch_columns
from prodiguer_client.metrics.api_proxy import fetch_count
from prodiguer_client.metrics.api_proxy import fetch_file
from prodiguer_client.metrics.api_proxy import fetch_list
from prodiguer_client.metrics.api_proxy import fetch_setup
from prodiguer_client.metrics.api_proxy import rename
from prodiguer_client.metrics.api_proxy import set_hashes
from prodiguer_client.metrics.formatter.main import execute as format
