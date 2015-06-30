import yaml
from collections import OrderedDict
from .formatters import BytesType, PercType, TimeType


SafeDumper = getattr(yaml, 'CSafeDumper', yaml.SafeDumper)
SafeLoader = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)


class OrderedDumper(SafeDumper):
    pass

OrderedDumper.add_representer(OrderedDict, OrderedDumper.represent_dict)
OrderedDumper.add_representer(BytesType, OrderedDumper.represent_float)
OrderedDumper.add_representer(PercType, OrderedDumper.represent_float)
OrderedDumper.add_representer(TimeType, OrderedDumper.represent_float)


class HumanizedDumper(OrderedDumper):

    def represent_humanized(self, data):
        data = data.human
        return self.represent_scalar(u'tag:yaml.org,2002:str', data)

HumanizedDumper.add_representer(BytesType, HumanizedDumper.represent_humanized)
HumanizedDumper.add_representer(PercType, HumanizedDumper.represent_humanized)
HumanizedDumper.add_representer(TimeType, HumanizedDumper.represent_humanized)


def dump(obj, **kwargs):
    if kwargs.pop('humanize', False):
        kwargs.setdefault('Dumper', HumanizedDumper)
    kwargs.setdefault('Dumper', OrderedDumper)
    return yaml.dump(obj, **kwargs)


def load(obj, **kwargs):
    kwargs.setdefault('Loader', SafeLoader)
    return yaml.load(obj, **kwargs)
