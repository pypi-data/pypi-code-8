import theano.tensor as T

from pystacks.layers.layer import Layer


class Container(Layer):
    """ Abstraction for a container of ``Layer`` objects. A ``Container`` can also contain other ``Container`` objects

    :ivar components: list of ``Layer`` objects that are included in this ``Container``
    """

    def __init__(self, components):

        self.components = components
        super(Container, self).__init__()

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

    def forward_(self, a):
        """
        :param ``a``: input into the ``Sequential`` container
        :return: output of the last ``Layer``
        """
        z = a
        for c in self.components:
            z = c.forward(z)
        return z


class Parallel(Container):

    def forward_(self, a):
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


