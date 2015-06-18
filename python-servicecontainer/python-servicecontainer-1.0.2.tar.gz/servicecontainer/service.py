class ServiceException(Exception):
    pass

class ServiceInterface(object):
    @classmethod
    def asService(cls, parameters):
        raise NotImplementedError("please implement this method")

class Service(object):
    name = None
    parameters = None
    service_class = None
    _instance = None

    def __init__(self, name, service_class, parameters):
        if not isinstance(service_class, type):
            raise ServiceException("Please provide class not object for service")
        self.name = name
        self.service_class = service_class
        self.parameters = parameters

    @property
    def instance(self):
        if self._instance is None:
            self._instance = self.service_class(**self.parameters)
        return self._instance