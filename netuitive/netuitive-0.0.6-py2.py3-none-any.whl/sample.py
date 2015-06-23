
class Sample(object):

    """A data point of the Metric

    Args:
        metricId: The name of the metric
        timestamp: The timestamp of the sample
        val: The value of the sample

    """

    def __init__(self, metricId, timestamp, val):
        self.metricId = metricId
        self.timestamp = timestamp
        self.val = val
