from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.six import StringIO

from mirrors.models import Component, ComponentAttribute

from mirrors_publisher.exceptions import UnpublishedAttributeError
from mirrors_publisher.management.commands import publish
from mirrors_publisher.filters import ContentFilter


class PublishTest(TestCase):
    def test_negative_year(self):
        with self.assertRaises(CommandError) as context:
            call_command('publish', 'test-component', '-2015', '10')

        self.assertIn('year and month must be valid integers',
                      str(context.exception))

    def test_negative_month(self):
        with self.assertRaises(CommandError) as context:
            call_command('publish', 'test-component', '2015', '-10')

        self.assertIn('year and month must be valid integers',
                      str(context.exception))

    def test_non_integer_year(self):
        with self.assertRaises(CommandError) as context:
            call_command('publish', 'test-component', 'blah', '10')

        self.assertIn('year and month must be valid integers',
                      str(context.exception))

    def test_non_integer_month(self):
        with self.assertRaises(CommandError) as context:
            call_command('publish', 'test-component', '2015', 'blah')

        self.assertIn('year and month must be valid integers',
                      str(context.exception))

    def test_too_few_args(self):
        with self.assertRaises(CommandError) as context:
            call_command('publish', 'test-component', '2015')

        self.assertIn('three arguments expected: slug year month',
                      str(context.exception))

    @mock.patch('mirrors_publisher.management.commands.publish.PublishReceipt')
    @mock.patch('mirrors_publisher.management.commands.publish.Component')
    @mock.patch('mirrors_publisher.filters.ContentFilter')
    @mock.patch.object(publish.Command, '_get_filters')
    def test_publish_with_no_children(self,
                                      p_get_filters,
                                      p_filter,
                                      p_component,
                                      p_receipt):
        p_filter.return_value = mock.Mock(spec=ContentFilter)
        p_get_filters.return_value = [p_filter]
        fake_component = mock.Mock(spec=Component,
                                   year=2015,
                                   month=10,
                                   data=None)
        fake_component.attributes.values_list.return_value = []
        p_component.objects.get.return_value = fake_component

        call_command('publish', 'test-component', 2015, 10)

        p_component.objects.get.assert_called_with(slug='test-component',
                                                   year=2015,
                                                   month=10)
        p_filter.apply.assert_called_once()
        p_receipt.objects.create.assert_called_once()

    @mock.patch('mirrors_publisher.management.commands.publish.Component')
    def test_no_such_component(self, p_component):
        p_component.objects.get = mock.Mock(
            side_effect=Component.DoesNotExist())

        with self.assertRaises(CommandError) as context:
            call_command('publish', 'test-component', '2015', '01')

    def test_get_filters_only_default(self):
        fake_component = mock.Mock(spec=Component,
                                   schema_name='fakeschemaname',
                                   content_type='fakecontenttype')

        cmd = publish.Command()
        filters = cmd._get_filters(fake_component)

        self.assertIsInstance(filters, list)
        self.assertEqual(len(filters), 1)
        self.assertIsInstance(filters[0], ContentFilter)

    @mock.patch('mirrors_publisher.management.commands.publish.Component')
    @mock.patch.object(publish.Command, '_publish_dependency_check')
    def test_depcheck_objectdoesnotexist(self, p_depcheck, p_component):
        p_depcheck.side_effect = ComponentAttribute.DoesNotExist()
        fake_component = mock.Mock(spec=Component)
        p_component.objects.get.return_value = fake_component

        with self.assertRaises(ComponentAttribute.DoesNotExist):
            out = StringIO()
            call_command('publish', 'test-component', '2015', '01', stdout=out)

        self.assertEqual('Unable to get component attribute!\n',
                         out.getvalue())
        p_depcheck.assert_called_once_with(fake_component)
        p_component.objects.get.assert_called_once_with(slug='test-component',
                                                        year=2015,
                                                        month=1)

    @mock.patch('mirrors_publisher.management.commands.publish.Component')
    @mock.patch.object(publish.Command, '_publish_dependency_check')
    def test_depcheck_unpublished(self, p_depcheck, p_component):
        fake_attr = mock.Mock(spec=UnpublishedAttributeError)
        fake_attr.name = 'fake-attribute'
        p_depcheck.side_effect = UnpublishedAttributeError(
            missing_attribute=fake_attr)
        fake_component = mock.Mock(spec=Component)
        p_component.objects.get.return_value = fake_component

        with self.assertRaises(CommandError) as context:
            call_command('publish', 'test-component', '2015', '01')

        p_depcheck.assert_called_once_with(fake_component)
        p_component.objects.get.assert_called_once_with(slug='test-component',
                                                        year=2015,
                                                        month=1)
        self.assertEqual('Unable to publish because component publishing depen'
                         'dencies have not been met: attribute fake-attribute '
                         'not yet published',
                         str(context.exception))


class DependencyCheckTests(TestCase):
    @mock.patch('mirrors_publisher.management.commands.publish.'
                'ComponentAttribute',
                autospec=True)
    @mock.patch('mirrors_publisher.management.commands.publish.Component',
                autospec=True)
    @mock.patch('mirrors_publisher.management.commands.publish.PublishReceipt',
                autospec=True)
    def test_dependency_check_unpublished_children(self,
                                                   p_publishreceipt,
                                                   p_component,
                                                   p_componentattribute):
        p_publishreceipt.objects.filter.return_value = [5, 6, 7]
        fake_component = mock.Mock(spec=Component,
                                   year=2015,
                                   month=10,
                                   data=None)
        fake_component.attributes.values_list.return_value = [2, 3]
        fake_attribute = mock.Mock(spec=ComponentAttribute)
        fake_attribute.name = 'attribute-name'
        p_componentattribute.objects.get.return_value = fake_attribute
        p_publishreceipt.objects.filter.return_value = [3, 4, 5]

        cmd = publish.Command()
        with self.assertRaises(UnpublishedAttributeError) as context:
            cmd._publish_dependency_check(fake_component)

        # self.assertIn('attribute-name', str(context.exception))
        self.assertIsInstance(context.exception.missing_attribute,
                              ComponentAttribute)
        self.assertEqual(context.exception.missing_attribute.name,
                         'attribute-name')

    @mock.patch('mirrors_publisher.management.commands.publish.'
                'ComponentAttribute',
                autospec=True)
    @mock.patch('mirrors_publisher.management.commands.publish.Component',
                autospec=True)
    @mock.patch('mirrors_publisher.management.commands.publish.PublishReceipt',
                autospec=True)
    def test_dependency_check_published_children(self,
                                                 p_publishreceipt,
                                                 p_component,
                                                 p_componentattribute):
        p_publishreceipt.objects.filter.return_value = [5, 6, 7]
        fake_component = mock.Mock(spec=Component,
                                   year=2015,
                                   month=10,
                                   data=None)
        fake_component.attributes.values_list.return_value = [2, 3, 4]
        p_publishreceipt.objects.filter.return_value = [2, 3, 4, 5]

        cmd = publish.Command()
        cmd._publish_dependency_check(fake_component)

    @mock.patch('mirrors_publisher.management.commands.publish.'
                'ComponentAttribute',
                autospec=True)
    @mock.patch('mirrors_publisher.management.commands.publish.Component',
                autospec=True)
    @mock.patch('mirrors_publisher.management.commands.publish.PublishReceipt',
                autospec=True)
    def test_dependency_check_object_not_found(self,
                                               p_publishreceipt,
                                               p_component,
                                               p_componentattribute):
        p_publishreceipt.objects.filter.return_value = [5, 6, 7]
        fake_component = mock.Mock(spec=Component,
                                   year=2015,
                                   month=10,
                                   data=None)
        fake_component.attributes.values_list.return_value = [2, 3]
        p_componentattribute.objects.get = mock.Mock(
            spec=ComponentAttribute,
            side_effect=ComponentAttribute.DoesNotExist()
        )
        p_publishreceipt.objects.filter.return_value = [3, 4, 5]

        cmd = publish.Command()
        with self.assertRaises(ComponentAttribute.DoesNotExist) as context:
            cmd._publish_dependency_check(fake_component)
