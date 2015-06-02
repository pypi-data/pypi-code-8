#!/usr/bin/env pypy
#-*- coding: utf-8 -*-

import os, sys
import math
from collections import *

from prob import *
from wordseg import context, Context, TopicContext

############################################################

class StrDist(object):
    # Following Mochihashi et al.'s (2009) HDP model

    def __init__(
        self, n, alpha, theta, p_stop=None, dists=None
    ):
        assert 0 <= alpha < 1
        assert theta > 0.0
        if dists is None:
            dists = []
            for i in xrange(n):
                dists.append(CRP(alpha, theta))
        self._n = n
        self._alpha = alpha
        self._theta = theta
        self._p_stop = p_stop
        self._dists = dists

    def __copy__(self):
        return StrDist(
            self._n, self._alpha, self._theta, self._p_stop,
            copy.deepcopy(self._dists)
        )

    def clear(self):
        for i in xrange(self._n):
            self._dists[i].clear()

    def repr(self):
        result = '<<STRING DISTRIBUTION>>'
        result += '\nalpha = %f' % self._alpha
        result += '\ntheta = %f' % self._theta
        result += '\np_stop = %s' % self._p_stop
        for i in xrange(self._n):
            result += '\n%d-gram Distribution: %s' % (
                i + 1, self._dists[i]
            )
        return result

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def pdf(self, s):
        result = 1.0
        for i in xrange(len(s)):
            q = self.pdf_n(self._n, s, i)
            result *= q
        if self._p_stop is not None:
            result *= self._p_stop * ((1.0 - self._p_stop) ** len(s))
        return result

    def learn(self, s):
        for i in xrange(len(s)):
            self.learn_n(self._n, s, i)

    def forget(self, s):
        for i in xrange(len(s)):
            self.forget_n(self._n, s, i)

    def pdf_n(self, n, s, i):
        if n <= 1:
            q = self._dists[0].pdf(s[i])
            return q
        else:
            result = 1.0
            dist = self._dists[n - 1]
            (t0, ts) = context(n, s, i)
            ctx = Context(ts)
            q = dist.pdf(t0, ctx)
            if dist.contains(t0, ctx):
                result *= q
            else:
                result *= q * self.pdf_n(n - 1, s, i)
            return result

    def learn_n(self, n, s, i):
        if n <= 1:
            self._dists[0].inc(s[i])
        else:
            dist = self._dists[n - 1]
            (t0, ts) = context(n, s, i)
            ctx = Context(ts)
            dist.inc(t0, ctx)
            self.learn_n(n - 1, s, i)

    def forget_n(self, n, s, i):
        if n <= 1:
            self._dists[0].dec(s[i])
        else:
            dist = self._dists[n - 1]
            (t0, ts) = context(n, s, i)
            ctx = Context(ts)
            dist.dec(t0, ctx)
            self.forget_n(n - 1, s, i)

############################################################

class TopicStrDist(StrDist):

    def __init__(
        self, n, alpha, theta, p_stop=None, dists=None
    ):
        super(TopicStrDist, self).__init__(
            n, alpha, theta, p_stop, dists
        )

    def __copy__(self):
        return TopicStrDist(
            self._n, self._alpha, self._theta, self._p_stop,
            copy.deepcopy(self._dists)
        )

    def repr(self):
        result = '<<TOPIC-BASED STRING DISTRIBUTION>>'
        result += '\nalpha = %f' % self._alpha
        result += '\ntheta = %f' % self._theta
        result += '\np_stop = %f' % self._p_stop
        for i in xrange(self._n):
            result += '\n%d-gram Distribution: %s' % (
                i + 1, self._dists[i]
            )
        return result

    def pdf(self, s, z):
        result = 1.0
        for i in xrange(len(s)):
            result *= self.pdf_n(self._n, s, z, i)
        if self._p_stop is not None:
            result *= self._p_stop * ((1.0 - self._p_stop) ** len(s))
        return result

    def learn(self, s, z):
        for i in xrange(len(s)):
            self.learn_n(self._n, s, z, i)

    def forget(self, s, z):
        for i in xrange(len(s)):
            self.forget_n(self._n, s, z, i)

    def pdf_n(self, n, s, z, i):
        if n <= 1:
            return self._dists[0].pdf(s[i], z)
        else:
            result = 1.0
            dist = self._dists[n - 1]
            (t0, ts) = context(n, s, i)
            ctx = TopicContext(ts, z)
            if dist.contains(t0, ctx):
                result *= dist.pdf(t0, ctx)
            else:
                result *= dist.pdf(t0, ctx) * self.pdf_n(n - 1, s, z, i)
            return result

    def learn_n(self, n, s, z, i):
        if n <= 1:
            self._dists[0].inc(s[i], z)
        else:
            dist = self._dists[n - 1]
            (t0, ts) = context(n, s, i)
            ctx = TopicContext(ts, z)
            dist.inc(t0, ctx)
            self.learn_n(n - 1, s, z, i)

    def forget_n(self, n, s, z, i):
        if n <= 1:
            self._dists[0].dec(s[i], z)
        else:
            dist = self._dists[n - 1]
            (t0, ts) = context(n, s, i)
            ctx = TopicContext(ts, z)
            dist.dec(t0, ctx)
            self.forget_n(n - 1, s, z, i)

############################################################

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
