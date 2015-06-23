# Copyright (c) 2015 Faculty of Engineering of the University of Porto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Module for declaring an Abstract class for Analysis.

If we want to add a new way of analyzing a repository, it's necessary to create a subclass
of AbstractAnalysis and override abstract methods.
"""

import abc


class AbstractAnalysis:
    """ Abstract class for Analysis.

    An Abstract Analysis class using Template Design Pattern to ensure a standard.

    Attributes:
        repository: A repository instance.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, repository):
        """ Inits AbstractAnalysis.

        Args:
            repository: A Repository instance.
        """
        self.repository = repository

    @abc.abstractmethod
    def analyze(self):
        """ Analyzes a repository and returns a RepositoryAnalytics instance. """
