import datetime
import json

from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.utils.timezone import utc

from mirrors.models import Component
from mirrors.serializers import ComponentSerializer
from mirrors.serializers import ComponentWithDataSerializer

from mirrors_publisher import backend_adapters
from mirrors_publisher.filters import ContentFilter
from mirrors_publisher.models import PublishReceipt


class ContentFilterTest(TestCase):
    @mock.patch('mirrors_publisher.filters.PublishReceipt')
    @mock.patch('mirrors_publisher.filters.ComponentSerializer')
    @mock.patch('mirrors_publisher.backend_adapters.get_adapter')
    @mock.patch('os.path.join')
    def test_with_no_data(self, p_join, p_get_adapter, p_serializer,
                          p_receipt):
        component_attrs = {'metadata': {'fake': 'metadata'},
                           'binary_data': None,
                           'slug': 'test-slug',
                           'year': 2015,
                           'month': 1}
        p_component = mock.MagicMock(autospec=Component, **component_attrs)
        p_join.return_value = 'patched_path'

        mock_adapter = mock.Mock(autospec=backend_adapters.BackendAdapter)
        p_get_adapter.return_value = mock_adapter
        p_serializer.return_value = mock.Mock(autospec=ComponentSerializer,
                                              data={'fake': 'metadata'})

        mock_receipt = mock.Mock(spec=PublishReceipt)
        mock_receipt.publish_datetime = datetime.datetime.utcnow()

        pr_filter_order_by = mock.Mock()
        pr_filter_order_by.first.return_value = mock_receipt

        pr_filter = mock.Mock()
        pr_filter.order_by.return_value = pr_filter_order_by

        p_receipt.objects.filter.return_value = pr_filter

        content_filter = ContentFilter()
        content_filter.apply(p_component)

        dateline_str = mock_receipt.publish_datetime.strftime(
            settings.REST_FRAMEWORK['DATETIME_FORMAT'])

        p_join.assert_has_calls([mock.call('2015', '01', 'test-slug'),
                                 mock.call('patched_path', 'index.json')])
        self.assertEqual(len(p_join.mock_calls), 2)

        mock_adapter.put.assert_called_once_with(
            'patched_path',
            bytes(json.dumps({'fake': 'metadata',
                              'dateline': dateline_str}),
                  'UTF-8'))

    @mock.patch('mirrors_publisher.filters.PublishReceipt')
    @mock.patch('mirrors_publisher.filters.ComponentWithDataSerializer')
    @mock.patch('mirrors_publisher.backend_adapters.get_adapter')
    @mock.patch('os.path.join')
    def test_with_data(self, p_join, p_get_adapter, p_serializer, p_receipt):
        component_attrs = {'metadata': {'fake': 'metadata'},
                           'binary_data': bytes('data', 'UTF-8'),
                           'slug': 'test-slug',
                           'year': 2015,
                           'month': 1}
        p_component = mock.MagicMock(autospec=Component, **component_attrs)
        p_join.return_value = 'patched_path'

        mock_adapter = mock.Mock(autospec=backend_adapters.BackendAdapter)
        p_get_adapter.return_value = mock_adapter
        p_serializer.return_value = mock.Mock(
            autospec=ComponentWithDataSerializer,
            data={'fake': 'metadata'})

        mock_receipt = mock.Mock(spec=PublishReceipt)
        mock_receipt.publish_datetime = datetime.datetime.utcnow()

        pr_filter_order_by = mock.Mock()
        pr_filter_order_by.first.return_value = mock_receipt

        pr_filter = mock.Mock()
        pr_filter.order_by.return_value = pr_filter_order_by

        p_receipt.objects.filter.return_value = pr_filter

        content_filter = ContentFilter()
        content_filter.apply(p_component)

        p_join.assert_has_calls([mock.call('2015', '01', 'test-slug'),
                                 mock.call('patched_path', 'data'),
                                 mock.call('patched_path', 'index.json')])
        self.assertEqual(len(p_join.mock_calls), 3)

        dateline_str = mock_receipt.publish_datetime.strftime(
            settings.REST_FRAMEWORK['DATETIME_FORMAT'])

        mock_adapter.put.assert_has_calls(
            [mock.call('patched_path', bytes('data', 'UTF-8')),
             mock.call('patched_path', bytes(json.dumps({
                 'fake': 'metadata',
                 'dateline': dateline_str}), 'UTF-8'))])
        self.assertEqual(len(mock_adapter.put.mock_calls), 2)

    @mock.patch('mirrors_publisher.filters.datetime')
    @mock.patch('mirrors_publisher.filters.PublishReceipt')
    @mock.patch('mirrors_publisher.filters.ComponentWithDataSerializer')
    @mock.patch('mirrors_publisher.backend_adapters.get_adapter')
    @mock.patch('os.path.join')
    def test_no_dateline(self, p_join, p_get_adapter, p_serializer, p_receipt,
                         p_datetime):
        component_attrs = {'metadata': {'fake': 'metadata'},
                           'binary_data': bytes('data', 'UTF-8'),
                           'slug': 'test-slug',
                           'year': 2015,
                           'month': 1}
        p_component = mock.MagicMock(autospec=Component, **component_attrs)
        p_join.return_value = 'patched_path'

        mock_adapter = mock.Mock(autospec=backend_adapters.BackendAdapter)
        p_get_adapter.return_value = mock_adapter
        p_serializer.return_value = mock.Mock(
            autospec=ComponentWithDataSerializer,
            data={'fake': 'metadata'})

        p_receipt.objects.filter.side_effect = PublishReceipt.DoesNotExist()

        mock_utc_time = mock.Mock()
        mock_utc_time.replace.return_value = datetime.datetime(
            2015, 1, 1).replace(tzinfo=utc)
        p_datetime.datetime.utcnow.return_value = mock_utc_time

        content_filter = ContentFilter()
        content_filter.apply(p_component)

        dateline_str = mock_utc_time.replace().strftime(
            settings.REST_FRAMEWORK['DATETIME_FORMAT'])

        p_join.assert_has_calls([mock.call('2015', '01', 'test-slug'),
                                 mock.call('patched_path', 'data'),
                                 mock.call('patched_path', 'index.json')])
        self.assertEqual(len(p_join.mock_calls), 3)

        mock_adapter.put.assert_has_calls(
            [mock.call('patched_path', bytes('data', 'UTF-8')),
             mock.call('patched_path', bytes(
                 json.dumps({'fake': 'metadata',
                             'dateline': dateline_str}),
                 'UTF-8'))])

        self.assertEqual(len(mock_adapter.put.mock_calls), 2)
