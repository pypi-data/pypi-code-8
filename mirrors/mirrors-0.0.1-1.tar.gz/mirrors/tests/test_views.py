import hashlib
import json
import logging
import os

import jsonschema

from unittest import mock

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import Client

from rest_framework import status
from rest_framework.test import APITestCase

from mirrors import components
from mirrors.models import Component, ComponentAttribute, ComponentRevision
from mirrors.serializers import ComponentSerializer
from mirrors.serializers import ComponentWithDataSerializer
from mirrors.views import ComponentGetterMixin


DT_FORMAT = settings.REST_FRAMEWORK['DATETIME_FORMAT']


class ComponentViewTest(APITestCase):
    fixtures = ['users.json', 'serializer.json']

    def setUp(self):
        self.valid_component = {
            'content_type': 'application/x-markdown',
            'schema_name': 'article',
            'metadata': json.dumps({
                'title': 'Valid component'
            })
        }

        user = User.objects.get(username='test_admin')
        self.client.force_authenticate(user=user)

        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_component(self):
        c = Component.objects.get(
            slug='2014-02-test-component-with-one-named-attribute')
        attr = ComponentAttribute.objects.get(parent=c,
                                              name='my_named_attribute')
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-test-component-with-one-named-attribute'
        })

        res = self.client.get(url)
        self.assertTrue(status.is_success(res.status_code))

        data = json.loads(res.content.decode('UTF-8'))
        self.assertEqual(data['schema_name'], 'schema name')
        self.assertEqual(data['created_at'],
                         c.created_at.strftime(DT_FORMAT))
        self.assertEqual(data['updated_at'],
                         c.updated_at.strftime(DT_FORMAT))
        self.assertEqual(data['slug'],
                         '2014-02-test-component-with-one-named-attribute')
        self.assertEqual(data['content_type'], 'none')
        self.assertEqual(data['metadata']['title'],
                         'test component with a single named attribute')
        self.assertEqual(data['metadata']['author'], 'author one')
        self.assertEqual(len(data['attributes']), 1)
        self.assertIn('my_named_attribute', data['attributes'])

        attribute = data['attributes']['my_named_attribute']
        self.assertEqual(attribute['schema_name'], 'schema name')
        self.assertEqual(attribute['created_at'],
                         attr.child.created_at.strftime(DT_FORMAT))
        self.assertEqual(attribute['slug'], '2014-02-attribute-1')
        self.assertEqual(attribute['content_type'], 'none')
        self.assertEqual(attribute['metadata']['author'], 'attribute author')
        self.assertEqual(attribute['metadata']['title'], 'attribute 1')
        self.assertEqual(len(attribute['attributes']), 0)

    def test_get_404_component(self):
        url = reverse('component-detail', kwargs={
            'slug': '1900-04-no-such-component-here'
        })

        res = self.client.get(url)
        self.assertTrue(res.status_code, 404)

    def test_post_new_component(self):
        url = reverse('component-list')
        self.valid_component['slug'] = 'my-new-slug'

        res = self.client.post(url, self.valid_component)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertEqual(data['schema_name'], 'article')
        self.assertEqual(data['content_type'], 'application/x-markdown')
        self.assertEqual(data['slug'], 'my-new-slug')

        self.assertIn('metadata', data)
        self.assertEqual(data['metadata']['title'], 'Valid component')

    def test_post_new_component_missing_data(self):
        url = reverse('component-list')

        res = self.client.post(url, self.valid_component)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(res.content.decode('UTF-8'))

        self.assertEqual(len(data.keys()), 1)
        self.assertIn('slug', data)
        self.assertEqual(data['slug'], ['This field is required.'])

    def test_post_new_component_invalid_name(self):
        url = reverse('component-list')
        self.valid_component['slug'] = 'not a valid slug'
        res = self.client.post(url, self.valid_component)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('slug', data)
        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['slug'],
                         ["Enter a valid 'slug' consisting of letters, "
                          "numbers, underscores or hyphens."])

    def test_patch_404_component(self):
        url = reverse('component-detail', kwargs={
            'slug': 'doesnt-exist'
        })

        res = self.client.patch(url, {'content_type': 'text/plain'})

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_component_one_change(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-this-is-for-testing-on'
        })

        res = self.client.patch(url, {'content_type': 'text/plain'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content.decode('UTF-8'))

        self.assertEqual(data['schema_name'], 'article')
        self.assertEqual(data['content_type'], 'text/plain')
        self.assertEqual(data['slug'], '2014-02-this-is-for-testing-on')
        self.assertEqual(data['metadata']['title'], 'thing thing thing')

    def test_patch_component_multiple_changes(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-this-is-for-testing-on'
        })

        res = self.client.patch(url, {
            'content_type': 'text/plain',
            'schema_name': 'patched'
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content.decode('UTF-8'))

        self.assertEqual(data['schema_name'], 'patched')
        self.assertEqual(data['content_type'], 'text/plain')
        self.assertEqual(data['slug'], '2014-02-this-is-for-testing-on')
        self.assertEqual(data['metadata']['title'], 'thing thing thing')

    def test_patch_component_not_a_dict(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-this-is-for-testing-on'
        })

        res = self.client.patch(url, "invalid data")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_component_invalid_data(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-this-is-for-testing-on'
        })

        res = self.client.patch(url, {
            'metadata': 3
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertEqual(data, {
            'metadata': ['This field must be a JSON object']
        })

    def test_patch_component_metadata(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-this-is-for-testing-on'
        })

        res = self.client.patch(url, {
            'metadata': {'title': 'updated thing'}
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content.decode('UTF-8'))
        self.assertEqual(data['metadata']['title'], 'updated thing')

    def test_patch_to_rename_component(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-this-is-for-testing-on'
        })

        res = self.client.get(url)
        expected_data = json.loads(res.content.decode('UTF-8'))
        expected_data['slug'] = 'this-is-a-rename-test'
        expected_data['revisions'] = ['this-is-a-rename-test v1']
        # skip checking to make sure the updated date is equal
        del expected_data['updated_at']

        res = self.client.patch(url, {
            'slug': 'this-is-a-rename-test'
        })

        self.assertEqual(res.status_code, status.HTTP_301_MOVED_PERMANENTLY)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('updated_at', data)
        # skip checking to make sure the updated date is equal
        del data['updated_at']

        self.assertTrue(isinstance(data, dict))

        self.assertEqual(data, expected_data)

    def test_patch_to_rename_component_used_name(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-this-is-for-testing-on'
        })

        res = self.client.patch(url, {
            'slug': '2014-02-test-component-mixed-attributes'
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_component(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-this-is-for-testing-on'
        })

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_404_component(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-02-doesnt-exist'
        })

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class ComponentAttributeViewTests(APITestCase):
    fixtures = ['users.json', 'componentattributes.json']

    def setUp(self):
        user = User.objects.get(username='test_admin')
        self.client.force_authenticate(user=user)
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_attribute(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-regular-attribute',
            'name': 'my_attribute'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('child', data)
        self.assertEqual(data['child'], '2014-04-attribute-1')

    def test_get_404_attribute(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-regular-attribute',
            'name': 'no_such_attribute'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_new_attribute(self):
        url = reverse('component-attribute-list', kwargs={
            'slug': '2014-04-component-with-regular-attribute'
        })

        res = self.client.post(url, {'name': 'new_attribute',
                                     'child': '2014-04-attribute-4'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        data = json.loads(res.content.decode('UTF-8'))

        expected = {'name': 'new_attribute',
                    'child': '2014-04-attribute-4',
                    'weight': -1,
                    'parent': '2014-04-component-with-regular-attribute'}

        self.assertDictEqual(data, expected)

    def test_put_attribute(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-regular-attribute',
            'name': 'my_attribute'
        })

        res = self.client.put(url, {'name': 'my_attribute',
                                    'child': '2014-04-attribute-2'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('child', data)
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'my_attribute')
        self.assertEqual(data['child'], '2014-04-attribute-2')

    def test_put_attribute_invalid_type(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-regular-attribute',
            'name': 'my_attribute'
        })

        res = self.client.put(url, 'blah')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('error', data)
        self.assertEqual(data['error'],
                         'ComponentAttribute data must be a list or a dict')

    def test_put_attribute_invalid_data(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-regular-attribute',
            'name': 'my_attribute'
        })

        res = self.client.put(url, {'name': 'my_attribute'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data = json.loads(res.content.decode('UTF-8'))

        self.assertDictEqual(data,  {'error': "['Child must be set']"})

    def test_post_new_attribute_strip_slug(self):
        url = reverse('component-attribute-list', kwargs={
            'slug': '2014-04-component-with-regular-attribute'
        })
        res = self.client.post(url, {'name': 'new_attribute',
                                     'child': '2014-04-attribute-4',
                                     'slug': '2014-04-attribute-4'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_new_attribute_invalid_name(self):
        url = reverse('component-attribute-list', kwargs={
            'slug': '2014-04-component-with-regular-attribute'
        })

        res = self.client.post(url, {'name': '$not a valid name(',
                                     'child': '2014-04-attribute-4'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data = json.loads(res.content.decode('UTF-8'))

        self.assertIn('name', data)
        self.assertEqual(len(data.keys()), 1)
        self.assertEqual(data['name'],
                         ["Enter a valid 'slug' consisting of letters, "
                          "numbers, underscores or hyphens."])

    def test_post_new_attribute_used_name(self):
        url = reverse('component-attribute-list', kwargs={
            'slug': '2014-04-component-with-regular-attribute'
        })

        res = self.client.post(url, {'name': 'my_attribute',
                                     'child': '2014-02-attribute-4'})

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_post_new_attribute_invalid_component_name(self):
        url = reverse('component-attribute-list', kwargs={
            'slug': '2014-04-component-with-regular-attribute'
        })

        res = self.client.post(url, {'name': 'new_attribute',
                                     'child': '#not a valid component name'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(res.content.decode('UTF-8'))

        err = "Object with slug='#not a valid component name' does not exist."
        self.assertDictEqual(data, {'error': {'child': [err]}})

    def test_get_attribute_list(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-list-attribute',
            'name': 'list_attribute'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['child'], '2014-04-attribute-3')
        self.assertEqual(data[1]['child'], '2014-04-attribute-4')

        self.assertEqual(data[0]['weight'], 100)
        self.assertEqual(data[1]['weight'], 200)

    def test_get_404_attribute_list(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-list-attribute',
            'name': 'no-such-attribute'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_attribute_list(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-list-attribute',
            'name': 'list_attribute'
        })

        attribute_list = [{'child': '2014-04-attribute-4', 'weight': 200},
                          {'child': '2014-04-attribute-3', 'weight': 100},
                          {'child': '2014-04-attribute-1', 'weight': 9999}]

        res = self.client.put(url, data=attribute_list)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 3)

        self.assertEqual(data[0]['child'], '2014-04-attribute-3')
        self.assertEqual(data[1]['child'], '2014-04-attribute-4')
        self.assertEqual(data[2]['child'], '2014-04-attribute-1')

        self.assertEqual(data[0]['weight'], 100)
        self.assertEqual(data[1]['weight'], 200)
        self.assertEqual(data[2]['weight'], 9999)

    def test_delete_attribute(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-regular-attribute',
            'name': 'my_attribute'
        })

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_404_attribute(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-regular-attribute',
            'name': 'no-such-slug'
        })

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_attribute_list(self):
        url = reverse('component-attribute-detail', kwargs={
            'slug': '2014-04-component-with-list-attribute',
            'name': 'list_attribute'
        })

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class ComponentDataViewTest(APITestCase):
    fixtures = ['users.json', 'component_data.json']

    def setUp(self):
        self.svg_hash = '01d5a1a9d1452f1b013bfc74da44d52e'
        self.jpeg_hash = '6367446e537b50e363f26e385f47e99d'
        self.md_hash = 'eb867962bfff036e98b5e59dc6153caf'

        user = User.objects.get(username='test_admin')
        self.client.force_authenticate(user=user)

    def test_get_data(self):
        url = reverse('component-data', kwargs={
            'slug': '2014-05-component-with-svg-data'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.get('Content-Type'), 'image/svg+xml')

        md5_hash = hashlib.md5()
        md5_hash.update(res.content)
        self.assertEqual(md5_hash.hexdigest(), self.svg_hash)

    def test_get_data_component_without_data(self):
        url = reverse('component-data', kwargs={
            'slug': '2014-05-component-with-no-data'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_data_with_filename(self):
        url = reverse('component-data', kwargs={
            'slug': '2014-05-component-with-svg-data-and-metadata-filename'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.get('Content-Disposition'),
                         'inline; filename=einfache_zeitung.svg')

    def test_get_data_without_filename(self):
        url = reverse('component-data', kwargs={
            'slug': '2014-05-component-with-svg-data'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.get('Content-Disposition'),
                         'inline; filename=2014-05-component-with-svg-data')

    def test_post_data(self):
        c = Client()
        c.login(username='test_user', password='password1')

        url = reverse('component-data', kwargs={
            'slug': '2014-05-component-with-no-data'
        })
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..',
                                                 'fixtures',
                                                 'binary-data',
                                                 'fake_article.md'))

        component = Component.objects.get(
            slug='2014-05-component-with-no-data')

        with open(file_path, 'rb') as upload_file:
            res = c.post(url, data={'file': upload_file})

            self.assertTrue(res.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(component.revisions.count(), 1)

            rev = component.revisions.first()
            md5_hash = hashlib.md5()
            md5_hash.update(rev.data)
            self.assertEqual(md5_hash.hexdigest(), self.md_hash)

        def test_get_deleted_data(self):
            url = reverse('component-data', kwargs={
                'slug': '2014-02-test-component-with-deleted-data'
            })

            res = self.client.get(url)
            self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class ComponentRevisionViewTest(APITestCase):
    fixtures = ['users.json', 'componentrevisions.json']

    def setUp(self):
        self.valid_component = {
            'content_type': 'application/x-markdown',
            'schema_name': 'article',
            'metadata': json.dumps({
                'title': 'Valid component'
            })
        }

        user = User.objects.get(username='test_admin')
        self.client.force_authenticate(user=user)

    def test_get_component_at_version(self):
        component = Component.objects.get(
            slug='2014-06-component-with-many-revisions')
        revision = ComponentRevision.objects.get(component=component,
                                                 version=3)

        url = reverse('component-revision-detail', kwargs={
            'slug': '2014-06-component-with-many-revisions',
            'version': 3
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertEqual(data['schema_name'], 'none')
        self.assertEqual(data['created_at'],
                         component.created_at.strftime(DT_FORMAT))
        self.assertEqual(data['slug'], '2014-06-component-with-many-revisions')
        self.assertEqual(data['content_type'], 'text/plain')
        self.assertEqual(data['metadata'], {"test": "first metadata"})
        self.assertEqual(len(data['attributes']), 0)

    def test_get_component_data_at_version(self):
        url = reverse('component-revision-data', kwargs={
            'slug': '2014-06-component-with-many-revisions',
            'version': 3
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res['Content-Type'], 'text/plain')

        data = res.content.decode('UTF-8')
        self.assertEqual(data, 'second data')

    def test_get_component_data_at_version_with_filename(self):
        url = reverse('component-revision-data', kwargs={
            'slug': '2014-06-component-with-data-and-filename',
            'version': 1
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res['Content-Type'], 'text/plain')

        data = res.content.decode('UTF-8')
        self.assertEqual(data, 'this is some data')
        self.assertEqual(res.get('Content-Disposition'),
                         'inline; filename=file.txt')

    def test_get_component_data_at_version_no_data(self):
        url = reverse('component-revision-data', kwargs={
            'slug': '2014-05-component-with-no-data',
            'version': 2
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_component_at_404_version(self):
        url = reverse('component-revision-detail', kwargs={
            'slug': '2014-06-component-with-many-revisions',
            'version': 999
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class ComponentRevisionSummaryViewTests(APITestCase):
    fixtures = ['users.json', 'componentrevisions.json']

    def setUp(self):
        user = User.objects.get(username='test_admin')
        self.client.force_authenticate(user=user)

    def test_serialize_revision_summary_with_multiple_type_changes(self):
        component = Component.objects.get(
            slug='2014-06-component-with-revision-with-data-and-metadata'
        )
        revision = component.revisions.first()

        url = reverse('component-revision-list', kwargs={
            'slug': '2014-06-component-with-revision-with-data-and-metadata'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)

        rev = data[0]
        self.assertTrue(isinstance(rev, dict))
        self.assertEqual(rev['version'], 1)
        self.assertEqual(rev['change_date'],
                         revision.created_at.strftime(DT_FORMAT))

        self.assertTrue(isinstance(rev['change_types'], list))
        self.assertEqual(len(rev['change_types']), 2)
        self.assertIn('data', rev['change_types'])
        self.assertIn('metadata', rev['change_types'])

    def test_serialize_revision_summary(self):
        component = Component.objects.get(
            slug='2014-06-component-with-two-revisions')
        revision_1 = component.revisions.all()[0]
        revision_2 = component.revisions.all()[1]

        url = reverse('component-revision-list', kwargs={
            'slug': '2014-06-component-with-two-revisions'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))

        self.assertTrue(isinstance(data, list))
        rev_1 = data[0]
        rev_2 = data[1]

        self.assertTrue(isinstance(rev_1, dict))
        self.assertEqual(rev_1['version'], 1)
        self.assertEqual(rev_1['change_date'],
                         revision_1.created_at.strftime(DT_FORMAT))
        self.assertEqual(rev_1['change_types'], ['metadata'])

        self.assertEqual(rev_2['version'], 2)
        self.assertEqual(rev_2['change_date'],
                         revision_2.created_at.strftime(DT_FORMAT))
        self.assertEqual(rev_2['change_types'], ['data'])

    def test_serialize_revision_summary_no_revisions(self):
        url = reverse('component-revision-list', kwargs={
            'slug': '2014-06-component-with-no-revisions'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class ComponentLockRequestTest(APITestCase):
    fixtures = ['component_lock_data.json', 'users.json']

    def setUp(self):
        # Friendly note:
        # The account 'test_user' is the one that has locked the component
        # 'locked-component'
        user = User.objects.get(username='test_staff')
        self.client.force_authenticate(user=user)

    def test_get_lock_status_unlocked(self):
        url = reverse('component-lock', kwargs={
            'slug': '2014-06-unlocked-component'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_lock_status_locked(self):
        component = Component.objects.get(slug='2014-06-locked-component')
        lock = component.lock
        url = reverse('component-lock', kwargs={
            'slug': '2014-06-locked-component'
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content.decode('UTF-8'))
        self.assertTrue(isinstance(data, dict))

        self.assertEqual(len(data), 4)
        self.assertIn('locked', data)
        self.assertIn('locked_by', data)
        self.assertIn('locked_at', data)
        self.assertIn('lock_ends_at', data)

        self.assertTrue(data['locked'])
        self.assertEqual(data['locked_by'], 'test_user')
        self.assertEqual(data['locked_at'],
                         lock.locked_at.strftime(DT_FORMAT))
        self.assertEqual(data['lock_ends_at'],
                         lock.lock_ends_at.strftime(DT_FORMAT))

    def test_lock_unlocked_component(self):
        url = reverse('component-lock', kwargs={
            'slug': '2014-06-unlocked-component'
        })
        data = {
            'locked': True,
            'lock_duration': 60
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = json.loads(response.content.decode('UTF-8'))
        self.assertEqual(set(data.keys()), {'locked',
                                            'locked_by',
                                            'locked_at',
                                            'lock_ends_at'})
        self.assertTrue(data['locked'])
        self.assertEqual(data['locked_by'], 'test_staff')

    def test_lock_unlocked_component_with_no_duration(self):
        url = reverse('component-lock', kwargs={
            'slug': '2014-06-unlocked-component'
        })
        data = {'locked': True}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lock_locked_by_me_component(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)

        url = reverse('component-lock', kwargs={
            'slug': '2014-06-locked-component'
        })
        put_data = {
            'locked': True,
            'lock_duration': 60
        }

        response = self.client.put(url, put_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unlock_locked_by_me_component(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)

        url = reverse('component-lock', kwargs={
            'slug': '2014-06-locked-component'
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unlock_unlocked_component(self):
        url = reverse('component-lock', kwargs={
            'slug': '2014-06-unlocked-component'
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_locked_component(self):
        user = User.objects.get(username='test_staff')
        self.client.force_authenticate(user=user)

        url = reverse('component-detail', kwargs={
            'slug': '2014-06-locked-component'
        })

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_locked_component(self):
        url = reverse('component-detail', kwargs={
            'slug': '2014-06-locked-component'
        })

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_locked_by_me_component(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)
        url = reverse('component-detail', kwargs={
            'slug': '2014-06-locked-component'
        })

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_locked_by_me_component(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)
        url = reverse('component-detail', kwargs={
            'slug': '2014-06-locked-component'
        })

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ComponentValidityTest(APITestCase):
    fixtures = ['users.json', 'component_validity.json']

    class TestAttributeSchema(components.Component):
        id = 'testattribute'
        schema_title = 'test attribute'
        content_type = ['text/plain']

    class TestComponentSchema(components.Component):
        id = 'testcomponent'
        schema_title = 'test component'
        content_type = ['text/plain']

        required_text = components.StringSchema(required=True)
        optional_text = components.StringSchema()

        required_attribute = components.Attribute('testattribute',
                                                  required=True)
        optional_attribute = components.Attribute('testattribute')

    class TestDataSchema(components.Component):
        id = 'testrequireddata'
        schema_title = 'test component with data'
        content_type = ['text/plain']

        requires_data = True

    def setUp(self):
        self.old_schema_cache = components.ComponentSchemaCache
        components.ComponentSchemaCache = {
            'testcomponent': self.TestComponentSchema(),
            'testattribute': self.TestAttributeSchema(),
            'testrequireddata': self.TestDataSchema()
        }

        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)

        logging.disable(logging.CRITICAL)

    def tearDown(self):
        components.ComponentSchemaCache = self.old_schema_cache
        logging.disable(logging.NOTSET)

    def test_valid_component(self):
        url = reverse('component-validity', kwargs={
            'slug': '2014-06-valid-component-with-optional-text-optional-attri'
            'bute'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('valid', data)
        self.assertEqual(data, {'valid': True})

    def test_valid_component_only_required_stuff(self):
        url = reverse('component-validity', kwargs={
            'slug': '2014-06-valid-component-only-required-fields'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('valid', data)
        self.assertTrue(data['valid'])

    def test_invalid_component_missing_required_metadata(self):
        url = reverse('component-validity', kwargs={
            'slug': '2014-06-invalid-component-missing-required-metadata'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('valid', data)
        self.assertFalse(data['valid'])

    def test_invalid_component_missing_required_attribute(self):
        url = reverse('component-validity', kwargs={
            'slug': '2014-06-invalid-component-missing-required-attribute'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('valid', data)
        self.assertFalse(data['valid'])

    def test_invalid_component_invalid_content_type(self):
        url = reverse('component-validity', kwargs={
            'slug': '2014-06-invalid-component-invalid-content-type'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('valid', data)
        self.assertFalse(data['valid'])

    def test_invalid_component_missing_schema(self):
        url = reverse('component-validity', kwargs={
            'slug': '2014-06-invalid-component-no-such-schema'
        })

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('valid', data)
        self.assertFalse(data['valid'])

    def test_component_with_required_data(self):
        url = reverse('component-validity', kwargs={
            'slug': '2014-06-component-with-required-data'
        })

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('valid', data)
        self.assertTrue(data['valid']),

    def test_invalid_component_missing_required_data(self):
        url = reverse('component-validity', kwargs={
            'slug': '2014-06-component-missing-required-data'
        })

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIn('valid', data)
        self.assertFalse(data['valid'])

    def test_get_component_schemas(self):
        url = reverse('component-schemas')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertEqual(set(data.keys()), {'testattribute',
                                            'testcomponent',
                                            'testrequireddata',
                                            'id'})

        jsonschema.validate({}, data)


class ComponentGetterMixinTest(APITestCase):
    fixtures = ['users.json', 'component_data.json']

    def setUp(self):
        self.getter = ComponentGetterMixin()

    def test_get_no_data_serializer(self):
        self.getter.object = Component.objects.get(
            slug='2014-05-component-with-no-data'
        )
        self.assertEqual(self.getter.get_serializer_class(),
                         ComponentSerializer)

    def test_get_data_serializer(self):
        obj = Component.objects.get(
            slug='2014-05-component-with-svg-data'
        )
        self.getter.kwargs = {'slug': '2014-05-component-with-svg-data'}
        self.getter.get_object = lambda: obj

        self.assertEqual(self.getter.get_serializer_class(),
                         ComponentWithDataSerializer)


class ComponentAutocompleteTest(APITestCase):
    fixtures = ['users.json']

    def setUp(self):
        Component.objects.create(
            slug='2015-01-component-one',
            schema_name='article',
            current_metadata={
                'author': 'Jane Doe',
                'title': 'First Component'
            }
        )
        Component.objects.create(
            slug='2015-02-my-pretty-painting',
            schema_name='article',
            current_metadata={
                'author': 'Janet Smith',
                'title': 'My Pretty Painting'
            }
        )
        Component.objects.create(
            slug='2015-02-the-pretty-painting',
            schema_name='image',
            current_metadata={
                'author': 'Janet Smith',
                'title': 'The Pretty Painting'
            }
        )
        Component.objects.create(
            slug='2015-01-story-about-pain',
            schema_name='article',
            current_metadata={
                'author': 'John Doe',
                'title': 'I leik mudkips'
            }
        )
        Component.objects.create(
            slug='1015-01-my-voyages',
            schema_name='article',
            current_metadata={
                'author': 'Leif Erikson',
                'title': 'I discovered the Americas first!'
            }
        )

        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)

    def test_match_by_slug(self):
        url = reverse('autocomplete')
        res = self.client.get(url, {
            'schema_type': 'article',
            'fields': 'nosuchfield',
            'q': 'compo'
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content.decode('UTF-8'))

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

        expected = {
            'slug': '2015-01-component-one',
            'data_uri': None,
            'metadata': {
                'author': 'Jane Doe',
                'title': 'First Component'
            }
        }
        self.assertDictEqual(data[0], expected)

    def test_too_short_query(self):
        url = reverse('autocomplete')

        res = self.client.get(url, {
            'schema_type': 'article',
            'fields': 'author',
            'q': 'co'
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(res.content.decode('UTF-8'))

        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, {
            'error': 'query too short'
        })

    def test_match_by_author(self):
        url = reverse('autocomplete')

        res = self.client.get(url, {
            'schema_type': 'article',
            'fields': 'author',
            'q': 'jane'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content.decode('UTF-8'))
        self.assertIsInstance(data, list)

        self.assertEqual(len(data), 2)

        expected = [{'slug': '2015-02-my-pretty-painting',
                     'data_uri': None,
                     'metadata': {
                         'author': 'Janet Smith',
                         'title': 'My Pretty Painting'
                     }},
                    {'slug': '2015-01-component-one',
                     'data_uri': None,
                     'metadata': {
                         'author': 'Jane Doe',
                         'title': 'First Component'
                     }}]

        self.assertDictEqual(data[0], expected[0])
        self.assertDictEqual(data[1], expected[1])

    def test_match_by_multiple_fields(self):
        url = reverse('autocomplete')

        res = self.client.get(url, {
            'schema_type': 'article',
            'fields': 'author,title',
            'q': 'lei'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content.decode('UTF-8'))
        self.assertIsInstance(data, list)

        self.assertEqual(len(data), 2)

        expected = [{'slug': '2015-01-story-about-pain',
                     'data_uri': None,
                     'metadata': {
                         'author': 'John Doe',
                         'title': 'I leik mudkips'
                     }},
                    {'slug': '1015-01-my-voyages',
                     'data_uri': None,
                     'metadata': {
                         'author': 'Leif Erikson',
                         'title': 'I discovered the Americas first!'
                     }}]

        self.assertDictEqual(data[0], expected[0])
        self.assertDictEqual(data[1], expected[1])

    def test_no_matches(self):
        url = reverse('autocomplete')

        res = self.client.get(url, {
            'schema_type': 'article',
            'fields': 'author,title',
            'q': 'there is no way this matches anything'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content.decode('UTF-8'))
        self.assertIsInstance(data, list)

        self.assertEqual(len(data), 0)

    def test_missing_schema_type(self):
        url = reverse('autocomplete')

        res = self.client.get(url, {
            'fields': 'author,title',
            'q': 'there is no way this matches anything'
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, {'error': 'Missing required parameter(s)'})

    def test_missing_query_string(self):
        url = reverse('autocomplete')

        res = self.client.get(url, {
            'schema_type': 'article',
            'fields': 'author,title'
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, {'error': 'Missing required parameter(s)'})

    def test_missing_optional_parameters(self):
        url = reverse('autocomplete')

        res = self.client.get(url, {
            'schema_type': 'article',
            'q': 'there is no way this matches anything'
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)


class UserDetailTests(APITestCase):
    def setUp(self):
        self.auth_user = mock.Mock(spec=User)
        self.auth_user.get_username.return_value = 'user123'
        self.auth_user.get_full_name.return_value = 'User Fullname'
        self.auth_user.email = 'user123@fakeemail.com'
        self.auth_user.is_authenticated.return_value = True

    def test_auth_user(self):
        url = reverse('user-detail')
        self.client.force_authenticate(self.auth_user)

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = json.loads(res.content.decode('UTF-8'))
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, {'username': 'user123',
                                    'full_name': 'User Fullname',
                                    'email': 'user123@fakeemail.com',
                                    'is_authenticated': True})
