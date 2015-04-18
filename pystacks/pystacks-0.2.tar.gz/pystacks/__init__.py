__author__ = 'victor'
from layers.layer import LinearLayer
from layers.container import Sequential, Parallel
from layers.lookup import LookupTable

from update import sgd, adagrad, rmsprop

from criteria import mean_squared_loss, cross_entropy_loss, negative_sampling_loss, max_margin_loss

from layers.transforms import Sigmoid, Tanh, ReLU, Softmax
