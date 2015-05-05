__author__ = 'victor'
import numpy as np
from theano import tensor as T, function, shared
from saveable import Saveable

from pystacks.update import sgd


class Layer(Saveable):
    count = 0

    def __init__(self):
        """ An abstraction for a ``Layer`` object
        """
        self.__class__.count += 1
        self.name = str(self.__class__.__name__) + str(self.__class__.count)

    def forward(self, a):
        """ Computes the forward activation of this ``Layer`` during training. The user should implement this function

        :param a: inputs into the layer
        :return: output from the layer
        """
        raise NotImplementedError

    def grad_updates(self, loss, lr, update=sgd, update_kwargs=None):
        """ Updates the parameters of this layer according to an update rule. By default SGD is used.

        :param loss: the variable to take gradients with respect to
        :param lr: learning rate
        """
        if update_kwargs is None: update_kwargs = {}
        updates = []
        for param, dparam in zip(self.params, self.dparams(loss)):
            updates += update(param, dparam, lr, **update_kwargs)
        return updates

    @property
    def params(self):
        """
        :return: a list of parameters for this layer
        """
        return []

    def dparams(self, loss):
        """
        :param loss: the variable to compute gradients with respect to
        :return: a list of gradients for the parameters of this layer
        """
        return [T.grad(loss, wrt=param) for param in self.params]

    @property
    def regularizable(self):
        """
        :return: a list of parameters for this layer for which to apply regularization
        """
        return []


class LinearLayer(Layer):
    """ A linear layer

    :ivar W: weight matrix of shape ``(n_in, n_out)``
    :ivar b: bias vector of shape ``(n_out)``

    :param n_in: feature dimension coming into this layer
    :param n_out: output dimension leaving this layer
    :param W: default value to initialize the weights to. Default is uniform distribution with bound ``sqrt(6/(n_in+n_out))``
    :param b: default value to initialize the bias to. Default is zero.
    """
    def __init__(self, n_in, n_out, W=None, b=None):

        self.n_in, self.n_out = n_in, n_out
        super(LinearLayer, self).__init__()
        bound = np.sqrt(6. / (n_in + n_out))
        if W is None:
            W = np.random.uniform(-bound, bound, (n_in, n_out))
        if b is None:
            b = np.zeros(n_out)
        self.W = shared(W, name=self.name + '.W')
        self.b = shared(b, name=self.name + '.b')

    @property
    def params(self):
        """
        :return: a list of learnable parameters for this layer
        """
        return [self.W, self.b]

    @property
    def regularizable(self):
        """
        :return: a list of regularizable paramters for this layer
        """
        return [self.W]

    def forward(self, a):
        """ Computes the forward function

        .. math::
            z = a W + b

        :param a: input into the linear layer
        """
        return T.dot(a, self.W) + self.b[np.newaxis, :]
