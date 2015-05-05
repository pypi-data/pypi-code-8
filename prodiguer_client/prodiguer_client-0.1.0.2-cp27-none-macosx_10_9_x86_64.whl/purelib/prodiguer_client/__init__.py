# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client.__init__.py

   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Prodiguer client root package intializer.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)

"""

__title__ = 'prodiguer_client'
__version__ = '0.1.0.2'
__author__ = 'Mark Anthony Greenslade'
__license__ = 'GPL / CeCILL'
__copyright__ = 'Copyright 2015 IPSL'


from prodiguer_client import metrics
from prodiguer_client import ops
from prodiguer_client.utils.runtime import log
from prodiguer_client.options import list_options
from prodiguer_client.options import OPT_WEB_API_URL
from prodiguer_client.options import set_option
