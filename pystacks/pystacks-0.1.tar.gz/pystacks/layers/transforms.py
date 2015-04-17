__author__ = 'victor'
import theano.tensor as T

from pystacks.layers.layer import Layer


class Transform(Layer):
    pass

class Sigmoid(Transform):

    def _forward(self, a):
        return T.nnet.sigmoid(a)

class Tanh(Transform):

    def _forward(self, a):
        return T.tanh(a)

class Softmax(Transform):

    def _forward(self, a):
        return T.nnet.softmax(a)

class ReLU(Transform):

    def _forward(self, a):
        return T.maximum(0, a)
