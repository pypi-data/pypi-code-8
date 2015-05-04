import datetime
import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase

from mirrors.exceptions import LockEnforcementError
from mirrors.models import validate_is_month, validate_is_year
from mirrors.models import Component
from mirrors.models import ComponentLock
from mirrors.models import ComponentAttribute


class ComponentModelValidatorsTest(TestCase):
    def test_non_int_year(self):
        with self.assertRaises(TypeError):
            validate_is_year('not-an-int')

    def test_negative_number_year(self):
        with self.assertRaises(ValidationError):
            validate_is_year(-1)

    def test_valid_year(self):
        validate_is_year(1900)

    def test_non_int_month(self):
        with self.assertRaises(TypeError):
            validate_is_month('not-an-int')

    def test_out_of_range_month(self):
        with self.assertRaises(ValidationError):
            validate_is_month(0)

        with self.assertRaises(ValidationError):
            validate_is_month(13)

    def test_valid_month(self):
        for i in range(1, 13):
            validate_is_month(i)


class ComponentModelTests(TestCase):
    fixtures = ['components.json']

    def test_get_binary_data(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-multiple-revisions'
        )
        self.assertEqual(c.binary_data, b'this is the second revision')

    def test_get_binary_data_failure(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-no-revisions')
        self.assertEqual(c.binary_data, None)

    def test_get_nonexisttant_data_uri(self):
        c = Component.objects.get(slug='2014-01-test-component-1')
        self.assertIsNone(c.data_uri)

    def test_get_str(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-multiple-revisions')
        self.assertEqual(c.__str__(),
                         '2014-02-test-component-with-multiple-revisions')

    def test_get_metadata(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-multiple-revisions')

        expected_metadata = {
            "title": "component data that has multiple revisions",
            "author": "bobby tables"
        }
        self.assertEqual(c.metadata, expected_metadata)

    def test_get_missing_metadata(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-no-metadata')

        self.assertEqual(c.metadata, {})

    def test_get_metadata_missing_version(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-multiple-revisions')

        with self.assertRaises(IndexError):
            c.metadata_at_version(999)

    def test_get_binary_data_missing_version(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-multiple-revisions')

        with self.assertRaises(IndexError):
            c.binary_data_at_version(999)

    def test_get_binary_data_no_data(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-no-data')

        self.assertIs(c.binary_data_at_version(1), None)

    def test_create_new_conflicting_yyyy_mm_slug(self):
        c = Component(slug='2014-02-test-component-with-no-data',
                      content_type='test_contenttype',
                      schema_name='test_schema')

        with self.assertRaises(IntegrityError):
            c.save()

    def test_create_new_nonconflicting_yyyy_mm_slug(self):
        c = Component(slug='2014-03-test-component-with-no-data',
                      content_type='test_contenttype',
                      schema_name='test_schema')
        c.save()

        new_c = Component.objects.get(
            slug='2014-03-test-component-with-no-data')

        self.assertEqual(c.slug, new_c.slug)
        self.assertEqual(c.content_type, new_c.content_type)
        self.assertEqual(c.schema_name, new_c.schema_name)
        self.assertEqual(c.created_at, new_c.created_at)
        self.assertEqual(c.updated_at, new_c.updated_at)

    # def test_no_year_month(self):
    #     c = Component(slug='test-component-with-no-dates',
    #                   content_type='test_contenttype',
    #                   schema_name='test_schema')

    #     c.save()
    #     self.assertEqual(c.year, None)
    #     self.assertEqual(c.month, None)

    # def test_missing_year(self):
    #     c = Component(slug='test-component-missing-year',
    #                   month=3,
    #                   content_type='test_contenttype',
    #                   schema_name='test_schema')

    #     with self.assertRaises(ValidationError):
    #         c.full_clean()

    # def test_missing_month(self):
    #     c = Component(slug='2014-test-component-missing-year',
    #                   year=2014,
    #                   content_type='test_contenttype',
    #                   schema_name='test_schema')

    #     with self.assertRaises(ValidationError):
    #         c.full_clean()

    def test_deleted_data(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-deleted-data')

        self.assertIsNone(c.binary_data)

    def test_deleted_data_with_new_data(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-deleted-and-restored-data')

        self.assertEqual(c.binary_data, b'this is the second revision')


class ComponentURITests(TestCase):
    fixtures = ['users.json', 'components.json']

    def test_get_data_uri(self):
        expected_url = reverse('component-detail', kwargs={
            'slug': '2014-02-component-with-binary-data',
        }) + '/data'

        c = Component.objects.get(
            slug='2014-02-component-with-binary-data')

        self.assertEqual(c.data_uri, expected_url)


class ComponentLockTests(TestCase):
    fixtures = ['users.json', 'component_lock_data.json']

    def setUp(self):
        self.test_user = User.objects.get(username='test_user')
        self.test_staff = User.objects.get(username='test_staff')

    def test_lock_component(self):
        c = Component.objects.get(slug='2014-06-unlocked-component')
        c.lock_by(self.test_user)

        cl = c.lock
        t_delta = datetime.timedelta(hours=1)
        expected_end_date = cl.locked_at + t_delta

        self.assertIsNot(cl, None)
        self.assertTrue(isinstance(cl, ComponentLock))
        self.assertEqual(cl.locked_by, self.test_user)

        self.assertEqual(cl.lock_ends_at.strftime("%Y-%m-%d %H:%M:%S"),
                         expected_end_date.strftime("%Y-%m-%d %H:%M:%S"))

    def test_lock_locked_component(self):
        c = Component.objects.get(slug='2014-06-locked-component')

        with self.assertRaises(LockEnforcementError):
            c.lock_by(self.test_staff)

    def test_extend_lock(self):
        c = Component.objects.get(slug='2014-06-locked-component')

        cur_end = c.lock.lock_ends_at
        new_end = cur_end + datetime.timedelta(hours=1)

        c.lock.extend_lock(hours=1)

        self.assertEqual(c.lock.lock_ends_at, new_end)

    def test_extend_lock_negative_length(self):
        c = Component.objects.get(slug='2014-06-locked-component')

        with self.assertRaises(ValueError):
            c.lock.extend_lock(hours=-1)

    def test_unlock_component(self):
        c = Component.objects.get(slug='2014-06-locked-component')
        c.unlock(self.test_user)

        self.assertIs(c.lock, None)

    def test_componentlock_str(self):
        c = ComponentLock.objects.get(pk=1)
        self.assertEqual(c.__str__(), '2014-06-locked-component locked by test'
                         '_user until 9999-01-31 01:01:01.001000+00:00')


class ComponentRevisionModelTests(TestCase):
    fixtures = ['components.json']

    def test_new_revision_first(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-no-revisions')

        c.new_revision(data=b'this is a new revision', metadata=json.dumps({
            'title': 'test component with no revisions'
        }))

        cr = c.revisions.order_by('-created_at').first()

        self.assertEqual(c.revisions.count(), 1)
        self.assertEqual(cr.component, c)
        self.assertEqual(bytes(cr.data), b'this is a new revision')

    def test_new_revision_no_data(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-no-revisions')

        with self.assertRaises(ValueError):
            c.new_revision()

    def test_revision_to_str(self):
        c = Component.objects.filter(
            slug='2014-02-test-component-with-multiple-revisions'
        ).first()
        cr = c.revisions.first()

        self.assertEqual(cr.__str__(),
                         '2014-02-test-component-with-multiple-revisions v1')

    def test_delete_revision_with_data(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-deleted-data')
        with self.assertRaises(ValueError):
            c.new_revision(data=b'blahblah', delete_point=True)


class ComponentAttributeModelTests(TestCase):
    fixtures = ['components.json']

    def test_get_attribute(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-multiple-levels-sub-1-2')
        c_2 = c.get_attribute('regular_attr')
        self.assertEqual(c_2.slug,
                         '2014-02-test-component-with-multiple-levels-sub-1')

    def test_get_attribute_list(self):
        c = Component.objects.get(slug='2014-02-component-with-list-attribute')
        attr_list = c.get_attribute('my_list_attr')

        self.assertEqual(len(attr_list), 3)

    def test_get_attribute_list_one_entry(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-list-one-attribute')
        attr_list = c.get_attribute('my_single_list_attr')

        self.assertTrue(isinstance(attr_list, list))
        self.assertEqual(len(attr_list), 1)

        attr = attr_list[0]
        self.assertEqual(attr.slug, '2014-02-attribute-1')

    def test_get_attribute_nonexistent(self):
        c = Component.objects.get(slug='2014-01-test-component-1')

        with self.assertRaises(KeyError):
            c.get_attribute('no-such-attribute')

    def test_new_attribute(self):
        c = Component.objects.get(slug='2014-02-component-with-list-attribute')
        c_2 = Component.objects.get(slug='2014-01-test-component-1')

        with self.assertRaises(ComponentAttribute.DoesNotExist):
            ComponentAttribute.objects.get(parent=c, child=c_2)

        c.new_attribute('new_attribute_name', c_2)

        ca = c.attributes.get(parent=c, child=c_2)
        self.assertEqual(ca.weight, -1)
        self.assertEqual(ca.name, 'new_attribute_name')

    def test_new_attribute_None_child(self):
        c = Component.objects.get(slug='2014-01-test-component-1')

        with self.assertRaises(ValueError):
            c.new_attribute('subcomponent', None)

    def test_new_attribute_self_child(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-one-attribute')

        with self.assertRaises(ValueError):
            c.new_attribute('selfcomponent', c)

    def test_new_attribute_illegal_name(self):
        c = Component.objects.get(slug='2014-01-test-component-1')
        c_2 = Component.objects.get(slug='2014-02-attribute-1')

        with self.assertRaises(KeyError):
            c.new_attribute('s nstubcomponent', c_2)

        with self.assertRaises(KeyError):
            c.new_attribute('-snth', c_2)

        with self.assertRaises(KeyError):
            c.new_attribute('snth$', c_2)

    def test_new_attribute_legal_names(self):
        c = Component.objects.get(slug='2014-01-test-component-1')
        c_2 = Component.objects.get(slug='2014-02-attribute-1')

        c.new_attribute('x', c_2)
        c.new_attribute('aoesnuthoaue', c_2)
        c.new_attribute('23eonth8', c_2)
        c.new_attribute('aeoutns-2342e', c_2)

        self.assertEqual(c.attributes.filter(name='x').count(), 1)
        self.assertEqual(c.attributes.filter(name='aoesnuthoaue').count(), 1)
        self.assertEqual(c.attributes.filter(name='23eonth8').count(), 1)
        self.assertEqual(c.attributes.filter(name='aeoutns-2342e').count(), 1)

    def test_new_attribute_creates_list(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-one-attribute')
        c_2 = Component.objects.get(slug='2014-02-attribute-2')

        c.new_attribute('my_attribute', c_2, 50)

        self.assertEqual(c.attributes.filter(name='my_attribute').count(), 2)

    def test_get_str_on_single_attribute(self):
        ca = ComponentAttribute.objects.get(pk=10)
        self.assertEqual(ca.__str__(), '2014-02-test-component-with-one-attri'
                         'bute[my_attribute] = 2014-02-attribute-1')

    def test_get_str_on_list_attribute(self):
        ca = ComponentAttribute.objects.get(pk=7)
        e_str = ('2014-02-component-with-list-attribute[my_list_attr,500] '
                 '-> 2014-02-attribute-1')
        self.assertEqual(ca.__str__(), e_str)
