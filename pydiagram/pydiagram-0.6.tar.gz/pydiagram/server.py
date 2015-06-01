# -*- coding: utf-8 -*-
"""
server.py
=========

This module dedicates to provide a set of utilities for communicating with remote servers.

"""
import time
import subprocess
import socket

import numpy as np

__all__ = [
    'run_command',
    'find_server',
]


def run_command(args):
    '''
    See Daily Note 2015-05-12 for details on how to run rsync via
    subprocess.Popen.
    '''
    res = subprocess.Popen(args, stdout=subprocess.PIPE,
                           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    response, err_msg = res.communicate()

    return response, err_msg


def is_server_on(server, port=22):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2.0)
        s.connect((server, port))
        s.close()
    except:
        return False

    return True


def find_server(config, num_jobs=1, info_level=-1):
    ssh = ['ssh']
    ssh_flag = ['-t', '-t']  # to keep connection
    servers = []
    for server in config.predictor.server:
        # ignore this server if qmax is negative
        if int(server.get('qmax', 0)) < 0:
            continue

        username, server_name = server.address.split('@')
        server_status = is_server_on(server_name)
        if info_level > 2:
            if server_status:
                print 'Server:', server_name, 'is on.'
            else:
                print 'Server:', server_name, 'is down.'
        if not server_status:
            continue

        queryR = ['qstat | grep {} | grep R'.format(username)]
        args = ssh + ssh_flag + [server.address] + queryR
        response, err_msg = run_command(args)
        # login failed
        if 'ssh_exchange_identification' in err_msg:
            continue
        if info_level > 2:
            print "SSH returns with following messages."
            print "SSH response:"
            print response
            print "SSH error message:"
            print err_msg
        server.number_of_running_jobs = response.count('\n')
        print 'Number of running jobs:', server.number_of_running_jobs
        time.sleep(0.2)

        queryQ = ['qstat | grep {} | grep Q'.format(username)]
        args = ssh + ssh_flag + [server.address] + queryQ
        response, err_msg = run_command(args)
        # login failed
        if 'ssh_exchange_identification' in err_msg:
            continue
        if info_level > 2:
            print "SSH returns with following messages."
            print "SSH response:"
            print response
            print "SSH error message:"
            print err_msg
        server.number_of_queuing_jobs = response.count('\n')
        print 'Number of queuing jobs:', server.number_of_queuing_jobs
        time.sleep(0.2)

        servers.append(server)

    best_server = None
    exceed_min = np.inf
    for server in servers:
        qmax = server.get('qmax', 0)
        exceed = server.number_of_queuing_jobs - qmax
        if exceed < 0:
            return server
        else:
            if exceed < exceed_min:
                best_server = server
                exceed_min = exceed

    return best_server
