__author__ = 'victor'
import theano.tensor as T
from theano.tensor.extra_ops import to_one_hot

def mean_squared_loss(a, y):
    r""" Returns the means squared loss computed as

    .. math::
        J = \sum_t^T \sum_k (a^{(t)}-y^{(t)})_k^2

    :param a: predictions
    :param y: real valued target labels
    :return: mean squared loss
    """
    return 0.5 * T.mean(T.sum((a-y)**2, axis=1), axis=0)

def cross_entropy_loss(a, y, one_hot_num_classes=None):
    r""" Compute the cross entropy loss over a softmax

    .. math::
        J = \frac{1}{T} \sum_t^T \sum_k - (y * \log a)_k

    :param a: predictions
    :param y: a one hot encoding of the target labels
    :param one_hot_num_classes: if this option is specified, then ``y`` should be given
                as a vector which will be converted to a one hot matrix
    :return: cross entropy loss
    """
    my_y = y if one_hot_num_classes is None else to_one_hot(y, one_hot_num_classes)
    return - T.mean(T.sum(my_y * T.log(a), axis=1), axis=0)

def max_margin_loss(a_true, a_false, margin=1):
    r""" Computes the max margin loss

    .. math::
        J = \frac{1}{T} \sum_t^T (\sum_k max(0, 1 - a_{true}^{(t)} - a_{false}^{(t)}))_k

    :param a_true: scores for the correct example
    :param a_false: scores for the corresponding corrupted example
    :param margin: margin to use
    :return: max margin loss
    """
    margins = margin - a_true + a_false
    return T.sum(T.maximum(0, margins))

def negative_sampling_loss(a_true, a_false_list):
    r""" Computes the negative sampling loss

    .. math::
        J = - \log a_{true} - \sum_c^C \log (1 - a_{false, c})

    :param a_true: probabilities for the true examples
    :param a_false_list: list of probabilities for the corresponding false examples
    :return: negative sampling loss
    """
    return -T.log(a_true) - T.sum([T.log(1-a_false) for a_false in a_false_list], axis=0)

