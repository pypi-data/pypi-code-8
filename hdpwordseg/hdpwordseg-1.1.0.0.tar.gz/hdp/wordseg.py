#!/usr/bin/env pypy
#-*- coding: utf-8 -*-

import copy
import random
import math
from collections import *

############################################################

def coorcmp((x1, y1), (x2, y2)):
    len1 = y1 - y2
    len2 = (y1 - x1) - (y2 - x2)
    if len2 != 0: return len2
    if len1 != 0: return len1
    return len2

class WordLattice(object):

    def __init__(self, text, segments=None, atoms=None):
        if segments is None: segments = set()
        if atoms is None: atoms = set()
        self._text = text
        self._segments = segments
        self._atoms = atoms

    def __copy__(self):
        return WordLattice(
            self._text, copy.copy(self._segments),
            copy.copy(self._atoms)
        )

    def get_text(self, x, y=None):
        if x is None: return None
        elif y is None: return self._text[x]
        else: return ''.join(self._text[x : y])

    def get_ctx(self, ctxlen, x, y):
        lctx = ''.join(self._text[x - ctxlen : x])
        rctx = ''.join(self._text[y + 1 : y + ctxlen + 1])
        return (lctx, rctx)

    def addseg(self, x, y):
        if not self.crossatom(x, y) and (x, y) not in self._atoms:
            self._segments.add((x, y))

    def delseg(self, x, y):
        if (x, y) in self._segments:
            self._segments.remove((x, y))

    def addatom(self, x, y):
        self._atoms.add((x, y))

    def crossatom(self, x, y):
        for (x1, y1) in self._atoms:
            if x1 < x and y <= y1: return True
            if x1 <= x and y < y1: return True
            if x1 < x and x < y1 and y1 < y: return True
            if x < x1 and x1 < y and y < y1: return True
        return False

    def crossseg(self, segments, x, y):
        for (x1, y1) in segments:
            if x1 < x and y <= y1: return True
            if x1 <= x and y < y1: return True
            if x1 < x and x < y1 and y1 < y: return True
            if x < x1 and x1 < y and y < y1: return True
        return False

    def exists(self, x, y):
        return (x, y) in self._segments

    def valid(self, x, y):
        return not self.exists(x, y) and not self.crossatom(x, y)

    def repr(self):
        result = '<<WORD LATTICE>>'
        result += '\nText: \"%s\"' % self._text
        pos = self._atoms.keys() + self._segments.keys()
        for (x, y) in sorted(pos, cmp=coorcmp):
            if (x, y) in self._atoms:
                result += '\n  * (%d, %d): \"%s\"' % (
                    x, y, self.get_text(x, y)
                )
            if (x, y) in self._segments:
                result += '\n    (%d, %d): \"%s\"' % (
                    x, y, self.get_text(x, y)
                )
        return result

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def __iter__(self):
        for (x, y) in sorted(self._atoms, cmp=coorcmp):
            yield (x, y)
        for (x, y) in sorted(self._segments, cmp=coorcmp):
            yield (x, y)

    def isatom(self, x, y):
        return (x, y) in self._atoms

    def __contains__(self, (x, y)):
        return (x, y) in self._atoms \
            or (x, y) in self._segments

    def atoms(self):
        return sorted(self._atoms)

    def segments(self):
        return sorted(self._segments)

    def __len__(self):
        return len(self._text)

    def __getitem__(self, i):
        return self._text[i]

    def __getslice__(self, x, y):
        return self._text[x : y]

    def enumsegs(self, maxlen=None, wordfn=None, atom=False):
        if maxlen is None: maxlen = len(self._text)
        for l in xrange(1, maxlen + 1):
            for x in xrange(len(self._text) - l + 1):
                y = x + l
                t0 = self.get_text(x, y)
                if atom:
                    if wordfn is not None and wordfn(t0):
                        self.addatom(x, y)
                else:
                    if wordfn is not None and wordfn(t0):
                        self.addseg(x, y)

    def fillupsegs(self, maxlen=None):
        if maxlen is None: maxlen = len(self._text)
        segments = sorted(
            self._segments.union(self._atoms),
            cmp=coorcmp, reverse=True
        )
        for l in xrange(maxlen, 0, -1):
            for x in xrange(len(self._text) - l + 1):
                y = x + l
                if (x, y) in segments: continue
                if not self.crossseg(segments, x, y):
                    self.addseg(x, y)

    def unigrams(self, y):
        if y is not None and y > 0:
            for x in xrange(y - 1, -1, -1):
                if self.crossatom(x, y): continue
                if (x, y) in self: yield x
        else: yield None

    def bigrams(self, x, y):
        if (x, y) in self:
            if x > 0:
                for k in self.unigrams(x):
                    yield k
            else: yield None

    def trigrams(self, x, y):
        if (x, y) in self:
            for k1 in self.bigrams(x, y):
                if k1 is not None:
                    for k2 in self.unigrams(k1):
                        yield (k2, k1)
                else: yield (None, None)

############################################################

class ProbWordLattice(WordLattice):

    _beamsize = 10

    def __init__(
        self, text,
        segments=None, atoms=None, samples=None, dist=None,
        fwdbwd=False, totaldist=None, idx=None
    ):
        if samples is None: samples = set()
        if dist is None: dist = {}
        if totaldist is None: totaldist = {}
        WordLattice.__init__(self, text, segments, atoms)
        self._samples = samples
        self._dist = dist
        self._fwdbwd = fwdbwd
        self._totaldist = totaldist
        self._idx = idx
        self._n = 0.0

    def __copy__(self):
        return ProbWordLattice(
            self._text, copy.copy(self._segments),
            copy.copy(self._atoms), copy.copy(self._samples),
            copy.copy(self._dist), self._fwdbwd,
            self._totaldist, self._idx
        )

    @staticmethod
    def setbeam(size):
        ProbWordLattice._beamsize = size

    def addsample(self, x, y):
        self._samples.add((x, y))

    def clearsamples(self):
        self._samples.clear()

    def repr(self):
        result = '<<PROB WORD LATTICE>>'
        result += '\nText: \"%s\"' % self._text
        pos = self._atoms.keys() + self._segments.keys()
        for (x, y) in sorted(pos, cmp=coorcmp):
            if (x, y) in self._samples:
                result += '\n  # (%d, %d): \"%s\"' % (
                    x, y, self.get_text(x, y)
                )
            elif (x, y) in self._atoms:
                result += '\n  * (%d, %d): \"%s\"' % (
                    x, y, self.get_text(x, y)
                )
            elif (x, y) in self._segments:
                result += '\n    (%d, %d): \"%s\"' % (
                    x, y, self.get_text(x, y)
                )
            if (x, y) in self._dist:
                result += ' (pred: %e)' % self._dist[(x, y)]
        if len(self._samples) > 0:
            result += '\nSentence: \"%s\"' % '|'.join(self.getsent())
        return result

    def getprob(self, x, y):
        if (x, y) in self._dist:
            return self._dist[(x, y)]
        else:
            return 0.0

    def setprob(self, x, y, v):
        if v > 0.0:
            self._dist[(x, y)] = v
        elif (x, y) in self._dist:
            del self._dist[(x, y)]

    def addprob(self, x, y, v):
        v1 = v + self.getprob(x, y)
        self.setprob(x, y, v1)

    def genkey(self, idx, x, y):
        return self.get_text(x, y)

    def normtotal(self):
        if type(self._totaldist) is dict:
            for k in self._totaldist:
                self._totaldist[k] /= self._n
        else:
            self._totaldist.normalize(self._n)

    def cleardist(self):
        self._dist.clear()

    def pdf(self, x, y):
        return 1.0

    def fwdfilter(self, fn=None):
        if fn is None:
            fn = lambda x, y: self.pdf(x, y)
        self.cleardist()
        for y in xrange(1, len(self._text) + 1):
            for x in self.unigrams(y):
                p = fn(x, y)
                if self._fwdbwd and x > 0:
                    expc = 0.0
                    for k in self.unigrams(x):
                        expc += self.getprob(k, x)
                    p *= expc
                self.setprob(x, y, p)

    def bwdsample(self, y, fn=None, temp=0.0):
        if y == 0: return
        if y == len(self._text):
            self.clearsamples()
        if fn is None:
            fn = lambda x, y: self.getprob(x, y)

        def fn1(x, y):
            if temp == 0.0:
                return fn(x, y)
            else:
                return fn(x, y) ** (10.0 ** (-1.0 * temp))

        while y > 0:
            xs = [(x, fn1(x, y)) for x in self.unigrams(y)]
            if len(xs) > 0:
                (x, i) = ProbWordLattice.choose(xs)
                self.addsample(x, y)
                y = x
            else: raise DeadEndException()
        self.cleardist()

    def run(self, temp=0.0):
        self.fwdfilter()
        self.bwdsample(len(self._text), temp=temp)

    @staticmethod
    def choose(xs):
        assert len(xs) > 0
        choices = []
        cdf = 0.0
        for (x, p) in xs:
            cdf += p
            choices.append((cdf, x))
        r = random.random() * cdf
        i = 0
        while i < len(choices):
            (cdf, c) = choices[i]
            if cdf >= r: return (c, i)
            i += 1

    def random(self):
        fn = lambda x, y: 1.0 / (y - x + 1.0)
        if self._fwdbwd:
            self.fwdfilter(fn)
            self.bwdsample(len(self._text))
        else:
            self.bwdsample(len(self._text), fn)

    def getsamples(self):
        return self._samples

    def setsamples(self, samples):
        self.clearsamples()
        for (x, y) in samples:
            self.addsample(x, y)

    def getsent(self):
        segs = []
        for (x, y) in sorted(self.getsamples()):
            t = self.get_text(x, y)
            segs.append(t)
        return segs

    def pdf_samples(self, samples):
        result = 1.0
        for (x, y) in samples:
            result *= self.pdf(x, y)
        return result

#     def decode(self):
#         # Viterbi algorithm
#         tbl = self.fwd_decode()
#         self.bwd_decode(tbl)
# 
#     def fwd_decode(self):
#         tbl = {}
#         for y in xrange(1, len(self._text) + 1):
#             tbl[y] = {}
#             for x in self.unigrams(y):
#                 key = self.genkey(self._idx, x, y)
#                 p = math.log(self._totaldist[key])
#                 if x > 0:
#                     choices = []
#                     for k in self.unigrams(x):
#                         (p1, k1) = tbl[x][k]
#                         choices.append((p1, k))
#                     choices.sort(reverse=True)
#                     if len(choices) > 0:
#                         (p1, k) = choices[0]
#                         tbl[y][x] = (p + p1, k)
#                 else: tbl[y][x] = (p, None)
#         return tbl
# 
#     def bwd_decode(self, tbl):
#         self.clearsamples()
#         y = len(self._text)
#         while y is not None and y > 0 and y in tbl:
#             choices = []
#             for x in tbl[y]:
#                 choices.append((tbl[y][x], x))
#             choices.sort(reverse=True)
#             if len(choices) == 0: break
#             (p, x) = choices[0]
#             self.addsample(x, y)
#             y = x

class DeadEndException(Exception):

    pass

############################################################

def context(n, s, i):
    result = []
    for k in xrange(i - 1, i - n, -1):
        if k >= 0:
            result.append(s[k])
        else:
            result.append(None)
    return (s[i], tuple(result))

class Context(namedtuple('Context', ['ts'])):
    
    def __repr__(self):
        return '<%s>' % ', '.join('%s' % s for s in self.ts)

class TopicContext(namedtuple('TopicContext', ['ts', 'z'])):

    def __repr__(self):
        if len(self.ts) > 0:
            return '<%s | %s>' % (
                ', '.join('%s' % s for s in self.ts), self.z
            )
        else:
            return '<%s>' % self.z

############################################################

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
