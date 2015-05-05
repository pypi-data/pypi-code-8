__author__ = 'victor'

from theano import tensor as T
import numpy as np

from saveable import Saveable
from pystacks.update import sgd


class MemoryLayer(Saveable):
    """ Abstraction for a memory layer
        Note that this class is not a subclass of ``Layer``
    """

    count = 0

    def __init__(self):
        self.__class__.count += 1
        self.name = self.__class__.__name__ + str(self.__class__.count)

    def forward(self, a, h_tm1):
        """ Computes the forward activation of this ``Layer`` during training. The user should implement this function

        :param a: inputs into the layer
        :param h_tm1: memory content from the previous time step
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


class RNNMemoryLayer(MemoryLayer):
    """ Vanilla RNN Layer
    """

    def __init__(self, n_in, n_out, W_in=None, W_h=None, b_h=None, h0=None):
        self.n_in, self.n_out  = n_in, n_out
        super(RNNMemoryLayer, self).__init__()

        self.W_in = self.gpu_param('W_in', shape=(n_in, n_out), init=W_in, fill='xavier')
        self.W_h = self.gpu_param('W_h', shape=(n_out, n_out), init=W_h, fill='xavier')
        self.b_h = self.gpu_param('b_h', shape=n_out, init=b_h, fill='zero')

        self.h0 = self.gpu_param('mem0', shape=n_out, init=h0, fill='zero')
        self.mem0 = [self.h0]

    @property
    def params(self):
        """
        :return: a list of parameters for this layer
        """
        return [self.W_in, self.W_h, self.b_h, self.h0]

    @property
    def regularizable(self):
        """
        :return: a list of regularizable parameters for this layer
        """
        return [self.W_in, self.W_h, self.h0]

    def forward(self, a, h_tm1):
        r""" Computes the forward function

        .. math::
            h_t = sigmoid( a W_{in} + h_{t-1} W_h + b_h)

        :param a: input into the linear layer
        :param h_tm1: hidden state at previous time step
        :return h_t: hidden state at current time step
        :return mem_t: a list of memories at this time step ``[h_t]``
        """
        h_t = T.nnet.sigmoid(T.dot(a, self.W_in) + T.dot(h_tm1, self.W_h) + self.b_h)
        mem_t = [h_t]
        return h_t, mem_t


class GRUMemoryLayer(MemoryLayer):
    """ Gated Recurrent Units
    """

    def __init__(self, n_in, n_out,
                 W_in=None, W_h = None,
                 W_in_reset=None, W_h_reset=None,
                 W_in_update=None, W_h_update=None,
                 h0=None):

        self.n_in, self.n_out = n_in, n_out
        super(GRUMemoryLayer, self).__init__()

        # reset gate
        self.W_in_reset = self.gpu_param('W_in_reset', shape=(n_in, n_out), init=W_in_reset, fill='xavier')
        self.W_h_reset = self.gpu_param('W_h_reset', shape=(n_out, n_out), init=W_h_reset, fill='xavier')

        # update gate
        self.W_in_update = self.gpu_param('W_in_update', shape=(n_in, n_out), init=W_in_update, fill='xavier')
        self.W_h_update = self.gpu_param('W_h_update', shape=(n_out, n_out), init=W_h_update, fill='xavier')

        # activation
        self.W_in = self.gpu_param('W_in', shape=(n_in, n_out), init=W_in, fill='xavier')
        self.W_h = self.gpu_param('W_h', shape=(n_out, n_out), init=W_h, fill='xavier')

        self.h0 = self.gpu_param('mem0', shape=n_out, init=h0, fill='zero')
        self.mem0 = [self.h0]

    @property
    def params(self):
        """
        :return: a list of parameters for this layer
        """
        return [self.W_in, self.W_h, self.W_in_update, self.W_in_reset, self.W_h_update, self.W_h_reset, self.h0]

    @property
    def regularizable(self):
        """
        :return: a list of regularizable parameters for this layer
        """
        return [self.W_in, self.W_h, self.W_in_update, self.W_in_reset, self.W_h_update, self.W_h_reset, self.h0]

    def forward(self, a, h_tm1):
        r""" Computes the forward function

        Note that to be consistent with other layers, we rename the update variable to ``u`` instead.

        .. math::
            u_t = sigmoid( a W_{in\_update} + h_{t-1} W_{h\_update} )

            r_t = sigmoid( a W_{in\_reset} + h_{t-1} W_{h\_reset} )

            g_t = tanh( a W_{in} + r_t * h_{t-1} W_h )

            h_t = u_t * h_{t-1} + (1-u_t) * g_t

        :param a: input into the linear layer
        :param h_tm1: hidden state at previous time step
        :return h_t: hidden state at current time step
        :return mem_t: a list of memories at this time step ``[h_t]``
        """
        u_t = T.nnet.sigmoid(T.dot(a, self.W_in_update) + T.dot(h_tm1, self.W_h_update))
        r_t = T.nnet.sigmoid(T.dot(a, self.W_in_reset) + T.dot(h_tm1, self.W_h_reset))
        g_t = T.tanh(T.dot(a, self.W_in) + r_t * T.dot(h_tm1, self.W_h))
        h_t = u_t * h_tm1 + (1-u_t) * g_t
        mem_t = [h_t]
        return h_t, mem_t


class LSTMMemoryLayer(MemoryLayer):
    """ Gated Recurrent Units
    """

    def __init__(self, n_in, n_out,
                 W_in=None, W_h = None,
                 W_in_input=None, W_h_input=None,
                 W_in_forget=None, W_h_forget=None,
                 W_in_output=None, W_h_output=None,
                 h0=None, c0=None):

        self.n_in, self.n_out = n_in, n_out
        super(LSTMMemoryLayer, self).__init__()

        # input gate
        self.W_in_input = self.gpu_param('W_in_input', shape=(n_in, n_out), init=W_in_input, fill='xavier')
        self.W_h_input = self.gpu_param('W_h_input', shape=(n_out, n_out), init=W_h_input, fill='xavier')

        # forget gate
        self.W_in_forget = self.gpu_param('W_in_forget', shape=(n_in, n_out), init=W_in_forget, fill='xavier')
        self.W_h_forget = self.gpu_param('W_h_forget', shape=(n_out, n_out), init=W_h_forget, fill='xavier')

        # output gate
        self.W_in_output = self.gpu_param('W_in_output', shape=(n_in, n_out), init=W_in_output, fill='xavier')
        self.W_h_output = self.gpu_param('W_h_output', shape=(n_out, n_out), init=W_h_output, fill='xavier')

        # activation
        self.W_in = self.gpu_param('W_in', shape=(n_in, n_out), init=W_in, fill='xavier')
        self.W_h = self.gpu_param('W_h', shape=(n_out, n_out), init=W_h, fill='xavier')

        self.h0 = self.gpu_param('h_0', shape=n_out, init=h0, fill='zero')
        self.c0 = self.gpu_param('h_0', shape=n_out, init=c0, fill='zero')

        self.mem0 = [self.h0, self.c0]

    @property
    def params(self):
        """
        :return: a list of parameters for this layer
        """
        return [self.W_in, self.W_h, self.W_in_input, self.W_h_input, self.W_in_forget, self.W_h_forget, self.W_in_output, self.W_h_output, self.h0, self.c0]

    @property
    def regularizable(self):
        """
        :return: a list of regularizable parameters for this layer
        """
        return [self.W_in, self.W_h, self.W_in_input, self.W_h_input, self.W_in_forget, self.W_h_forget, self.W_in_output, self.W_h_output, self.h0, self.c0]

    def forward(self, a, h_tm1, c_tm1):
        r""" Computes the forward function

        Note that to be consistent with other layers, we rename the update variable to ``u`` instead.

        .. math::
            i_t = sigmoid( a W_{in\_input} + h_{t-1} W_{h\_input} )

            f_t = sigmoid( a W_{in\_forget} + h_{t-1} W_{h\_forget} )

            o_t = sigmoid( a W_{in\_output} + h_{t-1} W_{h\_output} )

            g_t = tanh( a W_{in} + h_{t-1} W_h )

            c_t = f_t * c_{t-1} + i_t * g_t

            h_t = o_t * tanh(c_t)

        :param a: input into the linear layer
        :param mem_tm1: hidden state at previous time step
        :return mem_t: hidden state at current time step
        """

        i_t = T.nnet.sigmoid(T.dot(a, self.W_in_input) + T.dot(h_tm1, self.W_h_input))
        f_t = T.nnet.sigmoid(T.dot(a, self.W_in_forget) + T.dot(h_tm1, self.W_h_forget))
        o_t = T.nnet.sigmoid(T.dot(a, self.W_in_output) + T.dot(h_tm1, self.W_h_output))

        g_t = T.tanh(T.dot(a, self.W_in) + T.dot(h_tm1, self.W_h))
        c_t = f_t * c_tm1 + i_t * g_t
        h_t = o_t * T.tanh(c_t)

        mem_t = [h_t, c_t]
        return h_t, mem_t
