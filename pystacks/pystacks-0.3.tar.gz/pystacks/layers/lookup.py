import numpy as np
from scipy.sparse import csr_matrix
from theano import shared, function, tensor as T, sparse as S
from theano.tensor.extra_ops import to_one_hot

from layer import Layer


__author__ = 'victor'


class LookupTable(Layer):
    """ Abstraction for a collection of vectors index by integers
    :ivar vocab_size: size of the collection
    :ivar embedding_size: length of each vector
    :ivar window_size: how many words to look up at a time, default is 1
    :ivar E: lookup table array, where ``E[i, :]`` holds the vector for entry ``i`` in the LookupTable
    :ivar advanced_indexing: whether to perform look up by indexing or by multiplying by one hot vectors (much more memory!)
    """

    def __init__(self, vocab_size, embedding_size, window_size=1, E=None, advanced_indexing=True):
        super(LookupTable, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.window_size = 1
        self.n_in = window_size
        self.n_out = embedding_size
        self.advanced_indexing = advanced_indexing
        if E is None:
            scale = 0.01
            E = np.random.normal(scale=scale, size=(vocab_size, embedding_size))
        self.E = shared(E, name=self.name + '.E')

        self.normalize_E = function([], [], updates=[(self.E, self.E/T.sqrt(T.sum(self.E**2, axis=1)[:, np.newaxis]))])

    @property
    def params(self):
        """
        :return: list of learnable parameters for this layer
        """
        return [self.E]

    def forward(self, a):
        """ Performs a lookup in the LookupTable for vectors corresponding to entries in ``a``

        :param a: a 2-d array of indices that denote the indices to items in the lookup table
        :return: a 2-d array A such that ``A[i, :]`` contain the concatenated vectors for words
                requested by row ``i`` of ``a``
        """
        if a.ndim < 2: # this is a scalar index
            return self.E[a]

        lookup = []
        for col in range(self.window_size):
            if self.advanced_indexing:
                lookup += [self.E[a[:, col]]]
            else:
                one_hot = to_one_hot(a[:, col], nb_class=self.vocab_size)
                lookup += [T.dot(one_hot, self.E)]
        return T.concatenate(lookup, axis=1)

