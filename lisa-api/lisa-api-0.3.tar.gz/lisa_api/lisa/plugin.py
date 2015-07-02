import abc
import six


@six.add_metaclass(abc.ABCMeta)
class PluginBase(object):
    """Base class for example plugin.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def add_intents(self):
        """Install intents in the database
        """
