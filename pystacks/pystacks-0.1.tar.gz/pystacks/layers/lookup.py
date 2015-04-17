import numpy as np
from scipy.sparse import csr_matrix
from theano import shared, function, tensor as T, sparse as S

from pystacks.layers.layer import Layer


__author__ = 'victor'


class LookupTable(Layer):

    def __init__(self, vocab_size, embedding_size, E=None):
        """
        Abstraction for a collection of vectors index by integers
        :param vocab_size: size of the collection
        :param embedding_size: length of each vector
        :param E: lookup table array, where E[i, :] holds the vector for entry i in the LookupTable
        """
        super(LookupTable, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        if E is None:
            scale = 0.01
            E = np.random.normal(scale=scale, size=(vocab_size, embedding_size))
        self.E = shared(E)

        self.normalize_E = function([], [], updates=[(self.E, self.E/T.sqrt(T.sum(self.E**2, axis=1)[:, np.newaxis]))])

    @property
    def params(self):
        return [self.E]

    def sparse_index_for_rows(self, idx):
        """
        :param idx: a 1-d numpy array of indices
        :return: a sparse array S such that np.dot(S, A) returns A[idx, :]
        """
        data = np.ones_like(idx)
        ind_ptr = np.arange(idx.size + 1)
        return csr_matrix((data, idx, ind_ptr), shape=(idx.size, self.vocab_size))

    def _forward(self, a):
        """
        Performs a lookup in the LookupTable for vectors corresponding to entries in 'a'
        :param a: a 1-d array of indices that denote the indices to items in the lookup table
        :return: a 2-d array A such that A[i, :] is the vector for entry i in the LookupTable
        """
        if isinstance(a, S.basic.SparseVariable):
            return S.structured_dot(a, self.E)
        else:
            return self.E[a, :]

