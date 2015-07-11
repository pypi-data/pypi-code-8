# Ubuntu CI Engine
# Copyright 2015 Canonical Ltd.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License version 3, as
# published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

# A very nice and consice summary about timeouts and retries and why using any
# network related resource requires them:
# https://docs.aws.amazon.com/general/latest/gr/api-retries.html


class ExponentialBackoff(object):
    """Provides wait times summing up to a limit.

    When an operation can fail transiently, it can be retried several times
    until it succeeds up to a specified limit. The returned values are the
    succesive wait times and their total equals ``up_to``.

    :note: ``retries`` + 1 values are returned, the last values may end up
        being repeated and equal to zero. I.e. the caller decides how many
        retries will be attempted and ``up_to`` is the upper limit for
        total. This mimics manual retries by a user re-trying randomly but
        giving up after a limit.
    """

    def __init__(self, first, up_to, retries):
        self.first = first
        self.up_to = up_to
        self.retries = retries

    def __iter__(self):
        attempts = 1
        backoff = self.first
        cumulated = backoff
        # Yield the time to wait between retries
        while attempts < self.retries:
            if cumulated + backoff > self.up_to:
                backoff = 0
            else:
                cumulated += backoff
            yield backoff
            backoff = (2 ** attempts) * random.random()
            attempts += 1
        if self.retries:
            yield (self.up_to - cumulated)
