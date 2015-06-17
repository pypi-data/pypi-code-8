class NoPackageNameDefined(Exception):
    def __init__(self):
        message = "No Package Name is defined."
        super(NoPackageNameDefined, self).__init__(message)


class DependenciesNotFoundException(Exception):
    def __init__(self):
        message = "DEPENDENCIES dictionary not declared in the dependency config module."
        super(DependenciesNotFoundException, self).__init__(message)


class NoActionDefinedForPackage(Exception):
    def __init__(self, package_name):
        message = "No ACTION defined for {package_name}.".format(package_name=package_name)
        super(NoActionDefinedForPackage, self).__init__(message)


class StepsNotDefined(Exception):
    def __init__(self, package_name):
        message = "No STEPS(install_steps/uninstall_steps) defined for {package_name}.".format(package_name=package_name)
        super(StepsNotDefined, self).__init__(message)

class NoDestinationDefined(Exception):
    def __init__(self, package_name):
        message = "No Destinations defined for {package_name}.".format(package_name=package_name)
        super(NoDestinationDefined, self).__init__(message)

class NoCallablesGiven(Exception):
    def __init__(self, package_name):
        message = "No Callables given for {package_name}.".format(package_name=package_name)
        super(NoCallablesGiven, self).__init__(message)

class ListNotReceivedFromCallable(Exception):
    def __init__(self, package_name):
        message = "Callable didn't return a list of endpoints for  {package_name}.".format(package_name=package_name)
        super(ListNotReceivedFromCallable, self).__init__(message)

class NoMachineUserDefined(Exception):
    def __init__(self, machine_endpoint, package_name):
        message = "No Machine User defined for {machine_endpoint} under \
        {package_name}.".format(machine_endpoint=machine_endpoint, package_name=package_name)
        super(NoMachineUserDefined, self).__init__(message)

class NoMachineKeyDefined(Exception):
    def __init__(self, machine_endpoint, package_name):
        message = "No Machine Key defined for {machine_endpoint} under \
        {package_name}.".format(machine_endpoint=machine_endpoint, package_name=package_name)
        super(NoMachineKeyDefined, self).__init__(message)
