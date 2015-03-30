#!/usr/bin/env python

# Copyright 2012 Stefan Hoening
# 
# This file is part of the "Chess-Problem-Editor" software.
# 
# Chess-Problem-Editor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Chess-Problem-Editor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Diese Datei ist Teil der Software "Chess-Problem-Editor".
# 
# Chess-Problem-Editor ist Freie Software: Sie koennen es unter den Bedingungen
# der GNU General Public License, wie von der Free Software Foundation,
# Version 3 der Lizenz oder (nach Ihrer Option) jeder spaeteren
# veroeffentlichten Version, weiterverbreiten und/oder modifizieren.
# 
# Chess-Problem-Editor wird in der Hoffnung, dass es nuetzlich sein wird, aber
# OHNE JEDE GEWAEHRLEISTUNG, bereitgestellt; sogar ohne die implizite
# Gewaehrleistung der MARKTFAEHIGKEIT oder EIGNUNG FUER EINEN BESTIMMTEN ZWECK.
# Siehe die GNU General Public License fuer weitere Details.
# 
# Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
# Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.


from argparse import ArgumentParser
from chessproblem.config import create_config
from chessproblem.model import Source
from chessproblem.model.db import DbService

usage = '''
This script imports sources from the file with the given filename.
The file should contain one source per line.
'''

parser = ArgumentParser(usage=usage)
parser.add_argument('filename')
parser.add_argument('-d', '--database', dest='database_url', default=None,
        help='the url of the database to lookup countries, cities and authors')
parser.add_argument('-c', '--config_dir', dest='config_dir', help='specifies the configuration directory', default=None)

args = parser.parse_args()

if args.config_dir != None:
    cpe_config = create_config(args.config_dir)
else:
    cpe_config = create_config()


def import_sources(filename, database_url):
    db_service = DbService(database_url)
    with open(filename, 'r') as f:
        for line in f:
            source_name = line.strip()
            source = Source(source_name)
            db_service.store([source])


if args.filename != None:
    if args.database_url != None:
        database_url = args.database_url
    else:
        database_url = cpe_config.database_url
    import_sources(args.filename, database_url)
else:
    parser.print_help()

