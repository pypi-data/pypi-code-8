from abc import ABCMeta, abstractmethod


class GetInfoAbstract(metaclass=ABCMeta):
    """
    Abstract class to retrieve information from a Json API
    """

    @abstractmethod
    def store_data(self):
        pass

