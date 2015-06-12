from __future__ import print_function

import xml.etree.ElementTree as ET
import re

import sh

from . import (
    pbsxml, util
)

def get_pbsnodes_xml(nodes=[]):
    '''
    Return xml parsed pbsnodes -x

    .. code-block:: python

        >>> from pypbs import get_pbsnodes_xml
        >>> xml = get_pbsnodes_xml()
        >>> xml.Tag
        'Data'

    :param list nodes: list of nodes to retrieve info for 
    '''
    return util.pbs_xml_command('pbsnodes', *nodes)

def cluster_info(nodes_info):
    '''
    Get cluster status dictionary for all nodes
    in nodes_info.
    nodes_info needs to be information from pbsxml.parse_xml
    Cluster status will return the status of the cluster as a dictionary

    Dictionary will contain the following keys:

        * np_utilization - used np / total np as a (float <= 1)
        * load_utilization - load ave / total ncpus (float)
        * total_np - total of all np in cluster
        * used_np - total all np used from jobs
        * avail_np - total - used
        * running_jobs - number of jobs running

    :param dict nodes_info: pbsxml.parse_xml output for nodes
    :return: dict of cluster utilization values
    '''
    cluster_info = {
        'np_utilization': 0.0,
        'load_utilization': 0.0,
        'total_np': 0,
        'used_np': 0,
        'avail_np': 0,
        'running_jobs': 0
    }
    ncpus = 0
    for nodename, nodeinfo in nodes_info.items():
        if 'jobs' in nodeinfo:
            jobs = nodeinfo['jobs']
        else:
            jobs = []
        np = int(nodeinfo['np'])
        ncpus += int(nodeinfo['status']['ncpus'])
        loadave = float(nodeinfo['status']['loadave'])
        cluster_info['total_np'] += np
        cluster_info['load_utilization'] += loadave
        for job in jobs:
            _job = parse_job_string(job)
            cluster_info['running_jobs'] += 1
            cluster_info['used_np'] += _job['ncpus']
    cluster_info['avail_np'] = cluster_info['total_np'] - cluster_info['used_np']
    cluster_info['np_utilization'] = \
        float(cluster_info['used_np']) / cluster_info['total_np']
    cluster_info['load_utilization'] = \
        cluster_info['load_utilization'] / ncpus
    return cluster_info

def parse_job_string(job_str):
    '''
    Parse a job string of cpu/jobid.submithost or
    cpu-cpu/jobid.submithost

    Returns dictionary with keys:
    
        * ncpus - number cpus used
        * cpus - actual cpu numbers used
        * jobid - id of job
        * submit_host - submit host for job
    
    :param str job_str: job string with cpusused/jobid.submithost
    :return: 
    '''
    job = {
        'ncpus': 0,
        'cpus': [],
        'jobid': 0,
        'submit_host': ''
    }
    cpus, _job = job_str.split('/')
    jobid, submithost = _job.split('.', 1)
    job['jobid'] = int(jobid)
    job['submit_host'] = submithost

    cpus = util.parse_rangestring(cpus)
    job['ncpus'] = len(cpus)
    job['cpus'] = cpus

    return job

def cluster_status(cluster_info):
    '''
    Return a formatted string that should display cluster status nicely

    :param dict cluster_info: dict of cluster information
    '''
    template = 'NP Utilization\tCluster Load\tAvail CPU\tUsed CPU\tTotal CPU\tRunning Jobs\n'
    template += '{np_utilization:14.2%}\t{load_utilization:12.2%}\t{avail_np:9}\t{used_np:8}\t{total_np:9}\t{running_jobs:12}'
    return template.format(
        **cluster_info
    )

def main():
    xml = get_pbsnodes_xml()
    nodes = pbsxml.parse_xml(xml,'name')
    #import pprint
    #pprint.pprint(nodes)
    cinfo = cluster_info(nodes)
    print(cluster_status(cinfo))
