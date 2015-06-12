from unittest import TestCase

from magnetic.tests.utils import StatsdMixin

from faf import datadog
from faf.tests.test_relayer import connectedRelayerProtocol


class TestDatadogObserver(StatsdMixin, TestCase):

    success_metric = "pfft.metric.use.imperial"
    error_metric = "pfft.metric.use.imperial.error"

    def setUp(self):
        super(TestDatadogObserver, self).setUp()
        self.protocol = connectedRelayerProtocol()
        observer = datadog.observer(
            success_metric=self.success_metric,
            error_metric=self.error_metric,
        )
        self.protocol.factory.notify(observer)

    def test_successful_responses_tag_successfully(self):
        self.protocol.dataReceived("http://localhost/succeed\r\n")
        self.assertIncremented(self.success_metric, exact_tags=["status:200"])
        self.assertNotIncremented(self.error_metric)

    def test_unsuccessful_responses_tag_unsuccessfully(self):
        self.protocol.dataReceived("http://localhost/error\r\n")
        self.assertIncremented(self.error_metric, exact_tags=["status:500"])
        self.assertNotIncremented(self.success_metric)

    def test_error_responses_tag_errors(self):
        self.protocol.dataReceived("http://localhost/unknown\r\n")
        self.assertNotIncremented(self.success_metric)
        self.assertIncremented(self.error_metric)
