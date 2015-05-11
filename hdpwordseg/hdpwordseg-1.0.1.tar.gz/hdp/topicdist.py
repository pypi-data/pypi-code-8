#!/usr/bin/env pypy
#-*- coding: utf-8 -*-

import copy
import math
import random

from prob import *

############################################################

class TopicDist(CRP):

    def __init__(
        self, maxtopics, alpha, theta, 
        tbl=None, total=None, consqs=None, disk=None
    ):
        assert maxtopics > 0
        super(TopicDist, self).__init__(
            alpha, theta, tbl, total, consqs, disk
        )
        self._maxtopics = maxtopics

    def __copy__(self):
        return TopicDist(
            self._maxtopics, self._alpha, self._theta,
            copy.deepcopy(self._tbl), copy.copy(self._total),
            copy.copy(self._consqs)
        )

    def get_maxtopics(self):
        return self._maxtopics

    def inc(self, s, p=None):
        if s < 0 or s >= self._maxtopics: return
        super(TopicDist, self).inc(s, p)

    def dec(self, s, p=None):
        if s < 0 or s >= self._maxtopics: return
        super(TopicDist, self).dec(s, p)

    def pdf(self, s, p=None):
        denom = self.total(p) + self._theta
        if s < 0 or s >= self._maxtopics:
            num = 0.0
        elif p in self._consqs and s in self._consqs[p] \
                and self.freq(s, p) > 0.0:
            num = self.freq(s, p) - self._alpha
        else:
            num = self._theta + self._alpha * self.notbls(p)
        return num / denom

    def random(self, sent, p=None):
        choices = []
        cdf = 0.0
        for s in xrange(self._maxtopics):
            q = self.pdf(s, p)
            cdf += q
            choices.append((cdf, s))
        r = random.random() * cdf
        i = 0
        while i < len(choices):
            (cdf, c) = choices[i]
            if cdf >= r: return c
            i += 1
        return random.randint(0, self._maxtopics - 1)

    def sample_hparams(self):
        pass

############################################################

class TopicLDA(object):

    def __init__(
        self, maxtopics, alpha, theta, unidist,
        topratio=None, wtopratio=None
    ):
        if topratio is None: topratio = CRP(alpha, theta)
        if wtopratio is None: wtopratio = CRP(alpha, theta)
        self._maxtopics = maxtopics
        self._alpha = alpha
        self._theta = theta
        self._unidist = unidist
        self._topratio = topratio
        self._wtopratio = wtopratio
        # self.sample_hparams()

    def __copy__(self):
        return TopicLDA(
            self._maxtopics, self._alpha, self._theta, self._unidist,
            copy.copy(self._topratio), copy.copy(self._wtopratio)
        )

    def get_maxtopics(self):
        return self._maxtopics

    def inc(self, s, p=None):
        pass

    def dec(self, s, p=None):
        pass

    def pdf(self, sent, z):
        result = 1.0
        for w in sent:
            result *= self._topratio.freq(z) \
                * self._wtopratio.freq((w, z))
        return result

    def random(self, sent):
        choices = []
        cdf = 0.0
        for z in xrange(self._maxtopics):
            cdf += self.pdf(sent, z)
            choices.append((cdf, z))
        r = random.random() * cdf
        i = 0
        while i < len(choices):
            (cdf, c) = choices[i]
            if cdf >= r: return c
            i += 1
        return 0

    def sample_hparams(self):
        self.sample_topratio()
        self.sample_wtopratio()

    def sample_topratio(self):
        self._topratio.clear()
        vs = []
        total = 0.0
        for z in xrange(self._maxtopics):
            vk = self._unidist.total(z) + self._alpha + 0.1
            v = random.gammavariate(vk, 1)
            vs.append(vk)
            total += v
        for z in xrange(self._maxtopics):
            self._topratio.inc(z, vs[z] / total)

    def sample_wtopratio(self):
        self._wtopratio.clear()
        total = 0.0
        vs = {}
        for z in xrange(self._maxtopics):
            if z in self._unidist.prems():
                vs[z] = {}
                for w in self._unidist.consqs(z):
                    vk = self._unidist.freq(w, z) + self._alpha + 0.1
                    v = random.gammavariate(vk, 1)
                    vs[z][w] = v
                    total += v
        for z in vs:
            for w in vs[z]:
                self._wtopratio.inc(vs[z][w] / total)

############################################################

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
