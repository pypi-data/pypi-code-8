__author__ = 'victor'
import numpy as np
from theano import tensor as T, function, shared

from pystacks.update import sgd


class Layer(object):
    count = 0

    def __init__(self, batch_size=100):
        """
        An abstraction for a Layer object
        """
        self.__class__.count += 1

    def forward(self, a):
        return self._forward(a)

    def _forward(self, a):
        raise NotImplementedError

    def grad_updates(self, loss, lr, update=sgd, update_kwargs=None):
        """
        Updates the parameters of this layer according to an update rule. By default SGD is used.
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

    def __init__(self, n_in, n_out, W=None, b=None):
        """
        A linear layer



        :ivar W: weight matrix of shape (n_in, n_out)
        :ivar b: bias vector of shape (n_out)

        :param n_in: feature dimension coming into this layer
        :param n_out: output dimension leaving this layer
        :param W: default value to initialize the weights to. Default is uniform distribution with bound sqrt(6/(n_in+n_out))
        :param b: default value to initialize the bias to. Default is zero.
        """
        self.n_in, self.n_out = n_in, n_out
        super(LinearLayer, self).__init__()
        bound = np.sqrt(6. / (n_in + n_out))
        if W is None:
            W = np.random.uniform(-bound, bound, (n_in, n_out))
        if b is None:
            b = np.zeros(n_out)
        self.W = shared(W)
        self.b = shared(b)

    @property
    def params(self):
        return [self.W, self.b]

    @property
    def regularizable(self):
        return [self.W]

    def _forward(self, a):
        """
        Computes the forward function

        .. math::
            z = a W + b

        :param a: input into the linear layer
        """
        self._input = a
        self._output = T.dot(a, self.W) + self.b[np.newaxis, :]
        return self._output


if __name__ == '__main__':
    tmp = np.random.uniform(size=(3,4)).astype('float32')
    f = lambda x: x.dot(tmp)
    linear = LinearLayer(3, 4)
    x = T.fmatrix()
    y = T.fmatrix()
    guess = linear.forward(x)
    loss = T.sum(0.5*(guess - y)**2)
    sgd = function(inputs=[x, y], outputs=[loss, guess], updates=linear.grad_updates(lr=0.1, loss=loss))

    for i in range(100):
        batch_x = np.random.uniform(size=(6,3)).astype('float32')
        batch_y = f(batch_x)
        cost, out = sgd(batch_x, batch_y)
        if i%10 == 0:
            print 'iteration', i, 'error', cost
