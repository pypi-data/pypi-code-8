from importlib import import_module

from .config_parser import config_parser
from .exceptions import DependenciesNotFoundException
from .utils import INSTALL, manage_dependencies_on_machine, print_packages


def handle_dependencies(dependencies_config=None,
        action=INSTALL, dryrun=False):
    """Main function of library which is called
    with dependencies path and a valid action
    """
    machines = config_parser(dependencies_config=dependencies_config,
                             action=action)
    # this returns {'endpoint':{'machine':object, 'packages': []}}
    if dryrun:
        print_packages(machines)
        return True

    for endpoint, details in machines.iteritems():
        machine_obj = details["machine"]
        packages = details["packages"]
        manage_dependencies_on_machine(machine_obj, packages)

    return True

def handle_dependencies_file(dependencies_config_filepath=None,
        action=INSTALL, dryrun=False):
    """Takes dependency config file"""
    if not dependencies_config_filepath:
        raise DependenciesNotFoundException
    try:
        dependencies_module = import_module(dependencies_config_filepath)
    except ImportError:
        raise DependenciesNotFoundException

    if not hasattr(dependencies_module, 'DEPENDENCIES'):
        raise DependenciesNotFoundException

    dependencies_config = dependencies_module.DEPENDENCIES

    handle_dependencies(dependencies_config=dependencies_config, action=action,
            dryrun=dryrun)
