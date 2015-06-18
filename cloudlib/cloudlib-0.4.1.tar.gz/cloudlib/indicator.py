# Copyright 2015, Kevin Carter.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example Usage:
>>> from cloudlib import indicator
>>> with indicator.Spinner():
>>>     print('work on import things.')

>>> # The user can also call the indicator as an opbject and close it whenever.
>>> from cloudlib import indicator
>>> spinner = indicator.Spinner()
>>> spinner.start()
>>> print('work on import things.')
>>> spinner.stop()
"""

import multiprocessing
import sys
import time


class Spinner(object):
    """Creates a visual indicator while normally performing actions."""

    def __init__(self, work_q=None, run=True, msg=None):
        """Create an indicator thread while a job is running.

        :param work_q: ``Queue.Queue`` object.
        :param msg: ``str`` message indicator.

        Context Manager Usage:
        >>> with Spinner():
        ...     # Your awesome work here...
        ...     print('hello world')

        Object Usage:
        >>> spinner = Spinner()
        >>> job = spinner.start()
        >>> # Your amazing work here...
        >>> print('hello world')
        >>> job.terminate()
        """

        self.work_q = work_q
        self.run = run
        self.job = None
        self.msg = msg

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def indicator(self):
        """Produce the spinner."""

        while self.run:
            try:
                size = self.work_q.qsize()
            except Exception:
                note = 'Please wait '
            else:
                note = 'Number of Jobs in Queue = %s ' % size

            if self.msg:
                note = '%s %s' % (note, self.msg)

            for item in ['|', '/', '-', '\\']:
                sys.stdout.write('\rProcessing - [ %s ] - %s ' % (item, note))
                sys.stdout.flush()
                time.sleep(.1)
                self.run = self.run

    def start(self):
        """Indicate that we are performing work in a thread.

        :returns: multiprocessing job object
        """

        if self.run is True:
            self.job = multiprocessing.Process(target=self.indicator)
            self.job.start()
            return self.job

    def stop(self):
        """Stop the indicator process."""

        if self.run is True and all([self.job, self.job.is_alive()]):
            print('Done.')
            self.job.terminate()
