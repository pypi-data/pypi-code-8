from collections import defaultdict, OrderedDict
class OrderedDefaultDict(defaultdict, OrderedDict):
  def __init__(self, default, *args, **kwargs):
    defaultdict.__init__(self, default)
    OrderedDict.__init__(self, *args, **kwargs)