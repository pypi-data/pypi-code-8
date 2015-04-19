from abc import ABCMeta, abstractproperty, abstractmethod
import six


@six.add_metaclass(ABCMeta)
class Storage(object):
    @abstractproperty
    def control_block_file(self):
        raise NotImplementedError

    @abstractproperty
    def data_block_file(self):
        raise NotImplementedError

    @abstractmethod
    def update_control_block(self, control_block):
        raise NotImplementedError

    @abstractmethod
    def update_data_block(self, data_block):
        raise NotImplementedError

    def save(self, control_block, data_block):
        self.update_control_block(control_block)
        self.update_data_block(data_block)


from . fs import *