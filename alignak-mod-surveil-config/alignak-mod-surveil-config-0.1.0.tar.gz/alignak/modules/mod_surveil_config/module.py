#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2009-2012:
# Gabes Jean, naparuba@gmail.com
# Gerhard Lausser, Gerhard.Lausser@consol.de
# Gregory Starck, g.starck@gmail.com
# Hartmut Goebel, h.goebel@goebel-consult.de
#
# This file is part of Alignak
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken. If not, see <http://www.gnu.org/licenses/>.

"""
This module job is to get configuration data from Surveil
"""

import surveilclient

from alignak.basemodule import BaseModule
from alignak.log import logger

properties = {
    'daemons': ['arbiter'],
    'type': 'surveil_config',
    'external': False,
    'phases': ['configuration'],
}


def get_instance(mod_conf):
    logger.info(
        "[surveil_config] Get an influxdb data module for plugin %s"
        % mod_conf.get_name()
    )
    instance = SurveilConfig(mod_conf)
    return instance


class SurveilConfig(BaseModule):
    def __init__(self, modconf):
        BaseModule.__init__(self, modconf)
        self.surveil_api_url = getattr(modconf, 'surveil_api_url', None)
        self.surveil_auth_url = getattr(modconf, 'surveil_auth_url', None)
        self.surveil_version = getattr(modconf, 'surveil_version', None)

    def init(self):
        self.surveil_client = surveilclient.client.Client(
            self.surveil_api_url,
            auth_url=self.surveil_auth_url,
            version=self.surveil_version
        )

################################ Arbiter part #################################

    # Main function that is called in the CONFIGURATION phase
    def get_objects(self):
        if not self.db:
            logger.error("[Mongodb Module]: Problem during init phase")
            return {}

        r = {}

        tables = ['hosts', 'services', 'contacts', 'commands', 'timeperiods']
        for t in tables:
            r[t] = []

            cur = getattr(self.db, t).find({'_state': {'$ne': 'disabled'}})
            for h in cur:
                #print "DBG: mongodb: get an ", t, h
                # We remove a mongodb specific property, the _id
                del h['_id']
                # And we add an imported_from property to say it came from
                # mongodb
                h['imported_from'] = 'mongodb:%s:%s' % (self.uri, self.database)
                r[t].append(h)

        return r

    # Function called by the arbiter so we import the objects in our databases
    def import_objects(self, data):
        if not self.db:
            logger.error("[Mongodb]: error Problem during init phase")
            return False

        for t in data:
            col = getattr(self.db, t)
            print "Saving objects %s" % t
            elts = data[t]
            for e in elts:
                print "Element", e
                e['_id'] = self.get_uniq_id(t, e)
                col.save(e)


        return True