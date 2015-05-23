from abc import ABCMeta, abstractmethod


class GetInfoAbstract(metaclass=ABCMeta):
    """
    Abstract class to retrieve information from a Json API
    """

    @abstractmethod
    def store_data(self, data):
        pass

    @abstractmethod
    def http_retrieve(self, url):
        pass

    @abstractmethod
    def get_info(self, url, information_schema=None):
        pass

    @abstractmethod
    def get_db_connection(self):
        pass

