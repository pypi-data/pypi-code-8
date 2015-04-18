from theano import tensor as T, function, shared
import numpy as np

def sgd(param, grad, lr):
    r""" Performs the update rule

    .. math:: \theta := \theta - lr * \nabla_{\theta} J

    :param param: parameter to be updated
    :param grad: gradient
    :param lr: learning rate
    :return: updates for sgd
    """
    return [(param, param - lr * grad)]

def adagrad(param, grad, lr):
    r""" Performs the update rule

    .. math::
        A := A + (\nabla_\theta J)^2

        \theta := \theta - lr * \frac{\nabla_\theta J}{\sqrt A}

    :param param: parameter to be updated
    :param grad: gradient
    :param lr: learning rate
    :return: updates for adagrad
    """
    helper = shared(value=np.zeros(param.get_value().shape))
    new_helper = helper + grad**2
    return [
        (param, param - lr * grad / T.sqrt(1e-8 + new_helper)),
        (helper, new_helper)
        ]

def rmsprop(param, grad, lr, alpha=0.9, beta=0.1):
    r""" Performs the update rule

    .. math::
        A := \alpha A + \beta (\nabla_\theta J)^2

        \theta := \theta - lr * \frac{\nabla_\theta J}{\sqrt A}

    :param param: parameter to be updated
    :param grad: gradient
    :param lr: learning rate
    :param alpha: cache mixing portion for the previous cache
    :param beta: cache mixing portion for the new gradient
    :return: updates for rmsprop
    """
    helper = shared(value=np.zeros(param.get_value().shape))
    new_helper = 0.9 * helper + 0.1 * grad**2
    return [
        (param, param - lr * grad / T.sqrt(1e-8 + new_helper)),
        (helper, new_helper)
        ]
