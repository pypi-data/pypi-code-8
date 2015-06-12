from __future__ import print_function

from os.path import (
    join, dirname, basename
)
import os
import sys

import argparse
import sh

from . import qstat
from . import pbsxml

# Default $PBSHOME
PBSHOME = '/var/spool/torque'
# Default spool
SPOOL_DIR = join(PBSHOME, 'spool')
# Default protocol ssh or rsh
PROTOCOL = 'ssh'

OPERATIONS = {
    'follow': 'tail -f',
    'head': 'head',
    'tail': 'tail',
    'cat': 'cat',
}

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--operation',
        choices=(
            'follow', 'head', 'tail', 'cat'
        ),
        default='cat',
        help='Type of qpeek to perform[Default: %(default)s]'
    )

    parser.add_argument(
        '--protocol',
        choices=('ssh','rsh'),
        default=PROTOCOL,
        help='Protocol to connect to host with to issue operation with' \
            '[Default: %(default)s]'
    )

    parser.add_argument(
        '--spooldir',
        default=SPOOL_DIR,
        help='PBS Spool directory[Default: %(default)s]'
    )

    parser.add_argument(
        'jobid',
        help='Job id to qpeek on'
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    xml = qstat.get_qstat_xml(jobs=[args.jobid])
    jobdef = list(pbsxml.parse_xml(xml, 'Job_Id').items())[0][1]
    if jobdef['job_state'] != 'R':
        print('Job {0} is not running'.format(args.jobid))
        return
    exechost = jobdef['exec_host'].split('/')[0]
    base_filepath = join(args.spooldir,jobdef['Job_Id'] + '.*')
    #sout_filepath = base_filepath + '.OU'
    #serr_filepath = base_filepath + '.ER'
    
    protocol_cmd = getattr(sh, args.protocol)
    for line in protocol_cmd(
        exechost, OPERATIONS[args.operation], base_filepath, _iter=True
    ):
        sys.stdout.write(line)
