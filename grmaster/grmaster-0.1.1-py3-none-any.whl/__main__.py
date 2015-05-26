#!/bin/env python3
# -*- coding: utf-8 -*-

"""
group-master - tool for dividing students into groups.

Copyright (C) 2015  Lutov V. S. <vslutov@yandex.ru>
"""

#   group-master - tool for dividing students into groups
#   Copyright (C) 2015  Lutov V. S. <vslutov@yandex.ru>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from grmaster import Manager, data, rules, server
import sys, os, subprocess, pytest

USAGE = """Usage: {0} COMMAND

Please, read the doc: <https://vslutov.github.io/group-master/>

Available commands:
  divide file     Run dividing process
  help            Show this help and exit
  license         Show license and exit
  server          Run http server at 8000 port
  template        Print csv template on stdout
  test            Run internal tests"""

def printfile(filename, file):
    """Load file from data folder and print it."""
    with data.openfile(filename) as txtfile:
        txt = txtfile.readlines()
    file.writelines(txt)


def main(argv=sys.argv, file=sys.stdout, grmaster_http_app=server.APP):
    """Print usage and exec simple commands."""
    if len(argv) == 2 and argv[1] == 'license':
        printfile('LICENSE.txt', file=file)
    elif len(argv) == 2 and argv[1] == 'template':
        printfile('template.csv', file=file)
    elif len(argv) == 3 and argv[1] == 'divide':
        input_file = open(argv[2], 'r')
        manager = Manager(input_file)
        input_file.close()
        rules.english_rule(manager)
        print(manager.students.to_csv(), file=file)
    elif len(argv) == 2 and argv[1] == 'server':
        server.run(port=8000, app=grmaster_http_app)
    elif len(argv) == 2 and argv[1] == 'test':
        path = os.path.abspath(os.path.dirname(__file__))
        sys.argv[1] = path
        pytest.main()
    else:
        print(USAGE.format(argv[0]), file=file)
