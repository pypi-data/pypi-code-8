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

from ConfigParser import SafeConfigParser
import os


def parse_config(args):
    settings = {}
    parser = SafeConfigParser()
    config_precedence = [
        '/etc/sprintstats.cfg',
        '/usr/local/etc/sprintstats.cfg',
        '~/.sprintstats.cfg',
        'config.cfg'
    ]
    config_file = None

    for f in config_precedence:
        f = os.path.expanduser(f)
        if os.path.exists(f):
            config_file = f

    if args and args.config:
        if os.path.exists(args.config):
            config_file = args.config
        else:
            print('WARNING: Specified config file {0} not found'.format(
                (os.path.abspath(args.config))))
            if config_file and os.path.exists(config_file):
                print(
                    'Using {0} instead.'.format(os.path.abspath(config_file)))

    if config_file and os.path.exists(config_file):
        parser.read(config_file)
        if parser.has_section('default'):
            settings = dict(parser.items('default'))
    if 'default_points' not in settings:
        settings['default_points'] = 0
    return settings
