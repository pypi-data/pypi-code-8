from collections import defaultdict
import types

from .exceptions import (DependenciesNotFoundException, NoActionDefinedForPackage,
                         StepsNotDefined, NoDestinationDefined, NoPackageNameDefined,
                         NoCallablesGiven, ListNotReceivedFromCallable)
from .utils import INSTALL


def config_parser(dependencies_module, action):
    """Parses the given dependency module and prepares the list of
    packages that must be installed/uninstalled on respective machines.

    dependencies_module_path: path of dependecy module in dotted notation.
    action = INSTALL or UNINSTALL
    """
    #try:
    #    dependencies = import_module(dependencies_module_path)
    #except ImportError:
    #    raise DependenciesNotFoundException

    if not hasattr(dependencies_module, 'DEPENDENCIES'):
        raise DependenciesNotFoundException

    dependencies = dependencies_module.DEPENDENCIES
    endpoints_vs_packages = defaultdict(list)

    for dep in dependencies:
        package_name = dep.get("package_name")
        if not package_name:
            raise NoPackageNameDefined

        package_action = dep.get('action')
        if package_action is None:
            raise NoActionDefinedForPackage(package_name)

        if package_action != action:
            continue

        if action == INSTALL:
            steps = dep.get('install_steps')
        else:
            steps = dep.get('uninstall_steps')
        if not steps:
            raise StepsNotDefined(package_name)

        dep["steps"] = steps

        destinations = dep.get('destinations')
        if not destinations or len(destinations) == 0:
            raise NoDestinationDefined(package_name)

        for destination in destinations:
            destination_enabled = destination.get('enabled', False)
            if not destination_enabled:
                continue

            endpoints_callable = destination.get('server')
            if not endpoints_callable:
                # ignore it
                continue
            if not hasattr(endpoints_callable, '__call__'):
                raise NoCallablesGiven(package_name)

            if type(endpoints_callable) == types.FunctionType:
                dest_endpoints = endpoints_callable()
            else:
                dest_endpoints = endpoints_callable()()

            if not isinstance(dest_endpoints, list):
                raise ListNotReceivedFromCallable(package_name)
            for dest_endpoint in dest_endpoints:
                endpoints_vs_packages[dest_endpoint].append(dep)

    return endpoints_vs_packages
