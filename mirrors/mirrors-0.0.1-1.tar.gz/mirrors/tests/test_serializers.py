import json
from unittest import mock

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User

from rest_framework import serializers
from rest_framework.test import APITestCase

from mirrors.models import Component
from mirrors.models import ComponentAttribute
from mirrors.models import ComponentRevision
from mirrors.serializers import AutocompleteComponentSerializer
from mirrors.serializers import ComponentSerializer
from mirrors.serializers import ComponentWithDataSerializer
from mirrors.serializers import ComponentAttributeSerializer
from mirrors.serializers import ComponentRevisionSerializer
from mirrors.serializers import UserSerializer


DT_FORMAT = settings.REST_FRAMEWORK['DATETIME_FORMAT']


class ComponentResourceTests(APITestCase):
    fixtures = ['serializer.json']

    def _has_attribute(self, content, name):
        return name in content['attributes'].keys()

    def _get_attribute(self, content, name):
        return content['attributes'][name]

    def test_serialize_component_resource(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-no-attributes')
        content = ComponentSerializer(c).data

        self.assertTrue(isinstance(content, dict))
        self.assertEqual(set(content.keys()), {'slug',
                                               'content_type',
                                               'schema_name',
                                               'metadata',
                                               'attributes',
                                               'created_at',
                                               'revisions',
                                               'updated_at'})

        self.assertEqual(content['slug'],
                         '2014-02-test-component-with-no-attributes')
        self.assertEqual(content['content_type'], 'application/x-markdown')
        self.assertEqual(content['schema_name'], 'article')
        self.assertEqual(content['metadata'], {
            "title": "test component with no attributes",
            "description": "this is a test article"
        })

    def test_serialize_component_with_attribute(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-one-named-attribute')
        content = ComponentWithDataSerializer(c).data

        self.assertEqual(content['slug'],
                         '2014-02-test-component-with-one-named-attribute')
        self.assertIn('attributes', content)
        self.assertTrue(self._has_attribute(content, 'my_named_attribute'))

        attribute = self._get_attribute(content, 'my_named_attribute')
        self.assertTrue(isinstance(attribute, dict))

    def test_serialize_component_with_attribute_list(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-list-attribute')
        content = ComponentWithDataSerializer(c).data

        self.assertEqual(content['slug'], '2014-02-test-component-with-list-at'
                         'tribute')
        self.assertTrue(self._has_attribute(content, 'my_list_attribute'))

        attribute = self._get_attribute(content, 'my_list_attribute')

        self.assertTrue(isinstance(attribute, list))
        self.assertEqual(len(attribute), 3)

        found_slugs = [x['slug'] for x in attribute]
        expected_slugs = ['2014-02-attribute-4',
                          '2014-02-attribute-3',
                          '2014-02-attribute-1']

        for e in zip(found_slugs, expected_slugs):
            self.assertEqual(e[0], e[1])

    def test_serialize_component_with_attribute_list_one_item(self):
        c = Component.objects.get(slug='2015-07-attribute-with-one-item-list')
        content = ComponentSerializer(c).data

        self.assertEqual(content['slug'],
                         '2015-07-attribute-with-one-item-list')
        self.assertTrue(self._has_attribute(content, 'my_list_attribute'))

        attribute = self._get_attribute(content, 'my_list_attribute')

        self.assertTrue(isinstance(attribute, list))
        self.assertEqual(len(attribute), 1)

    def test_serialize_component_with_empty_attribute_list(self):
        c = Component.objects.get(slug='2015-07-attribute-with-empty-list')
        content = ComponentSerializer(c).data

        self.assertEqual(content['slug'], '2015-07-attribute-with-empty-list')
        self.assertTrue(self._has_attribute(content, 'empty_list_attribute'))

        attribute = self._get_attribute(content, 'empty_list_attribute')

        self.assertTrue(isinstance(attribute, list))
        self.assertEqual(len(attribute), 0)

    def test_serialize_component_with_empty_single_attribute(self):
        c = Component.objects.get(slug='2015-07-attribute-with-empty-object')
        content = ComponentSerializer(c).data

        self.assertEqual(content['slug'],
                         '2015-07-attribute-with-empty-object')
        self.assertTrue(self._has_attribute(content, 'empty_object_attribute'))

        attribute = self._get_attribute(content, 'empty_object_attribute')
        self.assertIs(attribute, None)

    def test_serialize_component_with_mixed_attributes(self):
        c = Component.objects.get(
            slug='2014-02-test-component-mixed-attributes')
        content = ComponentWithDataSerializer(c).data

        self.assertEqual(content['slug'],
                         '2014-02-test-component-mixed-attributes')
        self.assertTrue(self._has_attribute(content, 'my_list_attribute'))
        self.assertTrue(self._has_attribute(content, 'my_attribute'))

        list_attr = self._get_attribute(content, 'my_list_attribute')
        named_attr = self._get_attribute(content, 'my_attribute')

        self.assertTrue(isinstance(list_attr, list))
        self.assertEqual(len(list_attr), 2)

    def test_transform_metadata_from_string(self):
        c = Component.objects.get(
            slug='2014-02-test-component-mixed-attributes')
        serializer = ComponentWithDataSerializer(c)
        metadata_str = json.dumps({'test': 'value'})

        result = serializer.transform_metadata(serializer, metadata_str)
        self.assertEqual(result, {'test': 'value'})

    def test_transform_metadata_from_dict(self):
        c = Component.objects.get(
            slug='2014-02-test-component-mixed-attributes')
        serializer = ComponentWithDataSerializer(c)
        metadata_dict = {'test': 'value'}

        result = serializer.transform_metadata(None, metadata_dict)
        self.assertEqual(result, {'test': 'value'})

    def test_validate_non_string_or_dict_metadata(self):
        c = Component.objects.get(
            slug='2014-02-test-component-mixed-attributes')
        serializer = ComponentWithDataSerializer(c)

        with self.assertRaises(serializers.ValidationError):
            serializer.validate_metadata({'metadata': 32}, 'metadata')


class ComponentAttributeResourceTests(APITestCase):
    fixtures = ['users.json', 'componentattributes.json']

    def test_serialize_single_attribute(self):
        parent = Component.objects.filter(
            slug='2014-04-component-with-regular-attribute').first()

        ca = ComponentAttribute.objects.filter(parent=parent).first()
        content = ComponentAttributeSerializer(ca).data

        self.assertIn('name', content)
        self.assertIn('child', content)

        self.assertEqual(content['child'], '2014-04-attribute-1')
        self.assertEqual(content['name'], 'my_attribute')

    def test_serialize_list_attribute(self):
        cas = ComponentAttribute.objects.filter(
            name='list_attribute').order_by('weight')
        content = ComponentAttributeSerializer(cas, many=True).data

        self.assertTrue(isinstance(content, list))
        self.assertEqual(len(content), 2)

        attr_1 = content[0]
        attr_2 = content[1]

        expected_1 = {'parent': cas[0].parent.slug,
                      'child': '2014-04-attribute-3',
                      'name': 'list_attribute',
                      'weight': 100}
        expected_2 = {'parent': cas[0].parent.slug,
                      'child': '2014-04-attribute-4',
                      'name': 'list_attribute',
                      'weight': 200}

        self.assertDictEqual(attr_1, expected_1)
        self.assertDictEqual(attr_2, expected_2)

    def test_serialize_empty_single_attribute(self):
        parent = Component.objects.get(
            slug='2015-07-attribute-with-empty-object')

        ca = ComponentAttribute.objects.filter(parent=parent).first()
        content = ComponentAttributeSerializer(ca).data

        expected = {'parent': '2015-07-attribute-with-empty-object',
                    'name': 'empty_object_attribute',
                    'child': None,
                    'weight': -1}

        self.assertDictEqual(content, expected)

    def test_serialize_empty_list_attribute(self):
        parent = Component.objects.get(
            slug='2015-07-attribute-with-empty-list')

        ca = ComponentAttribute.objects.filter(parent=parent).first()
        content = ComponentAttributeSerializer(ca).data

        expected = {'parent': '2015-07-attribute-with-empty-list',
                    'name': 'empty_list_attribute',
                    'child': [],
                    'weight': 0}

        self.assertDictEqual(content, expected)


class ComponentRevisionResourceTests(APITestCase):
    fixtures = ['users.json', 'componentrevisions.json']

    def test_serialize_revision_with_multiple_type_changes(self):
        c_rev = ComponentRevision.objects.get(pk=4)
        rev = ComponentRevisionSerializer(c_rev).data

        self.assertTrue(isinstance(rev, dict))
        self.assertEqual(rev['version'], 1)
        self.assertEqual(str(rev['change_date']),
                         c_rev.created_at.strftime(DT_FORMAT))

        self.assertTrue(isinstance(rev['change_types'], list))
        self.assertEqual(len(rev['change_types']), 2)
        self.assertIn('data', rev['change_types'])
        self.assertIn('metadata', rev['change_types'])

    def test_serialize_revision_summary(self):
        c_rev_1 = ComponentRevision.objects.get(pk=3)
        c_rev_2 = ComponentRevision.objects.get(pk=5)
        rev_1 = ComponentRevisionSerializer(c_rev_1).data
        rev_2 = ComponentRevisionSerializer(c_rev_2).data

        self.assertTrue(isinstance(rev_1, dict))
        self.assertEqual(rev_1['version'], 1)
        self.assertEqual(str(rev_1['change_date']),
                         c_rev_1.created_at.strftime(DT_FORMAT))
        self.assertEqual(rev_1['change_types'], ['metadata'])

        self.assertEqual(rev_2['version'], 2)
        self.assertEqual(str(rev_2['change_date']),
                         c_rev_2.created_at.strftime(DT_FORMAT))
        self.assertEqual(rev_2['change_types'], ['data'])


class AutocompleteComponentSerializerTests(APITestCase):
    def test_autocomplete_component(self):
        component = Component.objects.create(slug='2015-01-test-component')
        component.new_revision(metadata={
            'title': 'component title',
            'tags': ['tag_1', 'tag_2']
        })

        expected = {
            'slug': '2015-01-test-component',
            'data_uri': None,
            'metadata': {
                'title': 'component title',
                'tags': ['tag_1', 'tag_2']
            }
        }

        data = AutocompleteComponentSerializer(component).data

        # for key in data:
        #     self.assertEqual(data[key], expected[key])
        self.assertDictEqual(data, expected)


class UserSerializerTests(APITestCase):
    def setUp(self):
        self.auth_user = mock.Mock(spec=User)
        self.auth_user.get_username.return_value = 'user123'
        self.auth_user.get_full_name.return_value = 'User Fullname'
        self.auth_user.email = 'user123@fakeemail.com'
        self.auth_user.is_authenticated.return_value = True

        self.anon_user = mock.Mock(spec=AnonymousUser)
        self.anon_user.is_authenticated.return_value = False

    def test_authenticated_user(self):
        serializer = UserSerializer(self.auth_user)
        expected_data = {'username': 'user123',
                         'full_name': 'User Fullname',
                         'email': 'user123@fakeemail.com',
                         'is_authenticated': True}

        self.assertDictEqual(serializer.data, expected_data)

        self.auth_user.get_username.assert_called_once_with()
        self.auth_user.get_full_name.assert_called_once_with()
        self.assertEqual(self.auth_user.is_authenticated.call_count, 4)

    def test_anonymous_user(self):
        serializer = UserSerializer(self.anon_user)
        expected_data = {'username': '',
                         'full_name': '',
                         'email': '',
                         'is_authenticated': False}

        self.assertDictEqual(serializer.data, expected_data)
        self.assertEqual(self.anon_user.is_authenticated.call_count, 4)
