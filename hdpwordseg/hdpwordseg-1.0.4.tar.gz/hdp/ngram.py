#!/usr/bin/env pypy
#-*- coding: utf-8 -*-

import os, sys
from collections import *
import tempfile

from prob import *
from wordseg import *
from strdist import *

############################################################

class Unigram(ProbWordLattice):

    def __init__(
        self, text, strdist, unidist,
        segments=None, atoms=None, samples=None, dist=None,
        fwdbwd=False, poisreg=None, totaldist=None, idx=None
    ):
        super(Unigram, self).__init__(
            text, 
            segments, atoms, samples, dist, fwdbwd,
            totaldist=totaldist, idx=idx
        )
        self._strdist = strdist
        self._unidist = unidist
        self._poisreg = poisreg

    def __copy__(self):
        return Unigram(
            self._text,
            copy.copy(self._strdist), copy.copy(self._unidist),
            copy.copy(self._segments), copy.copy(self._atoms), 
            copy.copy(self._samples), copy.copy(self._dist),
            self._fwdbwd, self._poisreg,
            totaldist=self._totaldist, idx=self._idx
        )

    def genkey_uni(self, idx, x, y):
        return self.get_text(x, y)

    def pdf(self, x, y):
        t0 = self.get_text(x, y)
        p = self.pdf_uni(t0)
        return p

    def pdf_uni(self, t0):
        p = self._unidist.pdf(t0)
        if self._unidist.contains(t0):
            return p
        else:
            return p * self.basepdf(t0)

    def basepdf(self, t0):
        result = self._strdist.pdf(t0)
        if self._poisreg:
            result *= self._poisreg.pdf(len(t0))
        return result

    def forget(self, sent):
        for i in xrange(len(sent)):
            t0 = sent[i]
            self._strdist.forget(t0)
            self._unidist.dec(t0)

    def learn(self, sent):
        for i in xrange(len(sent)):
            t0 = sent[i]
            self._strdist.learn(t0)
            self._unidist.inc(t0)

    def enumkeys_uni(self, keys):
        for y in xrange(1, len(self._text) + 1):
            for x in self.unigrams(y):
                key = self.genkey_uni(self._idx, x, y)
                keys.add(key)

############################################################

class Bigram(Unigram):

    def __init__(
        self, text, strdist, unidist, bidist,
        segments=None, atoms=None, samples=None, dist=None,
        fwdbwd=False, poisreg=None, totaldist=None, idx=None
    ):
        super(Bigram, self).__init__(
            text, strdist, unidist,
            segments, atoms, samples, dist, fwdbwd, poisreg,
            totaldist=totaldist, idx=idx
        )
        self._bidist = bidist

    def __copy__(self):
        return Bigram(
            self._text, copy.copy(self._strdist),
            copy.copy(self._unidist), copy.copy(self._bidist),
            copy.copy(self._segments), copy.copy(self._atoms), 
            copy.copy(self._samples), copy.copy(self._dist),
            self._fwdbwd, self._poisreg,
            totaldist=self._totaldist, idx=self._idx
        )

    def pdf(self, x, y):
        t0 = self.get_text(x, y)
        p = 0.0
        for k1 in self.bigrams(x, y):
            if k1 is None: t1 = None
            else: t1 = self.get_text(k1, x)
            p += self.pdf_bi(t0, t1)
        return p

    def pdf_bi(self, t0, t1):
        p = self._bidist.pdf(t0, t1)
        if self._bidist.contains(t0, t1):
            return p
        else:
            return p * self.pdf_uni(t0)

    def forget(self, sent):
        super(Bigram, self).forget(sent)
        for i in xrange(len(sent)):
            t0 = sent[i]
            if i > 0: t1 = sent[i - 1]
            else: t1 = None
            self._bidist.dec(t0, t1)

    def learn(self, sent):
        super(Bigram, self).learn(sent)
        for i in xrange(len(sent)):
            t0 = sent[i]
            if i > 0: t1 = sent[i - 1]
            else: t1 = None
            self._bidist.inc(t0, t1)

    def genkey_bi(self, idx, k, x, y):
        t0 = self.get_text(x, y)
        t1 = self.get_text(k, x)
        return (t0, t1)

    def enumkeys_bi(self, keys):
        for y in xrange(1, len(self._text) + 1):
            for x in self.unigrams(y):
                if x > 0:
                    for k in self.unigrams(x):
                        key = self.genkey_bi(self._idx, k, x, y)
                        keys.add(key)

    def fwd_decode(self):
        tbl = {}
        for y in xrange(1, len(self._text) + 1):
            tbl[y] = {}
            for x in self.unigrams(y):
                if x > 0:
                    choices = []
                    for k in self.unigrams(x):
                        key = self.genkey_bi(self._idx, k, x, y)
                        p = math.log(self._totaldist[key])
                        (p1, k1) = tbl[x][k]
                        choices.append((p + p1, k))
                    choices.sort(reverse=True)
                    if len(choices) > 0:
                        (p1, k) = choices[0]
                        tbl[y][x] = (p1, k)
                else:
                    key = self.genkey_uni(self._idx, x, y)
                    p = math.log(self._totaldist[key])
                    tbl[y][x] = (p, None)
        return tbl

############################################################

class Trigram(Bigram):

    def __init__(
        self, text, strdist, unidist, bidist, tridist,
        segments=None, atoms=None, samples=None, dist=None,
        fwdbwd=False, poisreg=None, totaldist=None, idx=None
    ):
        super(Trigram, self).__init__(
            text, strdist, unidist, bidist,
            segments, atoms, samples, dist, fwdbwd, poisreg,
            totaldist=totaldist, idx=idx
        )
        self._tridist = tridist

    def __copy__(self):
        return Bigram(
            self._text, copy.copy(self._strdist),
            copy.copy(self._unidist), copy.copy(self._bidist),
            copy.copy(self._tridist),
            copy.copy(self._segments), copy.copy(self._atoms), 
            copy.copy(self._samples), copy.copy(self._dist),
            self._fwdbwd, self._poisreg,
            totaldist=self._totaldist, idx=self._idx
        )

    def pdf(self, x, y):
        t0 = self.get_text(x, y)
        p = 0.0
        for (k2, k1) in self.trigrams(x, y):
            if k1 is None: t1 = None
            else: t1 = self.get_text(k1, x)
            if k2 is None: t2 = None
            else: t2 = self.get_text(k2, k1)
            p += self.pdf_tri(t0, t1, t2)
        return p

    def pdf_tri(self, t0, t1, t2):
        ctx = Context((t1, t2))
        p = self._tridist.pdf(t0, ctx)
        if self._tridist.contains(t0, ctx):
            return p
        else:
            return p * self.pdf_bi(t0, t1)

    def forget(self, sent):
        super(Trigram, self).forget(sent)
        for i in xrange(len(sent)):
            t0 = sent[i]
            if i > 1: t2 = sent[i - 2]
            else: t2 = None
            if i > 0: t1 = sent[i - 1]
            else: t1 = None
            ctx = Context((t1, t2))
            self._tridist.dec(t0, ctx)

    def learn(self, sent):
        super(Trigram, self).learn(sent)
        for i in xrange(len(sent)):
            t0 = sent[i]
            if i > 1: t2 = sent[i - 2]
            else: t2 = None
            if i > 0: t1 = sent[i - 1]
            else: t1 = None
            ctx = Context((t1, t2))
            self._tridist.inc(t0, ctx)

    def genkey_tri(self, idx, k2, k1, x, y):
        t0 = self.get_text(x, y)
        t1 = self.get_text(k1, x)
        t2 = self.get_text(k2, k1)
        return (t0, t1, t2)

    def enumkeys_tri(self, keys):
        for y in xrange(1, len(self._text) + 1):
            for x in self.unigrams(y):
                if x > 1:
                    for k1 in self.unigrams(x):
                        if k1 is None: continue
                        for k2 in self.unigrams(k1):
                            if k2 is None: continue
                            key = self.genkey_tri(self._idx, k2, k1, x, y)
                            keys.add(key)

    def fwd_decode(self):
        tbl = {}
        for y in xrange(1, len(self._text) + 1):
            tbl[y] = {}
            for x in self.unigrams(y):
                if x > 1:
                    choices = []
                    for k1 in self.unigrams(x):
                        if k1 is None: continue
                        for k2 in self.unigrams(k1):
                            if k2 is None: continue
                            key = self.genkey_tri(self._idx, k2, k1, x, y)
                            p = math.log(self._totaldist[key])
                            (p1, _) = tbl[x][k1]
                            (p2, _) = tbl[k1][k2]
                            choices.append((p + p1 + p2, (k1, k2)))
                    choices.sort(reverse=True)
                    if len(choices) > 0:
                        (p1, (k1, k2)) = choices[0]
                        tbl[y][x] = (p1, (k1, k2))
                elif x > 0:
                    choices = []
                    for k in self.bigrams(x, y):
                        key = self.genkey_bi(self._idx, k, x, y)
                        p = math.log(self._totaldist[key])
                        (p1, _) = tbl[x][k]
                        choices.append((p + p1, (None, (k, None))))
                    choices.sort(reverse=True)
                    if len(choices) > 0:
                        (p1, (k, _)) = choices[0]
                        tbl[y][x] = (p1, (k, None))
                else:
                    key = self.genkey_uni(self._idx, x, y)
                    p = math.log(self._totaldist[key])
                    tbl[y][x] = (p, (None, None))
        return tbl

############################################################

class Wordseg(object):
    # Following Goldwater's (2007) PhD thesis
    
    def __init__(
        self, n, cn, texts, atomfn=None, wordfn=None, 
        maxatomlen=None, maxwordlen=20,
        maxiters=100, burnin=None,
        alpha_char=0.0, alpha_uni=0.0, alpha_bi=0.0, alpha_tri=0.0,
        theta_char=1.0, theta_uni=1.0, theta_bi=1.0, theta_tri=0.0,
        p_stop=None, strdist=None, unidist=None, bidist=None, tridist=None,
        fwdbwd=False, hparamsmp=False, maxtemp=0.0, poisson=False,
        disk=None
    ):
        assert n in [1, 2, 3]
        assert cn >= 1
        if disk is not None:
            disk_uni = disk + '_unigram'
            disk_bi = disk + '_bigram'
            disk_tri = disk + '_trigram'
            disk_total = disk + '_total'
            totaldist = IdxTable(disk_total, defval=1e-6)
        else:
            disk_uni = None
            disk_bi = None
            disk_tri = None
            disk_total = tempfile.mktemp() + '_total'
            totaldist = IdxTable(disk_total, defval=1e-6)
        if maxatomlen is None: maxatomlen = maxwordlen
        if strdist is None:
            strdist = StrDist(cn, alpha_char, theta_char, p_stop=p_stop)
        if unidist is None:
            unidist = CRP(alpha_uni, theta_uni, disk=disk_uni)
        if bidist is None:
            bidist = CRP(alpha_bi, theta_bi, disk=disk_bi)
        if tridist is None:
            tridist = CRP(alpha_tri, theta_tri, disk=disk_tri)
        if burnin == 0.0: burnin = None
        self._n = n
        self._cn = cn
        self._texts = texts
        self._atomfn = atomfn
        self._wordfn = wordfn
        self._maxatomlen = maxatomlen
        self._maxwordlen = maxwordlen
        self._maxiters = maxiters
        self._burnin = burnin
        self._strdist = strdist
        self._unidist = unidist
        self._bidist = bidist
        self._tridist = tridist
        self._fwdbwd = fwdbwd
        self._hparamsmp = hparamsmp
        self._maxtemp = maxtemp
        self._poisson = poisson
        self._lattices = []
        self._itercnt = 0
        self._poisreg = Poisson() if self._poisson else None
        self._verbose = False
        self._debug = False
        self._cnt = 0
        self._temp = maxtemp
        self._disk = disk
        self._totaldist = totaldist
        self._unikeys = set()
        self._bikeys = set()
        self._trikeys = set()

    def close(self):
        self._unidist.close()
        self._bidist.close()
        self._tridist.close()
        if type(self._totaldist) is not dict:
            self._totaldist.close()

    def set_verbose(self, v=True):
        self._verbose = v

    def set_debug(self, v=True):
        self._debug = v

    def repr(self):
        result = '<<GOLDWATER\'S (2006) WORD SEGMENTER>>'
        result += '\n>> CHARDIST: %s' % self._strdist
        result += '\n>> UNIGRAM: %s' % self._unidist
        result += '\n>> BIGRAM: %s' % self._bidist
        result += '\n>> TRIGRAM: %s' % self._tridist
        result += '\n>> POISSON REGULATOR: %s' % self._poisreg
        result += '\n>> LATTICES:'
        for lattice in self._lattices:
            # result += '\n%s' % '|'.join(lattice.getsent())
            result += '\n%s' % lattice
        return result

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()

    def __getitem__(self, index):
        return self._lattices[index]

    def __len__(self):
        return len(self._lattices)

    def __iter__(self):
        for lattice in self._lattices:
            yield lattice

    def __getitem__(self, index):
        return self._lattices[index]

    def build(self):
        if self._verbose:
            sys.stderr.write('  Init: ')
        idx = 0
        for text in self._texts:
            if self._verbose:
                sys.stderr.write('.')
            m = self.build_onetext(text, idx)
            self._lattices.append(m)
            self.collectkeys(m)
            idx += 1
        if self._verbose:
            sys.stderr.write('\n')

    def build_onetext(self, text, idx):
        m = self.buildmodel(text, idx)
        m.enumsegs(maxlen=None, wordfn=self._atomfn, atom=True)
        m.enumsegs(maxlen=None, wordfn=self._wordfn)
        m.fillupsegs(maxlen=self._maxwordlen)
        m.random()
        m.learn(m.getsent())
        return m

    def buildmodel(self, text, idx):
        if self._n == 1:
            m = Unigram(
                text, self._strdist, 
                self._unidist,
                fwdbwd=self._fwdbwd, poisreg=self._poisreg,
                totaldist=self._totaldist, idx=idx
            )
        elif self._n == 2:
            m = Bigram(
                text, self._strdist, 
                self._unidist, self._bidist,
                fwdbwd=self._fwdbwd, poisreg=self._poisreg,
                totaldist=self._totaldist, idx=idx
            )
        elif self._n == 3:
            m = Trigram(
                text, self._strdist, 
                self._unidist, self._bidist, self._tridist,
                fwdbwd=self._fwdbwd, poisreg=self._poisreg,
                totaldist=self._totaldist, idx=idx
            )
        else: raise NotImplemented
        return m

    def collectkeys(self, m):
        if isinstance(m, Trigram):
            m.enumkeys_tri(self._trikeys)
        if isinstance(m, Bigram):
            m.enumkeys_bi(self._bikeys)
        if isinstance(m, Unigram):
            m.enumkeys_uni(self._unikeys)

    def run(self):
        if self._debug:
            q = '<<INITIALIZATION>>'
            q += '\n\n%s' % self
            sys.stderr.write(q.encode('utf-8'))
            sys.stderr.flush()
        step = self._maxtemp / (len(self._texts) * self._maxiters - 1.0)
        n = 0.0
        for x in xrange(self._maxiters):
            self.run_oneloop(x, step)
            if self._burnin is None or x < self._burnin:
                tail = 'BURN-IN'
            else:
                tail = 'MH-SAMPLING'
            if self._burnin is None or (
                self._burnin is not None and x >= self._burnin
            ):
                self.sample_hparams()
                n += 1.0
                self.acctotal()
            if self._debug:
                q = '\n\n<<ITERATION %d: %s>>' % (x + 1, tail)
                q += '\n>> Temperature: %f' % self._temp
                q += '\n\n%s' % self
                sys.stderr.write(q.encode('utf-8'))
                sys.stderr.flush()
        self.normtotal(n)
        self.run_decoder()
        if self._verbose:
            sys.stderr.write('\n')

    def acc(self, key, val):
        self._totaldist.acc(key, val)

    def acctotal(self):
        for t0 in self._unikeys:
            key = t0
            self.acc(key, self._unidist.pdf(t0))
        for (t0, t1) in self._bikeys:
            key = (t1, t0)
            self.acc(key, self._bidist.pdf(t0, t1))
        for (t0, t1, t2) in self._trikeys:
            key = (t0, t1, t2)
            ctx = Context((t1, t2))
            self.acc(key, self._tridist.pdf(t0, ctx))

    def normtotal(self, n):
        if type(self._totaldist) is dict:
            for k in self._totaldist:
                self._totaldist[k] /= n
        else:
            self._totaldist.normalize(n)

    def run_oneloop(self, x, step):
        if self._verbose:
            sys.stderr.write('%6d: ' % (x + 1))
        for i in xrange(len(self._lattices)):
            self._cnt += 1
            if self._burnin is None or x < self._burnin:
                tail = 'BURN-IN'
                self.gibbs(i, self._temp)
                acc = False
            else:
                tail = 'MH-SAMPLING'
                acc = self.mh(i, self._temp)
            if self._verbose:
                if self._burnin is None or x < self._burnin:
                    sys.stderr.write('.')
                elif acc:
                    sys.stderr.write('+')
                else:
                    sys.stderr.write('-')
                sys.stderr.flush()
            m = self._lattices[i]
            if self._temp > 0.0: self._temp -= step
            else: self._temp = 0.0
        if self._verbose:
            sys.stderr.write('\n')

    def gibbs(self, i, temp):
        # sentence-level blocked Gibbs sampler
        m = self._lattices[i]
        m.forget(m.getsent())
        m.run(temp)
        m.learn(m.getsent())

    def mh(self, i, temp):
        # Metropolis-Hasting algorithm
        m = self._lattices[i]
        (
            p_old, p_new, samples_old, samples_new, sent_old, sent_new
        ) = self.mh_transition(temp, m)
        if p_new > 0.0:
            acc = p_old / p_new
        else: acc = None
        if acc is not None and acc < 1:
            r = random.random()
            if r < acc:
                m.forget(sent_old)
                m.learn(sent_new)
                m.setsamples(samples_new)
                return True
        return False

    def mh_transition(self, temp, m):
        sent_old = m.getsent()
        samples_old = m.getsamples()
        p_old = m.pdf_samples(samples_old)  # m_old(samples_old)

        m.forget(sent_old)                  # m_old becomes m[-1]
        q_old = m.pdf_samples(samples_old)  # m[-1](samples_old)
        m.run(temp)
        sent_new = m.getsent()
        samples_new = m.getsamples()
        q_new = m.pdf_samples(samples_new)  # m[-1](samples_new)

        m.learn(sent_new)                   # m[-1] becomes m_new
        p_new = m.pdf_samples(samples_new)  # m_new(samples_new)
        m.forget(sent_new)                  # m_new becomes m[-1]
        
        m.learn(sent_old)                   # m[-1] becomes m_old

        return (
            p_old * q_new, p_new * q_old, 
            samples_old, samples_new, sent_old, sent_new
        )

    def sample_hparams(self):
        if self._hparamsmp:
            self._bidist.sample_hparams()
            self._unidist.sample_hparams()
        if self._poisson:
            self._poisreg.sample_hparams(self._unidist)

    def run_decoder(self):
        if self._verbose:
            sys.stderr.write('Decode: ')
        for i in xrange(len(self._lattices)):
            self._cnt += 1
            if self._verbose:
                sys.stderr.write('.')
                sys.stderr.flush()
            self._lattices[i].decode()

############################################################

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
