import yaml
from collections import OrderedDict


SafeDumper = getattr(yaml, 'CSafeDumper', yaml.SafeDumper)
SafeLoader = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)


class OrderedDumper(SafeDumper):
    pass

OrderedDumper.add_representer(OrderedDict, OrderedDumper.represent_dict)


def dump(obj, **kwargs):
    kwargs.setdefault('Dumper', OrderedDumper)
    return yaml.dump(obj, **kwargs)


def load(obj, **kwargs):
    kwargs.setdefault('Loader', SafeLoader)
    return yaml.load(obj, **kwargs)
