from importlib import import_module

from .config_parser import config_parser
from .exceptions import DependenciesNotFoundException
from .utils import INSTALL, manage_dependencies_on_machine


def handle_dependencies(dependencies_config_filepath=None,
        action=INSTALL, dryrun=False):
    """Main function of library which is called
    with dependencies path and a valid action
    """
    if not dependencies_config_filepath:
        raise DependenciesNotFoundException
    try:
        dependencies_module = import_module(dependencies_config_filepath)
    except ImportError:
        raise DependenciesNotFoundException

    machines = config_parser(dependencies_module=dependencies_module, action=action)
    for machine, packages in machines.iteritems():
        manage_dependencies_on_machine(machine, packages, dryrun=dryrun)

    return True
