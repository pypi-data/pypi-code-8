__author__ = 'victor'
import theano.tensor as T

from pystacks.layers.layer import Layer


class Transform(Layer):

    def __init__(self):
        self.n_in = None
        self.n_out = None
        super(Transform, self).__init__()

class Sigmoid(Transform):

    def forward(self, a):
        return T.nnet.sigmoid(a)

class Tanh(Transform):

    def forward(self, a):
        return T.tanh(a)

class Softmax(Transform):

    def forward(self, a):
        return T.nnet.softmax(a)

class ReLU(Transform):

    def forward(self, a):
        return T.maximum(0, a)
