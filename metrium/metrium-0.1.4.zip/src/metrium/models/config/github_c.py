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

import github
import quorum

from . import base

SCOPE = (
    "user:email",
    "repo"
)

class GithubConfig(base.Config):

    access_token = dict(
        index = True
    )

    username = dict(
        index = True
    )

    repos = dict(
        type = list
    )

    @classmethod
    def validate_new(cls):
        return super(GithubConfig, cls).validate_new() + [
            quorum.not_null("access_token"),
            quorum.not_empty("access_token"),

            quorum.not_null("username"),
            quorum.not_empty("username")
        ]

    @classmethod
    def get_api(cls, scope = SCOPE):
        config = cls.singleton()
        api = github.Api(scope = scope)
        api.access_token = config and config.access_token
        return api

    def pre_create(self):
        base.Config.pre_create(self)

        self.name = "github"
