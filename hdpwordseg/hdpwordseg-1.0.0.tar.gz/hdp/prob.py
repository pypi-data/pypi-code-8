#!/usr/bin/env pypy
#-*- coding: utf-8 -*-

import copy
import math
import random

import os, sys
import pickle, cPickle
import shelve

############################################################

class Histogram(object):
    
    def __init__(self, tbl=None, total=None, consqs=None, disk=None):
        if disk is not None and tbl is None:
            self._fname_tbl = disk + '.table'
            tbl = shelve.open(
                self._fname_tbl, protocol=pickle.HIGHEST_PROTOCOL
            )
        else:
            self._fname_tbl = None
            if tbl is None: tbl = {}
        if disk is not None and total is None:
            self._fname_total = disk + '.total'
            total = shelve.open(
                self._fname_total, protocol=pickle.HIGHEST_PROTOCOL
            )
        else:
            self._fname_total = None
            if total is None: total = {}
        if consqs is None: consqs = {}
        self._tbl = tbl
        self._total = total
        self._consqs = consqs
        self._disk = disk

    def __copy__(self):
        return Histogram(
            copy.deepcopy(self._tbl), copy.copy(self._total),
            copy.copy(self._consqs), self._disk
        )

    def indexstr(self, p, s):
        if self._disk is not None:
            return ('%s__%s' % (p, s)).encode('utf-8')
        else:
            return (p, s)

    def indextotal(self, p):
        if self._disk is not None:
            return ('%s' % (p,)).encode('utf-8')
        else:
            return p

    def close(self):
        if self._disk is not None:
            self._tbl.close()
            self._total.close()
            if self._fname_tbl is not None:
                os.remove(self._fname_tbl)
            if self._fname_total is not None:
                os.remove(self._fname_total)

    def prems(self):
        return self._total.keys()

    def consqs(self, p=None):
        return self._consqs[p]

    def contains(self, s, p=None):
        return p in self._consqs and s in self._consqs[p]

    def inc(self, s, p=None, v=1.0):
        if p not in self._consqs:
            self._consqs[p] = set()
        self._consqs[p].add(s)
        q = self.indexstr(p, s)
        if q not in self._tbl:
            self._tbl[q] = 0.0
        r = self.indextotal(p)
        if r not in self._total:
            self._total[r] = 0.0
        self._tbl[q] = self._tbl[q] + v
        self._total[r] = self._total[r] + v

    def dec(self, s, p=None, v=1.0):
        if p in self._consqs:
            if s in self._consqs[p]:
                q = self.indexstr(p, s)
                if self._tbl[q] > 0.0:
                    self._tbl[q] = self._tbl[q] - v
                    if self._tbl[q] == 0.0:
                        del self._tbl[q]
                        self._consqs[p].remove(s)
                        if len(self._consqs[p]) == 0:
                            del self._consqs[p]
                r = self.indextotal(p)
                if r in self._total:
                    self._total[r] = self._total[r] - v
                    if self._total[r] == 0.0:
                        del self._total[r]
        
    def freq(self, s, p=None):
        if p in self._consqs and s in self._consqs[p]:
            q = self.indexstr(p, s)
            return self._tbl[q]
        else:
            return 0.0

    def total(self, p=None):
        if p in self._consqs:
            r = self.indextotal(p)
            return self._total[r]
        else:
            return 0.0

    def clear(self):
        self._tbl.clear()
        self._total.clear()
        self._consqs.clear()

    def repr(self):
        result = '<<HISTOGRAM>>'
        singletbl = len(self._consqs) == 1
        for p in sorted(self._consqs):
            for s in sorted(self._consqs[p]):
                if p is None and singletbl:
                    result += '\n  p(%s) = %f' % (s, self.freq(s, p))
                else:
                    result += '\n  p(%s|%s) = %f' % (s, p, self.freq(s, p))
        for p in sorted(self._consqs):
            if p is None and singletbl:
                result += '\ntotal = %f' % self.total(p)
            else:
                result += '\n  #(%s) = %f' % (p, self.total(p))
        return result

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def pdf(self, s, p=None):
        return self.freq(s, p) / self.total(p)

    def random(self, p=None):
        if p not in self._consqs: return None
        choices = []
        cdf = 0.0
        for s in self._consqs[p]:
            q = self.pdf(s, p)
            cdf += q
            choices.append((cdf, s))
        r = random.random() * cdf
        i = 0
        while i < len(choices):
            (cdf, c) = choices[i]
            if cdf >= r: return c
            i += 1
        return None

############################################################

class CRP(Histogram):
    
    def __init__(
        self, alpha, theta,
        tbl=None, total=None, consqs=None, disk=None
    ):
        assert 0.0 <= alpha < 1.0
        assert theta > 0.0
        super(CRP, self).__init__(tbl, total, consqs, disk)
        self._alpha = alpha
        self._theta = theta

    def __copy__(self):
        return CRP(
            self._alpha, self._theta, 
            copy.deepcopy(self._tbl), copy.copy(self._total),
            copy.copy(self._consqs), self._disk
        )

    def repr(self):
        result = '<<CHINESE RESTAURANT PROCESS>>'
        result += '\nalpha = %f' % self._alpha
        result += '\ntheta = %f' % self._theta
        singletbl = len(self._consqs) == 1
        for p in self._consqs:
            for s in self._consqs[p]:
                if p is None and singletbl:
                    result += '\n  p(%s) = %f' % (s, self.freq(s, p))
                else:
                    result += '\n  p(%s|%s) = %f' % (s, p, self.freq(s, p))
        for p in self._consqs:
            if p is None and singletbl:
                result += '\ntotal = %f' % self.total(p)
            else:
                result += '\n  #(%s) = %f' % (p, self.total(p))
        return result

    def notbls(self, p=None):
        if p in self._consqs:
            return float(len(self._consqs[p]))
        else:
            return 0.0

    def pdf(self, s, p=None):
        denom = self.total(p) + self._theta
        if self.contains(s, p) and self.freq(s, p) > 0.0:
            num = self.freq(s, p) - self._alpha
        else:
            num = self._theta + self._alpha * self.notbls(p)
        return num / denom

    def sample_hparams(self):
        # alpha ~ Beta(0.5, 0.5), whose pdf is U-shaped
        if self._alpha != 0.0:
            r = 0.0
            while r == 0.0:
                r = random.betavariate(0.5, 0.5)
            self._alpha = r
        # theta ~ Gamma(1, 1), whose pdf is an exponential decay
        self._theta = random.gammavariate(1, 1)

    def get_alpha(self):
        return self._alpha

    def get_theta(self):
        return self._theta

    def random(self, p=None):
        if p not in self._consqs: return None
        choices = []
        cdf = 0.0
        for s in self._consqs[p]:
            q = self.pdf(s, p)
            cdf += q
            choices.append((cdf, s))
        r = random.random()
        i = 0
        while i < len(choices):
            (cdf, c) = choices[i]
            if cdf >= r: return c
        return None

############################################################

class Poisson:

    def __init__(self):
        self._mean = random.gammavariate(0.2, 0.1)

    def repr(self):
        result = '<<POISSON REGULATOR>>'
        result += '\nmean = %f' % self._mean
        return result

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def pdf(self, wordlen):
        return math.exp(-1.0 * self._mean) \
            * (self._mean ** wordlen) / gamma(wordlen + 1)

    def get_mean(self):
        return self._mean

    def set_mean(self, mean):
        self._mean = mean

    def sample_hparams(self, hist):
        a, b = 0.0, 0.0
        for p in hist._consqs:
            for s in hist._consqs[p]:
                q = hist.indexstr(p, s)
                a += hist._tbl[q] * len(s)
                b += hist._tbl[q]
        r = random.gammavariate(0.2 + a/b, 1.0)
        # r = random.gammavariate(a/b, 1.0)
        self._mean = r

############################################################

class IdxTable:

    def __init__(self, disk, defval=0.0):
        self._disk = disk
        self._fname_tbl = disk + '.index'
        self._tbl = shelve.open(
            self._fname_tbl, protocol=pickle.HIGHEST_PROTOCOL
        )
        self._defval = defval
        self._smallest = defval

    def __copy__(self):
        return ViterbiTable(self._disk, self._defval)

    def index(self, idx):
        if idx is None:
            return '*NONE*'
        if type(idx) is str:
            return '1;%s' % idx
        elif type(idx) is tuple or type(idx) is list:
            return '%d;%s' % (len(idx), ';'.join('%s' % s for s in idx))
        else:
            return '1;%s' % idx
        # return cPickle.dumps(idx, cPickle.HIGHEST_PROTOCOL)

    def close(self):
        self._tbl.close()
        os.remove(self._fname_tbl)

    def __contains__(self, idx):
        k = self.index(idx)
        return k in self._tbl

    def normalize(self, n):
        for k in self._tbl:
            self._tbl[k] = self._tbl[k] / n

    def __getitem__(self, idx):
        k = self.index(idx)
        if k not in self._tbl:
            return self._defval
        elif self._tbl[k] == 0.0:
            return self._smallest * 0.1
        else:
            return self._tbl[k]

    def __setitem__(self, idx, val):
        k = self.index(idx)
        self._tbl[k] = val

    def acc(self, idx, val):
        k = self.index(idx)
        self._tbl[k] += val
        if 0.0 < abs(val) < self._smallest:
            self._smallest = abs(val)

    def __delitem__(self, idx):
        k = self.index(idx)
        if k in self._tbl:
            del self._tbl[k]

############################################################

def digamma(x):
    assert x > 0
    result = 0
    while x < 7:
        result -= 1.0 / x
        x += 1
    x -= 0.5
    xx = 1.0 / x
    xx2 = xx * xx
    xx4 = xx2 * xx2
    result += math.log(x) \
        + (1.0/24.0) * xx2 \
        - (7.0 / 960.0) * xx4 \
        + (31.0 / 8064.0) * xx4 * xx2 \
        - (127.0 / 30720.0) * xx4 * xx4
    return result

_gamma_a =    ( 1.00000000000000000000, 0.57721566490153286061, -0.65587807152025388108,
         -0.04200263503409523553, 0.16653861138229148950, -0.04219773455554433675,
         -0.00962197152787697356, 0.00721894324666309954, -0.00116516759185906511,
         -0.00021524167411495097, 0.00012805028238811619, -0.00002013485478078824,
         -0.00000125049348214267, 0.00000113302723198170, -0.00000020563384169776,
          0.00000000611609510448, 0.00000000500200764447, -0.00000000118127457049,
          0.00000000010434267117, 0.00000000000778226344, -0.00000000000369680562,
          0.00000000000051003703, -0.00000000000002058326, -0.00000000000000534812,
          0.00000000000000122678, -0.00000000000000011813, 0.00000000000000000119,
          0.00000000000000000141, -0.00000000000000000023, 0.00000000000000000002
       )
def gamma (x): 
   y  = float(x) - 1.0
   sm = _gamma_a[-1]
   for an in _gamma_a[-2::-1]:
      sm = sm * y + an
   return 1.0 / sm

############################################################

def nlargest(n, choices):
    choices.sort(reverse=True)
    return choices[:n]

############################################################

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
