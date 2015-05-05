import os
import sys
import inspect
import argparse

from omnomnom import exceptions
from omnomnom.generics.micro.service import BasicMicroService


parser = argparse.ArgumentParser(description='Omnomnom Service Runner')
parser.add_argument('service', nargs='?')
parser.add_argument(
    '--bind', dest='bind', type=str,
    help='Socket address'
)
parser.add_argument(
    '--log-level', dest='log_level', type=str,
    default='INFO'
)


def import_service(module_name):
    parts = module_name.split(":", 1)
    if len(parts) == 1:
        module_name, obj = module_name, None
    else:
        module_name, obj = parts[0], parts[1]

    try:
        __import__(module_name)
    except ImportError as e:
        if module_name.endswith(".py") and os.path.exists(module_name):
            raise exceptions.MicroServiceRunnerException(
                u"Failed to find service, did you mean '{0}'?".format(
                    module_name[:-3].replace('/', '.')
                )
            )

        raise exceptions.MicroServiceRunnerException(
            u"No module named {0}".format(
                module_name
            )
        )

    module = sys.modules[module_name]

    if not obj:
        # inspect imported module to find service
        is_micro_service = lambda x: inspect.isclass(x) and issubclass(x, BasicMicroService)
        targets = inspect.getmembers(module, predicate=is_micro_service)
        if not targets:
            raise exceptions.MicroServiceRunnerException(
                u"No service instance found in {0}".format(
                    module
                )
            )
        else:
            print targets
    else:
        try:
            cls = getattr(module, obj)
        except AttributeError:
            raise exceptions.MicroServiceRunnerException(
                u"Module {0} does not have attribute {1}".format(
                    module_name, obj
                )
            )
        else:
            return cls


def get_options():
    arguments = parser.parse_args()
    return arguments


def main():
    args = get_options()
    service = import_service(args.service)
    print service