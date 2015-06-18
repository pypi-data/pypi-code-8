from . import Service

class ContainerException(Exception):
    pass

class Container(object):
    _container = []

    def add(self, service):
        if not isinstance(service, Service):
            raise ContainerException("Please only add Service classes")

        if self._get_service(service.name):
            raise ContainerException("Service with the name %s is already in the container" % service.name)

        self._container.append(service)

    def _get_service(self, service_name):
        service = filter(lambda x: True if x.name == service_name else False, self._container)
        if not len(service):
            return None
        return service[0]

    def get(self, service_name):
        service = self._get_service(service_name)
        if service is None:
            return None
        return service.instance

    def list(self):
        return map(lambda x: x.name, self._container)