# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client/metrics/api_proxy.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Proxy to the remote metrics web-service API.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
import collections
import json
import logging
import os
import tempfile

import requests

from prodiguer_client.utils import api
from prodiguer_client.utils import runtime as rt
from prodiguer_client.utils import io



# Reduce requests logging to warnings + errors only.
logging.getLogger("requests").setLevel(logging.WARNING)

# API endpoints.
_EP_ADD = r"/api/1/metric/add?duplicate_action={0}"
_EP_DELETE = r"/api/1/metric/delete?group={0}"
_EP_FETCH_GROUP = r"/api/1/metric/fetch?group={0}"
_EP_FETCH_COLUMNS = r"/api/1/metric/fetch_columns?group={0}"
_EP_FETCH_COUNT = r"/api/1/metric/fetch_count?group={0}"
_EP_FETCH_LIST = r"/api/1/metric/fetch_list"
_EP_FETCH_SETUP = r"/api/1/metric/fetch_setup?group={0}"
_EP_RENAME = r"/api/1/metric/rename?group={0}&new_name={1}"
_EP_SET_HASHES = r"/api/1/metric/set_hashes?group={0}"

# Actions to take when uploading duplicate metrics.
_ADD_DUPLICATE_ACTION_SKIP = 'skip'
_ADD_DUPLICATE_ACTION_FORCE = 'force'
_ADD_DUPLICATE_ACTION_SET = set([
    _ADD_DUPLICATE_ACTION_SKIP,
    _ADD_DUPLICATE_ACTION_FORCE
    ])


def _parse_group_id(group_id):
    """Parses a metrics group identifier.

    """
    if group_id:
        group_id = unicode(group_id).strip().lower()
    if not group_id:
        raise ValueError("group_id is undefined.")

    return group_id


def _log(action, msg=None):
    """Logger helper function.

    """
    if not msg:
        msg = action
    else:
        msg = "{0} :: {1}".format(action.upper(), msg)
    rt.log(msg, module="METRIC")


def _get_metric_block(columns, values):
    """Returns a metric block hydrated from a set of columns
    and a list of values.

    """
    return [(c, values[i]) for i, c in enumerate(columns)]


def _parse_duplicate_action(action):
    """Parses duplicate hash action.

    """
    if action not in _ADD_DUPLICATE_ACTION_SET:
        raise ValueError("Invalid duplicate metric action")

    return action


def add(metrics_filepath, duplicate_action=_ADD_DUPLICATE_ACTION_SKIP):
    """Adds metrics to remote repository.

    :param str metrics_filepath: Path to a file containing metrics to be uploaded.
    :param str duplicate_action: Action to take when encountering a metric set with a duplicate hash identifier.

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    # Parse params.
    metrics = io.parse_json_filepath(metrics_filepath, force=True)
    duplicate_action = _parse_duplicate_action(duplicate_action)

    # Invoke api.
    endpoint = api.get_endpoint(_EP_ADD.format(duplicate_action))
    response = api.invoke(endpoint, verb=requests.post, payload=metrics)

    # Inform user.
    msg = "processed file: {}".format(metrics_filepath)
    msg += " (added row count={0}, duplicate row count={1})".format(
        response['addedCount'], response['duplicateCount'])
    msg += "."
    _log("add", msg)


def add_batch(metrics_dirpath, duplicate_action=_ADD_DUPLICATE_ACTION_SKIP):
    """Adds a batch metrics to remote repository.

    :param str metrics_dirpath: Path to a directory containing metric files to be uploaded.
    :param str duplicate_action: Action to take when encountering a metric set with a duplicate hash identifier.

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    # Parse params.
    metrics_dirpath = io.parse_dirpath(metrics_dirpath)
    duplicate_action = _parse_duplicate_action(duplicate_action)

    # Process files.
    for metrics_filepath in os.listdir(metrics_dirpath):
        add(os.path.join(metrics_dirpath, metrics_filepath), duplicate_action)


def delete(group_id, group_filter_filepath=None):
    """Deletes a group of metrics.

    :param str group_id: A metrics group identifier.
    :param str group_filter_filepath: Path to a metrics group filter json file.

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    # Parse params.
    group_id = _parse_group_id(group_id)
    group_filter = io.parse_json_filepath(group_filter_filepath)

    # Invoke API.
    endpoint = api.get_endpoint(_EP_DELETE.format(group_id))
    api.invoke(endpoint, verb=requests.post, payload=group_filter)

    # Inform user.
    _log("delete", "Group {0} metrics sucessfully deleted".format(group_id))


def fetch(group_id, group_filter_filepath=None):
    """Returns a group of metrics.

    :param str group_id: A metrics group identifier.
    :param str group_filter_filepath: Path to a metrics group filter json file.

    :returns: A group of metrics.
    :rtype: list

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    # Parse params.
    group_id = _parse_group_id(group_id)
    group_filter = io.parse_json_filepath(group_filter_filepath)

    # Invoke API.
    endpoint = api.get_endpoint(_EP_FETCH_GROUP.format(group_id))
    response = api.invoke(endpoint, payload=group_filter)

    # Format API response.
    data = response['metrics']
    data = [m for m in data if len(m) == len(response['columns'])]
    data = [_get_metric_block(response['columns'], m) for m in data]

    return [collections.OrderedDict(m) for m in data]


def fetch_file(group_id, group_filter_filepath=None):
    """Downloads a group of metrics and saves them file system.

    :param str group_id: A metrics group identifier.
    :param str group_filter_filepath: Path to a metrics group filter json file.

    :returns: Path to a temporary file containing the downloaded metrics.
    :rtype: str

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    data = fetch(group_id, group_filter_filepath)
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as output_file:
        output_file.write(json.dumps(data, indent=4))

    return output_file.name


def fetch_columns(group_id):
    """Returns set of field names associated with a group of metrics.

    :param str group_id: A metrics group identifier.

    :returns: Set of column names associated with a group of metrics.
    :rtype: set

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    # Parse params.
    group_id = _parse_group_id(group_id)

    # Invoke API.
    endpoint = api.get_endpoint(_EP_FETCH_COLUMNS.format(group_id))
    response = api.invoke(endpoint)

    return set(response['columns'])


def fetch_count(group_id, group_filter_filepath=None):
    """Returns count of metrics within a group.

    :param str group_id: A metrics group identifier.
    :param str group_filter_filepath: Path to a metrics group filter json file.

    :returns: Count of number of metrics within a group.
    :rtype: int

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    # Parse params.
    group_id = _parse_group_id(group_id)
    group_filter = io.parse_json_filepath(group_filter_filepath)

    # Invoke API.
    endpoint = api.get_endpoint(_EP_FETCH_COUNT.format(group_id))
    response = api.invoke(endpoint, payload=group_filter)

    return int(response['count'])


def fetch_list():
    """Returns set of metric groups within remote repository.

    :returns: Set of metric groups within remote repository.
    :rtype: set

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    # Invoke API.
    endpoint = api.get_endpoint(_EP_FETCH_LIST)
    response = api.invoke(endpoint)

    return set(response['groups'])


def fetch_setup(group_id, group_filter_filepath=None):
    """Returns setup data associated with a group of metrics.

    The setup data is the set of unique values for each field within the metric group.

    :param str group_id: A metrics group identifier.
    :param str group_filter_filepath: Path to a metrics group filter json file.

    :returns: Setup data associated with a group of metrics.
    :rtype: collections.OrderedDict

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    # Parse params.
    group_id = _parse_group_id(group_id)
    group_filter = io.parse_json_filepath(group_filter_filepath)

    # Invoke API.
    endpoint = api.get_endpoint(_EP_FETCH_SETUP.format(group_id))
    response = api.invoke(endpoint, payload=group_filter)

    # Format API response.
    data = response['data']
    data = [(c, data[i]) for i, c in enumerate(response['columns'])]

    return collections.OrderedDict(data)


def rename(group_id, new_group_id):
    """Renames an existing group of metrics.

    :param str group_id: ID of a metric group.
    :param str new_group_id: New ID of the metric group.

    :raises prodiguer_client.exceptions.WebServiceException: If the web-service reports an error.

    """
    # Parse params.
    group_id = _parse_group_id(group_id)
    new_group_id = _parse_group_id(new_group_id)

    # Invoke API.
    endpoint = api.get_endpoint(_EP_RENAME.format(group_id, new_group_id))
    api.invoke(endpoint, verb=requests.post)

    # Inform user.
    _log("rename", \
         "Group {0} sucessfully renamed {1}".format(group_id, new_group_id))


def set_hashes(group_id):
    """Resets hash identifiers over a group of metrics.

    """
    # Parse params.
    group_id = _parse_group_id(group_id)

    # Invoke API.
    endpoint = api.get_endpoint(_EP_SET_HASHES.format(group_id))
    api.invoke(endpoint, verb=requests.post)

    # Inform user.
    _log("set_hashes", \
         "Group {} hashes sucessfully reset".format(group_id))
