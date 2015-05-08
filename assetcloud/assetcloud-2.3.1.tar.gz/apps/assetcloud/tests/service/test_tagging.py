from assetcloud.tests.service.utils import LoggedInTestCase
from .utils import TestCase, create_asset, create_account, RoleTest, create_admin, create_viewer, create_tag, AdminLoggedInTestCase
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from assetcloud.models import ProxyTag
from .test_actions import make_asset_ids


def extract_tags_from_html(html_list):
    return [tag[tag.index('?') + 6:tag.rindex('class="tag"') - 2].replace('&quot;', '')
            for tag in html_list]


def make_post_data(tags, assets):
    data = make_asset_ids(*assets)
    data['tags'] = ','.join(tags)
    return data


def post_tags(client, url, tags, assets):
    data = make_post_data(tags, assets)
    return client.post(url, data=data)


def post_add_tags(client, tags_to_add, assets):
    url = reverse('asset_add_tags_action')
    return post_tags(client, url, tags_to_add, assets)


def post_delete_tags(client, tags_to_delete, assets):
    url = reverse('asset_delete_tags_action')
    return post_tags(client, url, tags_to_delete, assets)


class TaggingTests(TestCase):
    """
    Test asset tagging.
    """

    class RoleTestCreateTags(RoleTest):
        """
        Ensure that we can create tags on an asset.
        """

        can = ['editor', 'admin']

        def when(self, test):
            self.tags_to_add = {u'foo', u'bar', u'baz'}
            self.asset = create_asset(account=test.account)

            # Ensure there are no tags on the asset to start with
            tags = set(self.asset.tags.all())
            test.assertEquals(tags, set())

            # Post some tags to the asset
            return post_add_tags(test.client, self.tags_to_add, [self.asset])

        def role_can(self, test, response):
            # Ensure the response is as expected
            tags = set(extract_tags_from_html(json.loads(response.content)))
            test.assertEquals(tags, self.tags_to_add)

            # Ensure the tags have been created
            tags = set([tag.name for tag in self.asset.tags.all()])
            test.assertEquals(tags, self.tags_to_add)

    class RoleTestDeleteTags(RoleTest):
        """
        Ensure tags can be deleted.
        """
        can = ['editor', 'admin']

        def when(self, test):
            self.tags_to_delete = {u'foo'}
            self.existing_tags = {u'foo', u'bar', u'baz'}
            self.asset = create_asset(tags=self.existing_tags,
                                      account=test.account)

            # Delete a tag from the asset
            return post_delete_tags(test.client, self.tags_to_delete, [self.asset])

        def role_can(self, test, response):
            # Ensure the response is as expected
            tags = set(extract_tags_from_html(json.loads(response.content)))
            test.assertEquals(tags, self.tags_to_delete)

            # Ensure the tags have been deleted
            tags = set([tag.name for tag in self.asset.tags.all()])
            test.assertEquals(tags, self.existing_tags - self.tags_to_delete)


class SlowTaggingTests(TestCase):
    tags = ['slow']

    def test_tag_case_is_preserved(self):
        tags_to_add = {u'foo', u'Foo', u'FOO'}
        expected_tags = {u'foo', u'Foo', u'FOO'}
        asset = create_asset()
        self.client.login(asset.added_by)

        # Post some tags to the asset
        response = post_add_tags(self.client, tags_to_add, [asset])

        # Ensure the response is as expected
        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertEquals(tags, expected_tags)

        # Ensure that lowercased tags have been created
        tags = set([tag.name for tag in asset.tags.all()])
        self.assertEquals(tags, expected_tags)

    def test_only_created_tags_are_returned(self):
        """
        Ensure that when we add a set of tags, the response only contains
        any tags which were created, and does not return existing tags.
        """
        tags_to_add = {u'foo', u'bar', u'baz'}
        existing_tags = {u'foo'}
        expected_tags = {u'bar', u'baz'}
        asset = create_asset(tags=existing_tags)
        self.client.login(asset.added_by)

        # Post some tags to the asset
        response = post_add_tags(self.client, tags_to_add, [asset])

        # Ensure the response is as expected
        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertSetEqual(tags, expected_tags)

    def test_only_created_tags_are_returned_multiple_assets(self):
        """
        Ensure that when we add a set of tags to multiple assets, the
        response only contains any tags which were created (for at least one
        asset), and does not return existing tags.

        This behaviour is necessary to prevent it being possible to add the
        same tag to a set of assets twice, resulting in two tag indicators on
        the page, and then click the delete button for one of them which
        results in the tag being removed from the assets even though it looks
        like they should still have the tag because there is still one tag
        indicator on the page
        (https://github.com/brightinteractive/assetcloud/issues/76).
        """
        tags_to_add = {u'foo', u'bar', u'baz'}
        # 'bar' will be added to asset1, but not asset2, and 'baz' will be
        # added to both of them
        expected_tags = {u'bar', u'baz'}
        asset1 = create_asset(tags={u'foo'})
        asset2 = create_asset(tags={u'foo', 'bar'}, user=asset1.added_by)
        self.client.login(asset1.added_by)

        # Post some tags to the asset
        response = post_add_tags(self.client, tags_to_add, [asset1, asset2])

        # Ensure the response is as expected
        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertSetEqual(tags, expected_tags)

    def test_account_tag_set(self):
        """
        Ensure that we can retrieve the set of all the existing tags for a
        given account.
        """
        account1 = create_account()
        account2 = create_account()
        account1_tags = sorted([u'foo', u'bar'])
        account2_tags = sorted([u'bar', u'baz'])

        # Account 1 has a single asset, with two tags.
        create_asset(account=account1, tags=account1_tags)

        # Account 2 has an asset with one tag and a user with the other.
        create_asset(account=account2, tags=[account2_tags[0]])
        create_viewer(account=account2, tags=[account2_tags[1]])

        self.assertEquals(list(account1.tags()), list(account1_tags))
        self.assertEquals(list(account2.tags()), list(account2_tags))

    def test_account_tag_counts(self):
        """
        Ensure that we can retrieve a set of tag counts for a account.
        """
        account = create_account()
        create_asset(account=account, tags=[u'foo', u'bar', u'baz'])
        create_asset(account=account, tags=[u'foo', u'bar'])
        create_asset(account=account, tags=[u'foo'])
        tag_counts = {
            u'foo': 3,
            u'bar': 2,
            u'baz': 1,
        }

        self.assertEquals(account.tag_counts(), tag_counts)

    def test_account_tag_popularity(self):
        """
        Ensure we can retrieve a list of tags ordered by popularity.
        """
        account = create_account()
        create_asset(account=account, tags=[u'foo', u'bar', u'c'])
        create_asset(account=account, tags=[u'foo', u'bar', u'a'])
        create_asset(account=account, tags=[u'foo', u'b'])
        tags_by_popularity = [u'foo', u'bar', u'a', u'b', u'c']

        self.assertEquals(account.tags_by_popularity(), tags_by_popularity)

    class RoleTestTagAutocompletion(RoleTest):
        """
        Ensure that we have a function tag autocompletion end-point.

        It should respect the JQuery url autocompletion style:
          http://docs.jquery.com/Plugins/Autocomplete/autocomplete

        Results should be ordered first by popularity, then by alphabetical.
        """
        can = ['editor', 'admin', 'viewer']

        def when(self, test):
            create_asset(account=test.account,
                         tags=[u'foo', u'bar', u'baz', u'bazbar', u'barbaz'])
            create_asset(account=test.account, tags=[u'baz'])

            url = reverse('tag_autocomplete_action')
            return test.client.get(url, {'term': u'b', 'limit': 3})

        def role_can(self, test, response):
            expected_suggestions = [u'baz', u'bar', u'barbaz']
            suggestions = json.loads(response.content)
            test.assertEquals(suggestions, expected_suggestions)

    def assertAutocompleteEqual(self, user, query, results):
        response = self.client.get(reverse('tag_autocomplete_action'),
                                   {'term': query})
        self.assertSetEqual(set(json.loads(response.content)),
                            set(results))

    def test_viewer_cannot_see_unrelated_user_tags(self):
        admin = create_admin()
        account = admin.get_profile().account
        viewer = create_viewer(account=account)
        other_viewer = create_viewer(account=account)
        viewer.get_profile().visible_tags.add('client_a', 'common')
        other_viewer.get_profile().visible_tags.add('client_b',
                                                    'common')

        create_asset(tags=['tag_a', 'client_a'], account=account)
        create_asset(tags=['tag_b', 'client_b'], account=account)
        create_asset(tags=['common'], account=account)

        self.client.login(viewer)
        self.assertAutocompleteEqual(viewer, 'tag_', [u'tag_a', u'tag_b'])
        self.assertAutocompleteEqual(viewer, 'client_', ['client_a'])
        self.assertAutocompleteEqual(viewer, 'com', ['common'])

        self.client.login(other_viewer)
        self.assertAutocompleteEqual(other_viewer, 'tag_', [u'tag_b', u'tag_a'])
        self.assertAutocompleteEqual(other_viewer, 'client_', ['client_b'])
        self.assertAutocompleteEqual(other_viewer, 'com', ['common'])

        self.client.login(admin)
        self.assertAutocompleteEqual(admin, 'tag_', ['tag_a', 'tag_b'])
        self.assertAutocompleteEqual(admin, 'client_', ['client_a', 'client_b'])
        self.assertAutocompleteEqual(admin, 'com', ['common'])

    def test_auto_complete_returns_results_for_multiple_case_variants_of_the_same_tag(self):
        user = create_viewer()
        account = user.get_profile().account
        create_asset(tags=['FOO', 'FOo', 'Foo'], account=account)

        self.client.login(user)
        self.assertAutocompleteEqual(user, 'f', [u'FOO', u'FOo', u'Foo'])
        self.assertAutocompleteEqual(user, 'FOO', [u'FOO', u'FOo', u'Foo'])
        self.assertAutocompleteEqual(user, 'foo', [u'FOO', u'FOo', u'Foo'])

    def test_ensure_tags(self):
        user = create_viewer()
        expected_tags = {'a', 'b', 'c', 'd'}
        user.get_profile().ensure_tags(expected_tags)
        self.assertSetEqual(
            set([t.name for t in user.get_profile().visible_tags.all()]),
            expected_tags)

    def test_tags_always_split_by_comma(self):
        expected_tags = set(['ab', 'c', 'de'])
        given_tags = 'ab,c,de'
        asset = create_asset()

        self.client.login(asset.added_by)

        data = make_asset_ids(asset)
        data['tags'] = given_tags
        response = self.client.post(reverse('asset_add_tags_action'), data=data)

        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertSetEqual(tags, expected_tags)

    def test_tags_can_have_spaces(self):
        expected_tags = set(['a b', 'c', 'd e'])
        given_tags = 'a b,c,d e'
        asset = create_asset()

        self.client.login(asset.added_by)

        data = make_asset_ids(asset)
        data['tags'] = given_tags
        response = self.client.post(reverse('asset_add_tags_action'), data=data)

        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertSetEqual(tags, expected_tags)

    def test_single_tag_can_have_spaces(self):
        expected_tags = set(['a b c'])
        given_tags = 'a b c'
        asset = create_asset()

        self.client.login(asset.added_by)

        data = make_asset_ids(asset)
        data['tags'] = given_tags
        response = self.client.post(reverse('asset_add_tags_action'), data=data)

        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertSetEqual(tags, expected_tags)


class RenderTagTests(AdminLoggedInTestCase):
    tags = ['slow']

    def setUp(self):
        super(RenderTagTests, self).setUp()
        self.tag = create_tag('test')

    def get_render_tag_response(self, tag, force_user_tag=''):
        response = self.client.get(reverse('render_tag_action'),
                                   {'tag_name': tag,
                                    'force_user_tag': force_user_tag},
                                   follow=True)
        return response.content

    def test_render_tag_renders_tag(self):
        self.assertIn('test', self.get_render_tag_response(tag=self.tag.name))

    def test_render_tag_shows_close_button_if_can_edit(self):
        self.assertTrue(self.user.get_profile().can_edit_assets())
        self.assertIn('close', self.get_render_tag_response(tag=self.tag.name))

    def test_render_tag_hides_close_button_if_cant_edit(self):
        self.user = create_viewer()
        self.client.login(self.user)
        self.assertFalse(self.user.get_profile().can_edit_assets())
        self.assertNotIn('close',
                         self.get_render_tag_response(tag=self.tag.name))

    def test_render_tag_shows_user_icon_if_applicable(self):
        user = create_viewer()
        user.get_profile().visible_tags.add(self.tag)
        self.assertIn('icon-user',
                      self.get_render_tag_response(tag=self.tag.name))
        other_tag = create_tag('test2')
        self.assertNotIn('icon-user',
                      self.get_render_tag_response(tag=other_tag.name))

    def test_render_tag_hides_user_icon_if_not_forced(self):
        self.assertFalse(self.tag.is_user_tag)
        self.assertNotIn('icon-user',
                         self.get_render_tag_response(tag=self.tag.name,
                                                      force_user_tag='0'))

    def test_render_tag_shows_user_icon_if_forced(self):
        self.assertIn('icon-user',
                      self.get_render_tag_response(tag=self.tag.name,
                                                   force_user_tag='1'))

    def test_render_tag_renders_tag_not_in_database(self):
        tag_name = 'test2'
        self.assertFalse(ProxyTag.objects.filter(name=tag_name).exists())
        self.assertIn('test2',
                      self.get_render_tag_response(tag=tag_name))

    def test_render_tag_hides_user_icon_if_viewer(self):
        tag_user = create_viewer()
        tag_user.get_profile().visible_tags.add(self.tag)
        self.assertIn('icon-user',
                      self.get_render_tag_response(tag=self.tag.name))

        self.user = create_viewer()
        self.client.login(self.user)
        self.assertNotIn('icon-user',
                      self.get_render_tag_response(tag=self.tag.name))


class BulkAddTagsTests(TestCase):
    tags = ['slow']

    class RoleTestBulkAddTags(RoleTest):
        can = ['admin', 'editor']

        def when(self, test):
            self.tags_to_add = {u'foo', u'bar', u'baz'}
            self.asset1 = create_asset(account=test.account)
            self.asset2 = create_asset(account=test.account)
            self.assets = [self.asset1, self.asset2]

            # Ensure there are no tags on the asset to start with
            for asset in self.assets:
                tags = set(asset.tags.all())
                test.assertEquals(tags, set())

            # Post some tags to the asset
            return post_add_tags(test.client, self.tags_to_add, self.assets)

        def role_can(self, test, response):
            # Ensure the tags have been created
            for asset in self.assets:
                tags = set([tag.name for tag in asset.tags.all()])
                test.assertEquals(tags, self.tags_to_add)


class BulkDeleteTagsTests(TestCase):
    tags = ['slow']

    class RoleTestBulkDeleteTags(RoleTest):
        """
        Ensure tags can be deleted.
        """
        can = ['editor', 'admin']

        def when(self, test):
            self.tags_to_delete = {u'foo'}
            self.existing_tags = {u'foo', u'bar', u'baz'}
            asset1 = create_asset(tags=self.existing_tags,
                                  account=test.account)
            asset2 = create_asset(tags=self.existing_tags,
                                  account=test.account)
            self.assets = [asset1, asset2]

            # Delete a tag from the asset
            return post_delete_tags(test.client, self.tags_to_delete, self.assets)

        def role_can(self, test, response):
            # Ensure the tags have been deleted
            for asset in self.assets:
                tags = set([tag.name for tag in asset.tags.all()])
                test.assertEquals(tags, self.existing_tags - self.tags_to_delete)


class CommonTagsTests(AdminLoggedInTestCase):
    tags = ['slow']

    def create_asset(self, **kwargs):
        return create_asset(account=self.account, **kwargs)

    def setUp(self):
        super(CommonTagsTests, self).setUp()
        self.expected_tags = ['tag_a', 'tag_b']
        asset_1 = self.create_asset(tags=self.expected_tags + ['tag_c'])
        asset_2 = self.create_asset(tags=self.expected_tags + ['tag_d'])
        asset_3 = self.create_asset(tags=self.expected_tags + ['tag_c', 'tag_d'])
        self.assets = [asset_1, asset_2, asset_3]

    def test_common_tags_works(self):
        response = self.client.post(reverse('common_tags_action'),
                                    data=make_asset_ids(*self.assets))
        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertEqual(tags, set(self.expected_tags))

    def test_common_tags_where_empty(self):
        self.assets[1].tags.clear()
        self.expected_tags = []
        response = self.client.post(reverse('common_tags_action'),
                                    data=make_asset_ids(*self.assets))
        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertEqual(tags, set(self.expected_tags))

    def test_common_tags_respects_restrictions(self):
        # If we restrict asset_1, we should get d and visible
        admin_expected = self.expected_tags
        viewer_expected = self.expected_tags + ['tag_d', 'visible']

        for asset in self.assets[1:]:
            asset.tags.add('visible')

        viewer = create_viewer(tags=['visible'], account=self.account)

        # Still logged in as admin
        response = self.client.post(reverse('common_tags_action'),
                                    data=make_asset_ids(*self.assets))
        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertEqual(tags, set(admin_expected))

        self.client.login(viewer)
        response = self.client.post(reverse('common_tags_action'),
                                    data=make_asset_ids(*self.assets))

        tags = set(extract_tags_from_html(json.loads(response.content)))
        self.assertEqual(tags, set(viewer_expected))


class TagListActionTest(LoggedInTestCase):
    def test_tag_list_contains_all_tags_visible_to_the_logged_in_user(self):
        account1 = self.account
        account2 = create_account()
        account1_tags = [u'foo', u'bar']
        account2_tags = [u'bar', u'baz']

        # Account 1 has two assets with both tags
        create_asset(account=account1, tags=account1_tags)
        create_asset(account=account1, tags=account1_tags)

        # Account 2 has one asset with one tag and a user with the other.
        create_asset(account=account2, tags=[account2_tags[0]])
        create_viewer(account=account2, tags=[account2_tags[1]])

        response = self.client.get(reverse('tag-list'))
        tags = json.loads(response.content)

        self.assertEqual([u'bar', u'foo'], tags)

    def test_tag_list_returns_tags_in_alphabetical_order(self):
        create_asset(account=self.account, tags=[u'bbb'])
        create_asset(account=self.account, tags=[u'zzz'])
        create_asset(account=self.account, tags=[u'aaa'])

        response = self.client.get(reverse('tag-list'))
        tags = json.loads(response.content)

        self.assertEqual([u'aaa', u'bbb', u'zzz'], tags)
