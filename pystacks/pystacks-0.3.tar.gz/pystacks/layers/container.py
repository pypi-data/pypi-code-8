import theano.tensor as T
from theano import scan
from layer import Layer
from memory import *

class Container(Layer):
    """ Abstraction for a container of ``Layer`` objects. A ``Container`` can also contain other ``Container`` objects

    :ivar components: list of ``Layer`` objects that are included in this ``Container``
    """

    def __init__(self, components):
        self.components = components
        super(Container, self).__init__()

    @property
    def n_in(self):
        raise NotImplementedError

    @property
    def n_out(self):
        raise NotImplementedError

    @property
    def params(self):
        """
        :return: a list of all parameters of ``Layer`` objects contained in this ``Container``
        """
        params = []
        for c in self.components:
            params += [p for p in c.params if p not in params] # don't add duplicates
        return params


class Sequential(Container):
    """ A sequential container like a multilayer perceptron. The output of each layer is used as the input to the next
        layer.
    """

    @property
    def n_in(self):
        """
        :return: input dimension of the first layer in the container
        """
        ret = self.components[0].n_in
        assert ret is not None
        return ret

    @property
    def n_out(self):
        """
        :return: output dimension of the last layer in the container
        """
        # the last layer may not have n_out set because it infers its size from the input
        ret = None
        for c in reversed(self.components):
            ret = c.n_out
            if ret is not None: break
        assert ret is not None, 'could not deduce n_out for Sequential'
        return ret

    def forward(self, a):
        """
        :param ``a``: input into the ``Sequential`` container
        :return: output of the last ``Layer``
        """
        z = a
        for c in self.components:
            z = c.forward(z)
        return z


class Parallel(Container):
    """ A parallel container. The input to the container is divided up into inputs for each layer in the container (see
        ``self.forward``. The output of the container is the concatenation of the output of each layer in the container
    """

    @property
    def n_in(self):
        """
        :return: the sum of the number of inputs in each layer in the container
        """
        ret = 0
        for c in self.components:
            assert c.n_in is not None, str(c) + ' has no n_in'
            ret += c.n_in
        return ret

    @property
    def n_out(self):
        """
        :return: the sum of the number of outputs in each layer in the container
        """
        ret = 0
        for c in self.components:
            assert c.n_out is not None, str(c) + ' has no n_out'
            ret += c.n_out
        return ret

    def forward(self, a):
        """
        :param a: input into the ``Parallel`` container. Suppose the ``Layer`` ``i`` has ``n_in_i`` and ``n_out_i``, then
                    ``a[:, 0:n_in_0]`` is given as input to the first Layer, ``a[:, n_in_0:n_in_0+n_in_1]`` is
                    given as input to the second Layer, and so forth.
        :return: output of the ``Parallel`` container. ``z[:, 0:n_out_0]`` is produced by the first Layer,
                    ``z[:, n_out_0:n_out_0+n_out_1]`` is produced by the second Layer, and so forth.
        """
        z = []
        start = 0
        for c in self.components:
            end = start + c.n_in
            a_c = a[:, start:end]
            z.append(c.forward(a_c))
            start = end
        return T.concatenate(z, axis=1)


class Recurrent(Container):

    @property
    def n_in(self):
        """
        :return: input dimension of the first layer in the container
        """
        ret = self.components[0].n_in
        assert ret is not None
        return ret

    @property
    def n_out(self):
        """
        :return: output dimension of the last layer in the container
        """
        # the last layer may not have n_out set because it infers its size from the input
        ret = None
        for c in reversed(self.components):
            ret = c.n_out
            if ret is not None: break
        assert ret is not None, 'could not deduce n_out for Sequential'
        return ret

    def recurrence(self, x_t, *memories_tm1):
        """ generates a time step in the recurrent sequence

        :param x_t: input at current time step
        :param memories_tm1: memory states from the previous time step
        :return: returns a list of memories from the current time step and the activation at the current time step
        """
        memory_i = 0
        z = x_t
        memories_t = []

        for component in self.components:
            if isinstance(component, MemoryLayer):
                mem_tm1 = memories_tm1[memory_i:memory_i+len(component.mem0)]
                z, mem_t = component.forward(z, *mem_tm1)
                memories_t += mem_t
                memory_i += len(component.mem0)
            else:
                z = component.forward(z)
        return memories_t + [z]

    def forward(self, a, return_history=False):
        """ returns the activation of this layer that is generated at the end of the sequence

        :param a: sequence of inputs
        :param return_history: if ``True``, return the hidden states and the activation through each time step for this sequence
                               else return the activation during the last time step after iterating over the entire
                               sequence.
        :return: see ``return_history``
        """
        memories = []
        for c in self.components:
            if isinstance(c, MemoryLayer):
                mem = [T.alloc(m, a.shape[1], c.n_out) for m in c.mem0]
                memories += mem
        assert memories, "Recurrent network has no memory cells! If this is intentional, you should use Sequential instead!"
        results_through_time, updates = scan(fn=self.recurrence,
                                sequences=a,
                                outputs_info=memories + [None],
                                n_steps=a.shape[0])
        z_through_time = results_through_time[-1]
        hidden_states_through_time = results_through_time[:-1]
        if return_history:
            return results_through_time
        else:
            return z_through_time[-1]


