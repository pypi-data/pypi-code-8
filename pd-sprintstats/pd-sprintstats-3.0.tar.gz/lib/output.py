# Copyright:: Copyright (c) 2015 PagerDuty, Inc.
# License:: Apache License, Version 2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

from __future__ import print_function
import sys


def dot(char='.'):
    if sys.stderr.isatty():
        sys.stderr.write(char)
        sys.stderr.flush()


def output_issues(title, issues):
    print (title)
    print ('=' * len(title))
    for issue in [i for i in issues if i.fields.issuetype.name != 'Sub-task']:
        print (issue.key.ljust(10) + issue.fields.summary)
    print('\r')


def output_stats(title, stats, indent=0):
    print('\t' * indent + title)
    print('\t' * indent + '=' * len(title))
    for k, v in sorted(stats.iteritems()):
        if isinstance(v, float):
            v = round(v, 2)
        if isinstance(v, dict):
            output_stats(k, v, indent + 1)
        else:
            print('\t' * indent + k.ljust(20) + ':' + str(v))
    print('\r')
