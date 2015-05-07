#!/usr/bin/env python
#
#   Copyright 2015 Linux2Go
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
import requests
import argparse
import sys
import time
import select

def create_new(args):
    resp = requests.post(args.url + '/new')
    retval = resp.json()
    print 'Read/Write URL:        ', retval['rw_url']
    print 'Read-only URL:         ', retval['ro_url']
    print 'Friendly read-only URL:', retval['html_ro_url']
    return retval['rw_url']

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()

    parser.add_argument('--url', default='http://streambin.net',
                        help="Service URL")
    parser.add_argument('uuid',
                        help='Read/write ID (Use "new" to create new stream)')
    parser.add_argument('file', help="File to upload (- denotes stdin)")

    args = parser.parse_args()

    if args.uuid == 'new':
        write_url = create_new(args)
    else:
        write_url = args.url + '/' + args.uuid

    if args.file == '-':
        fp = sys.stdin
    else:
        fp = open(args.file, 'r')

    last_post = 0
    buf = ''

    while True:
        while True:
            now = time.time()

            if fp in select.select([fp], [], [], 1)[0]:
                l = fp.readline()
                buf += l

            if l == '' or (now - last_post) > 1:
                break

        if buf:
            requests.post(write_url, buf)

        if l == '':
            # fp.readline() only returns an empty line
            # on EOF
            break

        buf = ''
        last_post = now


if __name__ == '__main__':
    sys.exit(not main())
