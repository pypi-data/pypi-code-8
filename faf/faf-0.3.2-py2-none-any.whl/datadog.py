from __future__ import absolute_import

try:
    from datadog import statsd
except ImportError:
    from statsd import statsd


def observer(success_metric, error_metric, statsd=statsd, sample_rate=0.1):
    """
    Create an ILogObserver that will observe to the given Datadog metrics.

    """

    def observe(event):
        response = event.get("response")
        if response is None:
            statsd.increment(error_metric, sample_rate=sample_rate)
            return

        status = response.code
        if status >= 400:
            metric = error_metric
        else:
            metric = success_metric
        tags = ["status:{0}".format(status)]
        statsd.increment(metric, tags=tags, sample_rate=sample_rate)
    return observe
