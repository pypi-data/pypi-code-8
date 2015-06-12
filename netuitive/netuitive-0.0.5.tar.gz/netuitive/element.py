from .attribute import Attribute
from .metric import Metric
from .sample import Sample
from .tag import Tag


class Element(object):

    """
    An entity that represents the host that the agent runs on
    """

    def __init__(self, ElementType='SERVER'):
        self.type = ElementType
        self.tags = []
        self.attributes = []
        self.metrics = []
        self.samples = []

    def add_attribute(self, name, value):
        self.attributes.append(Attribute(name, value))

    def add_tag(self, name, value):
        self.tags.append(Tag(name, value))

    def add_sample(self, metricId, timestamp, value, metricType=None, host=None):
        """
        add a metric sample
        """

        self.id = host
        self.name = host
        self.metrics.append(Metric(metricId, metricType))
        self.samples.append(Sample(metricId, timestamp * 1000, value))

    def clear_samples(self):
        self.metrics = []
        self.samples = []
