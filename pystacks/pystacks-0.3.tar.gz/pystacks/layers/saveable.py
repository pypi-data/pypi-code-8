import numpy as np
import json
import os
from theano import shared

class Saveable(object):

    def save(self, to_dir):
        """ Saves the network parameters and configurations

        :param to_dir: directory in which to save the network
        """
        config = {'components':[], 'params':[]}
        if isinstance(self, list):
            for c in self.components:
                config['components'] += [c.name]
                c.save(to_dir)
        else:
            for param in self.params:
                np.save(os.path.join(to_dir, param.name), param.get_value())
                config['params'] += [param.name]
        with open(os.path.join(to_dir, self.name + '.json'), 'wb') as f:
            json.dump(config, f)

    def gpu_param(self, name, shape=None, init=None, fill='xavier'):
        """ returns an initialized parameter on the GPU

        :param name: name of the parameter in the computation graph
        :param shape: shape of the parameter
        :param init: if not ``None``, the parameter will be initialized to the value of ``init``
        :param fill: if ``init`` is not specified, the parameter will be initialized using the specified `fill`. Can be
                     ``xavier`` or ``zero``
        :return: a Theano shared parameter
        """
        if init is None:
            if fill == 'xavier':
                n_in, n_out = shape
                bound = np.sqrt(6. / (n_in + n_out))
                init = np.random.uniform(-bound, bound, (n_in, n_out))
            elif fill == 'zero':
                init = np.zeros(shape)
            else:
                init = np.random.uniform(-0.1, 0.1, shape)
        return shared(init, name=self.name + '.' + name)
