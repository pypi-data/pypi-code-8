#!/usr/bin/env python
#
# Copyright 2015 Trey Morris
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import argparse
import os
from gister import gister


def parse_arguments():
    parser = argparse.ArgumentParser(description='generate ipynb links!')
    parser.add_argument('-a', '--anonymous', action='store_true',
                        help='gist will be anonymous'
                             'even if you have oauth configured')
    parser.add_argument('-e', '--edit', nargs=1, metavar='id/url',
                        help='edit a gist identified by id or url')
    return parser.parse_args()


def get_files():
    nb_path = os.path.expanduser('~/.ipython/notebooks')
    files = os.listdir(nb_path)
    files = [f for f in files if f[-6:] == '.ipynb']
    for i, f in enumerate(files):
        print '%d. %s' % (i+1, f)
    x = raw_input('enter the number for the notebook you want link to: ')
    x = int(x) - 1
    if x <= len(files):
        return ['%s/%s' % (nb_path, files[x])]
    return []


def print_nbviewer_url():
    args = parse_arguments()
    files = get_files()

    print gister.create_gist(anonymous=args.anonymous, files=files,
                             edit=args.edit)
