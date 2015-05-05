# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client/utils/api.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: API utility functions.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
import json, requests

from prodiguer_client import exceptions, options



def get_endpoint(route):
    """Returns an API endpoint for invocation.

    """
    base_url = options.get_option(options.OPT_WEB_API_URL)

    return r"{0}{1}".format(base_url, route)


def invoke(endpoint, verb=requests.get, payload=None):
    """Invokes api endpoint.

    """
    # Prepare request info.
    data = headers = None
    if payload:
        headers = {'content-type': 'application/json'}
        data = json.dumps(payload)

    # Invoke API.
    response = verb(endpoint, data=data, headers=headers, verify=False).json()

    # Raise errors.
    if 'error' in response:
        raise exceptions.WebServiceException(endpoint, response)

    return response
