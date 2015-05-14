#!/usr/bin/env pypy
#-*- coding: utf-8 -*-

import os, sys
from collections import *

from prob import *
from wordseg import *
from strdist import *
from ngram import *
from topicdist import *

############################################################

class TopicUnigram(Unigram):

    def __init__(
        self, text, strdist, unidist, topicdist,
        segments=None, atoms=None, samples=None, dist=None,
        fwdbwd=False, poisreg=None, topic=None,
        totaldist=None, idx=None
    ):
        super(TopicUnigram, self).__init__(
            text, strdist, unidist, 
            segments, atoms, samples, dist, fwdbwd, poisreg,
            totaldist=totaldist, idx=idx
        )
        self._topicdist = topicdist
        self._topic = topic

    def __copy__(self):
        return TopicUnigram(
            self._text, 
            copy.copy(self._strdist), copy.copy(self._unidist),
            copy.copy(self._topicdist),
            copy.copy(self._segments), copy.copy(self._atoms), 
            copy.copy(self._samples), copy.copy(self._dist),
            self._fwdbwd, self._poisreg, self._topic,
            totaldist=self._totaldist, idx=self._idx
        )

    def set_topic(self, topic):
        self._topic = topic

    def get_topic(self):
        return self._topic

    def pdf_uni(self, t0):
        p = self._unidist.pdf(t0, self._topic)
        if self._unidist.contains(t0, self._topic):
            return p
        else:
            return p * self.basepdf(t0)

    def basepdf(self, t0):
        result = 1.0
        for c in t0:
            result *= self._strdist.pdf(c, self._topic)
        if self._poisreg:
            result *= self._poisreg.pdf(len(t0))
        return result

    def forget(self, sent):
        for i in xrange(len(sent)):
            t0 = sent[i]
            self._strdist.forget(t0, self._topic)
            self._unidist.dec(t0, self._topic)

    def learn(self, sent):
        for i in xrange(len(sent)):
            t0 = sent[i]
            self._strdist.learn(t0, self._topic)
            self._unidist.inc(t0, self._topic)

    def genkey_uni(self, idx, z, x, y):
        return (z, self.get_text(x, y))

    def enumkeys_uni(self, totaldist):
        for z in xrange(self._topicdist.get_maxtopics()):
            for y in xrange(1, len(self._text) + 1):
                for x in self.unigrams(y):
                    key = self.genkey_uni(self._idx, z, x, y)
                    totaldist.add_unikey(key)

    def fwd_decode(self):
        tbl = {}
        topic_old = self.get_topic()
        for z in xrange(self._topicdist.get_maxtopics()):
            tbl[z] = {}
            for y in xrange(1, len(self._text) + 1):
                tbl[z][y] = {}
                self.set_topic(z)
                for x in self.unigrams(y):
                    key = self.genkey_uni(self._idx, z, x, y)
                    p = math.log(self._totaldist[key])
                    if x > 0:
                        choices = []
                        for k in self.unigrams(x):
                            (p1, k1) = tbl[z][x][k]
                            choices.append((p1, k))
                        choices.sort(reverse=True)
                        if len(choices) > 0:
                            (p1, k) = choices[0]
                            tbl[z][y][x] = (p + p1, k)
                    else: tbl[z][y][x] = (p, None)
        self.set_topic(topic_old)
        return tbl

    def bwd_decode(self, tbl):
        self.clearsamples()
        y = len(self._text)
        choices = []
        for z in xrange(self._topicdist.get_maxtopics()):
            for x in tbl[z][y]:
                choices.append((tbl[z][y][x], z))
        choices.sort(reverse=True)
        (_, z) = choices[0]
        self.set_topic(z)
        while y is not None and y > 0 and y in tbl[z]:
            choices = []
            for x in tbl[z][y]:
                choices.append((tbl[z][y][x], x))
            choices.sort(reverse=True)
            if len(choices) == 0: break
            (p, x) = choices[0]
            self.addsample(x, y)
            y = x

############################################################

class TopicBigram(TopicUnigram):

    def __init__(
        self, text, strdist, unidist, bidist, topicdist,
        segments=None, atoms=None, samples=None, dist=None,
        fwdbwd=False, poisreg=None, topic=None,
        totaldist=None, idx=None
    ):
        super(TopicBigram, self).__init__(
            text, strdist, unidist, topicdist,
            segments, atoms, samples, dist,
            fwdbwd, poisreg, topic,
            totaldist=totaldist, idx=idx
        )
        self._bidist = bidist

    def __copy__(self):
        return TopicBigram(
            self._text, copy.copy(self._strdist),
            copy.copy(self._unidist), copy.copy(self._bidist),
            copy.copy(self._topicdist),
            copy.copy(self._segments), copy.copy(self._atoms), 
            copy.copy(self._samples), copy.copy(self._dist),
            self._fwdbwd, self._poisreg, self._topic,
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
        ctx = TopicContext((t1,), self._topic)
        p = self._bidist.pdf(t0, ctx)
        if self._bidist.contains(t0, ctx):
            return p
        else:
            return p * self.pdf_uni(t0)

    def forget(self, sent):
        super(TopicBigram, self).forget(sent)
        for i in xrange(len(sent)):
            t0 = sent[i]
            if i > 0: t1 = sent[i - 1]
            else: t1 = None
            ctx = TopicContext((t1,), self._topic)
            self._bidist.dec(t0, ctx)

    def learn(self, sent):
        super(TopicBigram, self).learn(sent)
        for i in xrange(len(sent)):
            t0 = sent[i]
            if i > 0: t1 = sent[i - 1]
            else: t1 = None
            ctx = TopicContext((t1,), self._topic)
            self._bidist.inc(t0, ctx)

    def genkey_bi(self, idx, z, k, x, y):
        t0 = self.get_text(x, y)
        t1 = self.get_text(k, x)
        return (z, t0, t1)

    def enumkeys_bi(self, totaldist):
        for z in xrange(self._topicdist.get_maxtopics()):
            for y in xrange(1, len(self._text) + 1):
                for x in self.unigrams(y):
                    if x > 0:
                        for k in self.unigrams(x):
                            key = self.genkey_bi(self._idx, z, k, x, y)
                            totaldist.add_bikey(key)

    def fwd_decode(self):
        tbl = {}
        for z in xrange(self._topicdist.get_maxtopics()):
            tbl[z] = {}
            for y in xrange(1, len(self._text) + 1):
                tbl[z][y] = {}
                for x in self.unigrams(y):
                    if x > 0:
                        choices = []
                        for k in self.unigrams(x):
                            key = self.genkey_bi(self._idx, z, k, x, y)
                            p = math.log(self._totaldist[key])
                            (p1, k1) = tbl[z][x][k]
                            choices.append((p + p1, k))
                        choices.sort(reverse=True)
                        if len(choices) > 0:
                            (p1, k) = choices[0]
                            tbl[z][y][x] = (p1, k)
                    else:
                        key = self.genkey_uni(self._idx, z, x, y)
                        p = math.log(self._totaldist[key])
                        tbl[z][y][x] = (p, None)
        return tbl

############################################################

class TopicTrigram(TopicBigram):

    def __init__(
        self, text, strdist, unidist, bidist, tridist, topicdist,
        segments=None, atoms=None, samples=None, dist=None,
        fwdbwd=False, poisreg=None, topic=None,
        totaldist=None, idx=None
    ):
        super(TopicTrigram, self).__init__(
            text, strdist, unidist, bidist, topicdist,
            segments, atoms, samples, dist,
            fwdbwd, poisreg, topic,
            totaldist=totaldist, idx=idx
        )
        self._tridist = tridist

    def __copy__(self):
        return TopicTrigram(
            self._text, copy.copy(self._strdist),
            copy.copy(self._unidist), copy.copy(self._bidist),
            copy.copy(self._tridist), copy.copy(self._topicdist),
            copy.copy(self._segments), copy.copy(self._atoms), 
            copy.copy(self._samples), copy.copy(self._dist),
            self._fwdbwd, self._poisreg, self._topic,
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
        ctx = TopicContext((t1, t2), self._topic)
        p = self._tridist.pdf(t0, ctx)
        if self._tridist.contains(t0, ctx):
            return p
        else:
            return p * self.pdf_bi(t0, t1)

    def forget(self, sent):
        super(TopicTrigram, self).forget(sent)
        for i in xrange(len(sent)):
            t0 = sent[i]
            if i > 1: t2 = sent[i - 2]
            else: t2 = None
            if i > 0: t1 = sent[i - 1]
            else: t1 = None
            ctx = TopicContext((t1, t2), self._topic)
            self._tridist.dec(t0, ctx)

    def learn(self, sent):
        super(TopicTrigram, self).learn(sent)
        for i in xrange(len(sent)):
            t0 = sent[i]
            if i > 1: t2 = sent[i - 2]
            else: t2 = None
            if i > 0: t1 = sent[i - 1]
            else: t1 = None
            ctx = TopicContext((t1, t2), self._topic)
            self._tridist.inc(t0, ctx)

    def genkey_tri(self, idx, z, k2, k1, x, y):
        t0 = self.get_text(x, y)
        t1 = self.get_text(k1, x)
        t2 = self.get_text(k2, k1)
        return (z, t0, t1, t2)

    def enumkeys_tri(self, totaldist):
        for z in xrange(self._topicdist.get_maxtopics()):
            for y in xrange(1, len(self._text) + 1):
                for x in self.unigrams(y):
                    if x > 1:
                        for k1 in self.unigrams(x):
                            if k1 is None: continue
                            for k2 in self.unigrams(k1):
                                if k2 is None: continue
                                key = self.genkey_tri(self._idx, z, k2, k1, x, y)
                                totaldist.add_trikey(key)

    def fwd_decode(self):
        tbl = {}
        for z in xrange(self._topicdist.get_maxtopics()):
            tbl[z] = {}
            for y in xrange(1, len(self._text) + 1):
                tbl[z][y] = {}
                for x in self.unigrams(y):
                    if x > 1:
                        choices = []
                        for k1 in self.unigrams(x):
                            if k1 is None: continue
                            for k2 in self.unigrams(k1):
                                if k2 is None: continue
                                key = self.genkey_tri(self._idx, z, k2, k1, x, y)
                                p = math.log(self._totaldist[key])
                                (p1, _) = tbl[z][x][k1]
                                (p2, _) = tbl[z][k1][k2]
                                choices.append((p + p1 + p2, (k1, k2)))
                        choices.sort(reverse=True)
                        if len(choices) > 0:
                            (p1, (k1, k2)) = choices[0]
                            tbl[z][y][x] = (p1, (k1, k2))
                    elif x > 0:
                        choices = []
                        for k in self.unigrams(x):
                            key = self.genkey_bi(self._idx, z, k, x, y)
                            p = math.log(self._totaldist[key])
                            (p1, _) = tbl[z][x][k]
                            choices.append((p + p1, (None, (k, None))))
                        choices.sort(reverse=True)
                        if len(choices) > 0:
                            (p1, (k, _)) = choices[0]
                            tbl[z][y][x] = (p1, (k, None))
                    else:
                        key = self.genkey_uni(self._idx, z, x, y)
                        p = math.log(self._totaldist[key])
                        tbl[z][y][x] = (p, (None, None))
        return tbl

############################################################

class TopicWordseg(Wordseg):

    def __init__(
        self, n, cn, texts, atomfn=None, wordfn=None, 
        maxatomlen=None, maxwordlen=20,
        maxiters=100, burnin=None,
        alpha_char=0.0, alpha_uni=0.0, alpha_bi=0.0, alpha_tri=0.0,
        theta_char=1.0, theta_uni=1.0, theta_bi=1.0, theta_tri=1.0,
        p_stop=None, strdist=None, unidist=None, bidist=None, tridist=None,
        fwdbwd=False, hparamsmp=False, maxtemp=0.0, poisson=False,
        disk=None,
        maxtopics=5, topicdist=None,
        alpha_topic=0.0, theta_topic=1.0
    ):
        if strdist is None:
            strdist = TopicStrDist(
                cn, alpha_char, theta_char, p_stop=p_stop
            )
        super(TopicWordseg, self).__init__(
            n, cn, texts, atomfn=atomfn, wordfn=wordfn, 
            maxatomlen=maxatomlen, maxwordlen=maxwordlen, 
            maxiters=maxiters, burnin=burnin,
            alpha_char=alpha_char, alpha_uni=alpha_uni,
            alpha_bi=alpha_bi, alpha_tri=alpha_tri,
            theta_char=theta_char, theta_uni=theta_uni,
            theta_bi=theta_bi, theta_tri=theta_tri,
            p_stop=p_stop, strdist=strdist,
            unidist=unidist, bidist=bidist, tridist=tridist,
            fwdbwd=fwdbwd, hparamsmp=hparamsmp, 
            maxtemp=maxtemp, poisson=poisson,
            disk=disk
        )
        if topicdist is None:
            topicdist = TopicDist(maxtopics, alpha_topic, theta_topic)
        self._maxtopics = maxtopics
        self._topicdist = topicdist

    def collectkeys(self, m):
        if isinstance(m, TopicTrigram):
            m.enumkeys_tri(self._totaldist)
        if isinstance(m, TopicBigram):
            m.enumkeys_bi(self._totaldist)
        if isinstance(m, TopicUnigram):
            m.enumkeys_uni(self._totaldist)

    def build_onetext(self, text, idx):
        m = super(TopicWordseg, self).build_onetext(text, idx)
        t = self._topicdist.random(m.getsent())
        m.set_topic(t)
        return m

    def buildmodel(self, text, idx):
        if self._n == 1:
            m = TopicUnigram(
                text, self._strdist, 
                self._unidist, self._topicdist,
                fwdbwd=self._fwdbwd, poisreg=self._poisreg,
                totaldist=self._totaldist, idx=idx
            )
        elif self._n == 2:
            m = TopicBigram(
                text, self._strdist, 
                self._unidist, self._bidist, self._topicdist,
                fwdbwd=self._fwdbwd, poisreg=self._poisreg,
                totaldist=self._totaldist, idx=idx
            )
        elif self._n == 3:
            m = TopicTrigram(
                text, self._strdist, self._unidist, 
                self._bidist, self._tridist, 
                self._topicdist,
                fwdbwd=self._fwdbwd, poisreg=self._poisreg,
                totaldist=self._totaldist, idx=idx
            )
        else: raise NotImplemented
        return m

    def acctotal(self):
        for (z, t0) in self._totaldist.unikeys():
            key = (z, t0)
            self.acc(key, self._unidist.pdf(t0, z))
        for (z, t0, t1) in self._totaldist.bikeys():
            ctx = TopicContext(t1, z)
            key = (z, t1, t0)
            self.acc(key, self._bidist.pdf(t0, ctx))
        for (z, t0, t1, t2) in self._totaldist.trikeys():
            ctx = TopicContext((t1, t2), z)
            key = (z, t0, t1, t2)
            self.acc(key, self._tridist.pdf(t0, ctx))

    def gibbs(self, i, temp):
        # sentence-level blocked Gibbs sampler
        m = self._lattices[i]
        m.forget(m.getsent())
        self._topicdist.dec(m.get_topic())
        t = self._topicdist.random(m.getsent())
        m.set_topic(t)
        m.run(temp)
        m.learn(m.getsent())
        self._topicdist.inc(t)

    def mh(self, i, temp):
        # Metropolis-Hasting algorithm
        m = self._lattices[i]
        (
            p_old, p_new, samples_old, samples_new, 
            sent_old, sent_new, topic_old, topic_new
        ) = self.mh_transition(temp, m)
        if p_new > 0.0:
            acc = p_old / p_new
        else: acc = None
        if acc is not None and acc < 1:
            r = random.random()
            if r < acc:
                m.forget(sent_old)
                self._topicdist.dec(topic_old)
                m.learn(sent_new)
                m.set_topic(topic_new)
                self._topicdist.inc(topic_new)
                m.setsamples(samples_new)
                return True
        return False

    def mh_transition(self, temp, m):
        sent_old = m.getsent()
        samples_old = m.getsamples()
        p_old = m.pdf_samples(samples_old)  # m_old(samples_old)
        topic_old = m.get_topic()

        m.forget(sent_old)                  # m_old becomes m[-1]
        q_old = m.pdf_samples(samples_old)  # m[-1](samples_old)
        self._topicdist.dec(topic_old)
        topic_new = self._topicdist.random(sent_old)
        m.set_topic(topic_new)
        self._topicdist.inc(topic_new)
        m.run(temp)
        sent_new = m.getsent()
        samples_new = m.getsamples()
        q_new = m.pdf_samples(samples_new)  # m[-1](samples_new)

        m.learn(sent_new)                   # m[-1] becomes m_new
        p_new = m.pdf_samples(samples_new)  # m_new(samples_new)
        m.forget(sent_new)                  # m_new becomes m[-1]
        self._topicdist.dec(topic_new)

        m.learn(sent_old)                   # m[-1] becomes m_old
        m.set_topic(topic_old)
        self._topicdist.inc(topic_old)

        return (
            p_old * q_new, p_new * q_old, 
            samples_old, samples_new, 
            sent_old, sent_new, topic_old, topic_new
        )

    def sample_hparams(self):
        super(TopicWordseg, self).sample_hparams()
        self._topicdist.sample_hparams()

############################################################

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
