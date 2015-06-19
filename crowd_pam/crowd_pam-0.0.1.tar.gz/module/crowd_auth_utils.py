#!/usr/bin/env python
# -*- coding: utf-8 -*-
import crowd
import re
import sys
from logs import get_logger
from functools import wraps
from error import ERROR


class CrowdAuth(object):
    def __init__(self, app_url, app_name, app_pass, timeout=15, log=get_logger("DEBUG")):
        self.logger = get_logger()
        try:
            self.cs = crowd.CrowdServer(app_url, app_name, app_pass, timeout)
        except Exception as e:
            self.logger.error(
                "failed to connect to crowd server.  Exception:".format(e)
            )
            sys.exit(1)

    def _decorator_crowd_connected(func):
        @wraps(func)
        def wrapped(inst, *args, **kwargs):
            if inst.cs.auth_ping():
                return func(inst, *args, **kwargs)
            else:
                inst.logger.error(
                    "Error connecting to Crowd server {0}".format(
                        inst.cs.crowd_url
                    )
                )
                return ERROR.CROWD_CONNECT_FAILED
        return wrapped

    def contains_valid_characters(self, valid_chars):
        valid_chars_re = "^({})$".format(valid_chars)

        def func(value):
            return re.match(valid_chars_re, value)
        return func

    @_decorator_crowd_connected
    def get_groups(self, username):
        """Retrieves a list of groups where username is a direct member"""
        groups = self.cs.get_nested_groups(username)
        filtered_groups = filter(
            self.contains_valid_characters("[a-z_][a-z0-9_-]*"),
            groups
        )
        if groups != filtered_groups:
            diff = set(groups).difference(set(filtered_groups))
            self.logger.warning(
                "Unicode groups not allowed, filtered out: {}".format(diff)
            )
        return list(filtered_groups)

    @_decorator_crowd_connected
    def auth_user(self, username, password):
        """Authenticate a user against the Crowd server

        Returns a user attribute dict on success, otherwise raises Exception
        """
        authed = self.cs.auth_user(username, password)
        if authed is None:
            self.logger.error(
                "Authentication failed for user {} on {}: invalid username or password".format(
                    username,
                    self.cs.crowd_url
                )
            )
            return ERROR.AUTHENTICATION_FAILED
        else:
            check_chars = self.contains_valid_characters("[a-z_][a-z0-9_-]*")
            if not check_chars(authed['name']):
                self.logger.error(
                    "Invalid username (no Unicode allowed): {}"
                    .format(username)
                )
                return ERROR.INVALID_USERNAME
            return authed

    @_decorator_crowd_connected
    def verify_user(self, username):
        check_chars = self.contains_valid_characters("[a-z_][a-z0-9_-]*")
        if not check_chars(username):
            self.logger.error(
                "Invalid username (no Unicode allowed): {}"
                .format(username)
            )
            return ERROR.INVALID_USERNAME
        return self.cs.user_exists(username)


if __name__ == '__main__':
    ca = CrowdAuth('http://172.20.0.160:8095/crowd', 'bsapp', 'p@ssw0rd')
    print "User: %s" % ca.auth_user('test', 'password')
