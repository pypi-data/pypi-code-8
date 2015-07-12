#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Metrium System
# Copyright (C) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Metrium System.
#
# Hive Metrium System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Metrium System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Metrium System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import quorum

from metrium import models

from . import base

SLEEP_TIME = 120.0
""" The default sleep time to be used by the bots
in case no sleep time is defined in the constructor,
this bot uses a large value as its tick operation is
a lot expensive and should be used with care """

class GithubBot(base.Bot):

    def __init__(self, sleep_time = SLEEP_TIME, *args, **kwargs):
        base.Bot.__init__(self, sleep_time, *args, **kwargs)

    def tick(self):
        api = models.GithubConfig.get_api()
        config = models.GithubConfig.singleton()

        activity = self.activity(api, config)
        commits_total = self.commits_total(api, activity)

        _github = models.Github.get(raise_e = False)
        if not _github: _github = models.Github()
        _github.commits_total = commits_total
        _github.save()

        pusher = quorum.get_pusher()
        pusher.trigger("global", "github.commits_total", {
            "commits_total" : commits_total
        })

    def activity(self, api, config):
        activity = dict()
        for repo in config.repos:
            owner, repo = repo.split("/", 1)
            item = api.stats_activity_repo(owner, repo)
            activity[repo] = item
        return activity

    def commits_total(self, api, activity):
        count = [0, 0]
        for _repo, item in quorum.legacy.iteritems(activity):
            if not item: continue
            item_l = len(item)
            current = item[-1]
            previous = item[-2] if item_l > 1 else dict(total = 0)
            current_t = current["total"]
            previous_t = previous["total"]
            count[0] += previous_t
            count[1] += current_t
        return count
