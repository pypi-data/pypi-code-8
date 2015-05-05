__author__ = 'victor'

from layer import Layer
from theano.tensor.shared_randomstreams import RandomStreams
from theano import tensor as T, config, shared
import numpy as np

class Dropout(Layer):
    """ Performs dropout in which a subsample of the incoming signal is deactivated

        Paper: http://arxiv.org/abs/1207.0580
        Geoffrey E. Hinton

        :ivar keep_rate: ``1 - drop_rate``, the probability that a signal is activated
        :ivar rng: random number generator used to subsample which incoming signal is kept
    """

    def __init__(self, drop_rate=0.5, rng=None):
        super(Dropout, self).__init__()
        if rng is None: rng = RandomStreams(0)
        self.keep_rate, self.rng = 1 - drop_rate, rng

    def forward(self, a):
        """
        :param a: input to the dropout layer
        :return: randomly deactivated version of the input
        """
        mask = self.rng.binomial(size=a.shape, p=self.keep_rate) / self.keep_rate
        return a * T.cast(mask, config.floatX)


class BatchNormalize(Layer):
    """ Performs batch normalization

        Paper: http://arxiv.org/abs/1502.03167
        Sergey Ioffe, Christian Szegedy

        :ivar gamma: normalization parameter (see ``forward_``)
        :ivar beta: normalization parameter (see ``forward_``)
    """

    def __init__(self, n_out, mode='train', gamma=None, beta=None, fudge=1e-8):
        super(BatchNormalize, self).__init__()
        self.mode = mode
        if gamma is None: gamma = np.random.normal(size=n_out)
        if beta is None: beta = np.random.normal(size=n_out)
        self.gamma, self.beta, self.fudge = shared(gamma, name=self.name+'.gamma'), shared(beta, name=self.name+'.beta'), fudge

    def forward(self, a):
        if self.mode == 'train':
            return self.forward_(a)
        else:
            return self.forward_test_(a)

    def forward_(self, a):
        """ Performs mean variance normalization on the input, scales by `gamma` and shifts by `beta`

        :param a: input to the batch normalization layer
        :return: normalized a
        """
        mean  = T.mean(a, axis=0, keepdims=True)
        var = T.var(a, axis=0, keepdims=True)
        return self.gamma * (a - mean) / T.sqrt(var + self.fudge) + self.beta

    def forward_test_(self, a):
        mean  = T.mean(a, axis=0, keepdims=True)
        var = T.var(a, axis=0, keepdims=True)
        return self.gamma / T.sqrt(var + self.fudge) * a + self.beta - self.gamma * mean / T.sqrt(var + self.fudge)
