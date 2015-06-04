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

    def pdf_samples(self, samples):
        result = 1.0
        for (x, y) in samples:
            t0 = self.get_text(x, y)
            result *= self.pdf_uni(t0)
        return result

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

    def pdf_samples(self, samples):
        samples = sorted(samples)
        result = 1.0
        if len(samples) > 0:
            (x0, y0) = samples[0]
            t0 = self.get_text(x0, y0)
            result *= self.pdf_uni(t0)
        for i in xrange(1, len(samples)):
            (x1, y1) = samples[i - 1]
            (x0, y0) = samples[i]
            t0 = self.get_text(x0, y0)
            t1 = self.get_text(x1, y1)
            result *= self.pdf_bi(t0, t1)
        return result

    def learn(self, sent):
        super(TopicBigram, self).learn(sent)
        for i in xrange(len(sent)):
            t0 = sent[i]
            if i > 0: t1 = sent[i - 1]
            else: t1 = None
            ctx = TopicContext((t1,), self._topic)
            self._bidist.inc(t0, ctx)

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

    def pdf_samples(self, samples): 
        samples = sorted(samples)
        result = 1.0
        t0 = None
        if len(samples) > 0:
            (x0, y0) = samples[0]
            t0 = self.get_text(x0, y0)
            result *= self.pdf_uni(t0)
        if len(samples) > 1:
            (x1, y1) = samples[1]
            t1 = self.get_text(x1, y1)
            result *= self.pdf_bi(t0, t1)
        for i in xrange(2, len(samples)):
            (x2, y2) = samples[i - 2]
            (x1, y1) = samples[i - 1]
            (x0, y0) = samples[i]
            t0 = self.get_text(x0, y0)
            t1 = self.get_text(x1, y1)
            t2 = self.get_text(x2, y2)
            result *= self.pdf_tri(t0, t1, t2)
        return result

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

    def save_samples(self, i):
        m = self._lattices[i]
        topic = m.get_topic()
        samples = tuple(sorted(m.getsamples()))
        if len(samples) > 0:
            prob = m.pdf_samples(samples)
            self._totaldist.inc((topic, samples), i, prob)

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

    def run_decoder_onestep(self, i):
        m = self._lattices[i]
        (topic, samples) = self._totaldist.maxconsq(i)
        m.set_topic(topic)
        m.setsamples(samples)

############################################################

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
