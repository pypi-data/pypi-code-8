# -*- coding: utf-8 -*-
# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
"""
Service tests for Asset Cloud's Haystack-based search.
"""
from .utils import LoggedInTestCase, TestCase, create_user, create_account, create_asset, create_image_asset
from assetcloud import index, models, model_shortcuts
from assetcloud.models import Upload
from assetcloud.search import assets_from_results, pks_from_results
from assetcloud.views import SearchView
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.webdesign import lorem_ipsum
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.utils import unittest
from haystack.query import SearchQuerySet
from urlparse import urlparse
import datetime


skip_if_whoosh = unittest.skipIf(
    settings.HAYSTACK_CONNECTIONS['default']['ENGINE'] == 'haystack.backends.whoosh_backend.WhooshEngine',
    "This sort of search is know not to work with the Whoosh backend, "
    "but it should work with Solr.")


class SearchTests(TestCase):
    needs_index = True

    def test_simple_search(self):
        """
        Simple search test intended to just check that the basics are working.
        """

        # Create an asset
        asset = create_asset(filename='FrivolousCat.jpg', title='Silly')

        # Any search results?
        results = SearchQuerySet().all()
        self.assertIn(asset, assets_from_results(results))

        # Can search by title?
        results = SearchQuerySet().filter(content=asset.title)
        self.assertIn(asset, assets_from_results(results))

        # Can search by filename?
        results = SearchQuerySet().filter(content=asset.filename)
        self.assertIn(asset, assets_from_results(results))

        # Search for something that isn't in the asset data - we shouldn't get
        # any results.
        results = SearchQuerySet().filter(content='Stupid')
        self.assertEqual(assets_from_results(results), [])

        # Shouldn't be in the index any more after it has been deleted
        id = asset.id
        asset.delete()

        results = SearchQuerySet().filter(content=asset.title)
        # This was passing even though the record was still in the index because
        # haystack.models.SearchResult._get_object loads the object from the DB
        # (and of course the object isn' t in the DB)...
        self.assertNotIn(asset, assets_from_results(results))
        # ... so we assert based on the PKs too
        self.assertNotIn(id, pks_from_results(results))
        self.assertNotIn(unicode(id), pks_from_results(results))


class SlowSearchTests(TestCase):
    needs_index = True
    tags = ['slow']

    def test_search_for_one_word_in_many(self):
        asset = create_asset(filename='FrivolousCat.jpg',
                             title='I am a title with many words')
        results = SearchQuerySet().filter(content='many')
        self.assertEqual(assets_from_results(results), [asset])

    def test_search_for_non_consecutive_words(self):
        asset = create_asset(filename='FrivolousCat.jpg',
                             title='I am a title with many words')

        # shouldn't work, according to my reading of
        # http://docs.haystacksearch.org/dev/searchqueryset_api.html#filter
        # but does with Whoosh (but not Solr).
        #results = SearchQuerySet().filter(content='title many')
        results = SearchQuerySet().auto_query('title many')
        self.assertEqual(assets_from_results(results), [asset])

    def test_stemming(self):
        asset = create_asset(filename='FrivolousCat.jpg',
                             title='I am a title with many buggies')
        results = SearchQuerySet().filter(content='buggy')
        self.assertEqual(assets_from_results(results), [asset])

    def test_search_is_case_insensitive(self):
        asset = create_asset(filename='FrivolousCat.jpg',
                             title='I am a title with many Buggies')

        results = SearchQuerySet().filter(content='buggies')
        self.assertEqual(assets_from_results(results), [asset])

        results = SearchQuerySet().filter(content='MANY')
        self.assertEqual(assets_from_results(results), [asset])

    # This test would pass if we removed the solr.WordDelimiterFilterFactory
    # filters from <fieldType name="text"> in the solr schema.xml, however
    # that would break test_search_by_filename_without_extension and
    # test_search_by_word_in_camel_case_filename.
#    def test_search_of_camel_case_dotted_is_case_insensitive(self):
#        create_asset(filename='FrivolousCat.jpg',
#                     title='FooBar.baz')
#
#        results = SearchQuerySet().filter(content='foobar.baz')
#        self.assertEqual(1, len(results))

    def test_search_by_whole_filename(self):
        asset = create_asset(filename='FrivolousCat.jpg', title='Silly')
        results = SearchQuerySet().filter(content='FrivolousCat.jpg')
        self.assertEqual(assets_from_results(results), [asset])

    def test_search_by_whole_filename_is_case_insensitive(self):
        # N.B. this would fail when run with solr if filename was
        # 'FrivolousCat.jpg'. See
        # test_search_of_camel_case_dotted_is_case_insensitive for an
        # explanation.
        asset = create_asset(filename='Frivolouscat.jpg', title='Silly')
        results = SearchQuerySet().filter(content='frivolouscat.jpg')
        self.assertEqual(assets_from_results(results), [asset])

    def test_search_by_whole_filename_containing_space(self):
        asset = create_asset(filename='Frivolous Cat.jpg', title='Silly')
        results = SearchQuerySet().filter(content='Frivolous Cat.jpg')
        self.assertEqual(assets_from_results(results), [asset])

    def test_search_by_tags(self):
        asset = create_asset()
        asset.tags.add('foo', 'bar')
        results = SearchQuerySet().filter(content='foo')
        self.assertEqual(assets_from_results(results), [asset])

    def test_search_by_tags_ignores_case(self):
        asset = create_asset()
        asset.tags.add('foo', 'BAR')
        results = SearchQuerySet().filter(content='FOO bar')
        self.assertEqual(assets_from_results(results), [asset])

    @skip_if_whoosh
    def test_search_by_filename_without_extension(self):
        asset = create_asset(filename='FrivolousCat.jpg', title='Silly')
        results = SearchQuerySet().filter(content__startswith='FrivolousCat')
        self.assertEqual(assets_from_results(results), [asset])

    def test_search_by_word_in_space_sep_filename(self):
        asset = create_asset(filename='Frivolous Cat.jpg', title='Silly')
        results = SearchQuerySet().filter(content='Frivolous')
        self.assertEqual(assets_from_results(results), [asset])

    @skip_if_whoosh
    def test_search_by_word_in_camel_case_filename(self):
        asset = create_asset(filename='FrivolousCat.jpg', title='Silly')
        results = SearchQuerySet().filter(content='Frivolous')
        self.assertEqual(assets_from_results(results), [asset])

    def test_search_for_bang_returns_no_results(self):
        create_asset(filename='FrivolousCat.jpg', title='Silly')
        results = SearchQuerySet().auto_query('!')
        self.assertEqual(assets_from_results(results), [])

    # This test failed before preserveOriginal="1" was added to the
    # WordDelimiterFilterFactory in
    # schema.xml. test_search_for_bang_returns_no_results, above, passed even
    # before the preserveOriginal flag was added.
    @skip_if_whoosh
    def test_search_for_account_and_bang_returns_no_results(self):
        account = create_account()
        user = create_user(account=account)
        create_asset(filename='FrivolousCat.jpg', title='Silly',
                     account=account)

        results = user.get_profile().filter_search(
            SearchQuerySet().auto_query('!'))

        self.assertEqual(assets_from_results(results), [])


def create_data_for_access_control_tests():
    accounts = []
    account_users = []
    # create test data - 2 accounts, an asset owned by each
    for i in range(2):
        account = create_account()
        accounts.append(account)
        user = create_user(account)
        account_users.append(user)

    create_asset(account=accounts[0],
                 title='Asset belonging to account 1. abc.')
    create_asset(account=accounts[1],
                 title='Asset belonging to account 2. def.')

    return account_users


class SearchAccountAccessControlTests(TestCase):
    """
    Make sure that the UserProfile.filter_search method filters other
    accounts' assets out of the search results.
    """
    needs_index = True

    def setUp(self):
        super(SearchAccountAccessControlTests, self).setUp()
        self.client_users = create_data_for_access_control_tests()

    def test_asset_from_same_account_included(self):
        user = self.client_users[0]
        results = SearchQuerySet().filter(content='abc')
        results = user.get_profile().filter_search(results)
        self.assertEqual(1, len(results))

    def test_asset_from_different_account_not_included(self):
        user = self.client_users[1]
        results = SearchQuerySet().filter(content='abc')
        results = user.get_profile().filter_search(results)
        self.assertEqual(assets_from_results(results), [])


class SearchPageAccountAccessControlTests(TestCase):
    """
    Make sure that the search results page filters other accounts' assets out
    of the search results.
    """
    needs_index = True

    def setUp(self):
        super(SearchPageAccountAccessControlTests, self).setUp()
        self.client_users = create_data_for_access_control_tests()

    def test_asset_from_same_account_included(self):
        self.client.login(self.client_users[0])

        results = search_page_query(self.client, {'q': 'abc'})

        # Check that 1 search result was returned
        self.assertEqual(1, len(results))

    def test_asset_from_different_account_not_included(self):
        self.client.login(self.client_users[1])

        results = search_page_query(self.client, {'q': 'abc'})

        # Check that no search results were returned
        self.assertEqual(results, [])


class SearchPageAssertions(object):
    def assert_filter_results(self, search_text, filter_type, results_map):
        """
        Given some search text, and a search filter, check that expected
        results are returned.
        `results_map` is a dict of filter query -> results.
        """
        for query, expected_results in results_map.items():
            search = {'q': search_text, filter_type: query}
            results = search_page_query(self.client, search)
            self.assertEquals(results, expected_results)

    def assert_filter_results_between(self, search_text, results_map):
        """
        Like `assert_filter_results` except it does a search with both a
        `from_date` and an `until_date` instead of just one or the other.
        """
        for (from_date, until_date), results_map in results_map.items():
            search = {
                'q': search_text,
                'from_date': from_date,
                'until_date': until_date
            }
            results = search_page_query(self.client, search)
            self.assertEquals(results, results_map)


class SearchPageTests(TestCase, SearchPageAssertions):
    needs_index = True

    def test_search_page_returns_results(self):
        """
        Ensure that a simple free-text search returns correct results.
        """
        asset = create_asset(title='I am a title with many words')
        self.client.login(asset.added_by)

        # Get the search page
        response = self.client.get(reverse('search'), {'q': 'many'})

        # Ensure all the page is rendered with the correct template,
        # and the correct list of assets.
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assetcloud/pages/search.html')
        self.assertEquals(search_results(response), [asset])

    def test_search_page_results_include_thumbnail(self):
        """
        Ensure that the thumbnail is correctly included
        """
        asset = create_image_asset(title='Crazy mad title')
        self.client.login(asset.added_by)

        # Get the search page
        response = self.client.get(reverse('search'), {'q': 'crazy'})

        # Ensure all the page is rendered with the correct template,
        # and the correct list of assets.
        self.assertTemplateUsed(response, 'assetcloud/snippets/asset_display_thumbnail.html')
        self.assertContains(response, 'alt="%s"' % asset.title)

    @skip_if_whoosh
    def test_filter_between_dates(self):
        """
        Test that we can filter search results to only include assets
        added between a pair of dates.
        """
        added = datetime.date(2001, 1, 26)
        title = random_title()

        asset = create_asset(title=title, added=added)
        self.client.login(asset.added_by)

        expected_results = {
            (datetime.date(2001, 1, 25), datetime.date(2001, 1, 25)): [],
            (datetime.date(2001, 1, 25), datetime.date(2001, 1, 26)): [asset],
            (datetime.date(2001, 1, 25), datetime.date(2001, 1, 27)): [asset],
            (datetime.date(2001, 1, 26), datetime.date(2001, 1, 26)): [asset],
            (datetime.date(2001, 1, 26), datetime.date(2001, 1, 27)): [asset],
            (datetime.date(2001, 1, 27), datetime.date(2001, 1, 27)): [],
        }

        self.assert_filter_results_between(title, expected_results)


class SlowSearchPageTests(TestCase, SearchPageAssertions):
    needs_index = True
    tags = ['slow']

    def test_search_view_has_section_defined(self):
        try:
            SearchView().section
        except AttributeError:
            self.fail('Section should be defined on search view')

    def test_search_page_exists(self):
        """
        Ensure we can get the search page.
        """
        # Get the search page
        self.client.login()
        response = self.client.get(reverse('search'))

        # Ensure all the page is rendered, with no assets.
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assetcloud/pages/search.html')
        self.assertEquals(search_results(response), [])

    def test_no_query_returns_all_assets(self):
        """
        Check that a search with no query returns all the assets (as opposed to
        no assets and a validation error, like it used to).
        """
        user = self.client.login()
        account = user.get_profile().account

        assets = [create_asset(filename='FrivolousCat.jpg',
                               title='Hello Dog!',
                               account=account),
                  create_asset(filename='FrivolousDog.jpg',
                               title='Hello Cat!',
                               account=account)]
        response = self.client.get(reverse('search'))

        # Ensure all the page is rendered, with all the assets.
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assetcloud/pages/search.html')
        # we use set() because we don't care about the order
        self.assertEqual(set(search_results(response)), set(assets))

    def test_search_by_whole_filename(self):
        """
        Search by filename, including file extension.
        """
        asset = create_image_asset(filename='myimage.png')
        self.client.login(asset.added_by)

        # Get the search page
        response = self.client.get(reverse('search'), {'q': asset.filename})

        # Ensure all the page is rendered with the correct template,
        # and the correct list of assets.
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assetcloud/pages/search.html')
        self.assertEquals(search_results(response), [asset])

    @skip_if_whoosh
    def test_search_by_stopword_doesnt_return_all_assets(self):
        """
        Whoosh appears to have a bug wherby a search for a stopword, such
        as 'the', 'than' or 'an', returns all the assets.

        This test verifies that this behaviour does not occur with Solr.
        """
        stopwords = ['the', 'that']
        asset = create_asset(title=random_title())

        self.client.login(asset.added_by)
        self.assert_no_results(stopwords)

    @skip_if_whoosh
    def test_search_for_single_letter_doesnt_return_all_assets(self):
        """
        Whoosh appears to have a bug wherby a search for a single letter
        returns all the assets.

        This test verifies that this behaviour does not occur with Solr.
        """
        single_letters = ['x', 'y', 'z']
        asset = create_asset(
            filename='FrivolousCat.jpg',
            title='Temporibus facilis doloribus eveniet?')

        self.client.login(asset.added_by)
        self.assert_no_results(single_letters)

    def assert_no_results(self, queries):
        """
        Assert that no search results are returned for any of the passed
        query strings.
        """
        for word in queries:
            # Get the search page
            response = self.client.get(reverse('search'), {'q': word})

            # Ensure all the page is rendered with the correct template,
            # and the correct list of assets.
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'assetcloud/pages/search.html')
            self.assertEquals(search_results(response), [])

    def test_filter_after_date(self):
        """
        Test that we can filter search results to only include
        assets added on, or after, a given date.
        """
        added = datetime.date(2001, 1, 26)
        title = random_title()

        asset = create_asset(title=title, added=added)

        filter_type = 'from_date'
        expected_results = {
            datetime.date(2001, 1, 25): [asset],
            datetime.date(2001, 1, 26): [asset],
            datetime.date(2001, 1, 27): []
        }

        self.client.login(asset.added_by)
        self.assert_filter_results(asset.title, filter_type, expected_results)

    @skip_if_whoosh
    def test_filter_before_date(self):
        """
        Test that we can filter search results to only include
        assets added on, or before, a given date.
        """
        # Use a non-midnight time because that will cause a test failure if
        # the search naively does asset.date <= search.date
        added = datetime.datetime(2001, 1, 26, 12, 42, 55)
        title = random_title()

        asset = create_asset(title=title, added=added)

        filter_type = 'until_date'
        expected_results = {
            datetime.date(2001, 1, 25): [],
            datetime.date(2001, 1, 26): [asset],
            datetime.date(2001, 1, 27): [asset]
        }

        self.client.login(asset.added_by)
        self.assert_filter_results(asset.title, filter_type, expected_results)

    @skip_if_whoosh
    def test_filter_between_back_to_front_dates(self):
        """
        Test that date search filtering still works if the user enters the
        dates the wrong way round.
        """
        added = datetime.date(2001, 1, 26)
        title = random_title()

        asset = create_asset(title=title, added=added)
        self.client.login(asset.added_by)

        expected_results = {
            (datetime.date(2001, 1, 25), datetime.date(2001, 1, 25)): [],
            (datetime.date(2001, 1, 26), datetime.date(2001, 1, 25)): [asset],
            (datetime.date(2001, 1, 27), datetime.date(2001, 1, 25)): [asset],
            (datetime.date(2001, 1, 26), datetime.date(2001, 1, 26)): [asset],
            (datetime.date(2001, 1, 27), datetime.date(2001, 1, 26)): [asset],
            (datetime.date(2001, 1, 27), datetime.date(2001, 1, 27)): [],
        }

        self.assert_filter_results_between(title, expected_results)

    @skip_if_whoosh
    def test_back_to_front_dates_swapped_on_form(self):
        """
        Test that back to front dates are swapped to become the right way
        round in the form that is shown on the search results page
        """
        added = datetime.date(2001, 1, 26)
        title = random_title()

        asset = create_asset(title=title, added=added)
        self.client.login(asset.added_by)

        search = {
            'q': title,
            'from_date': datetime.date(2001, 1, 27),
            'until_date': datetime.date(2001, 1, 25)
        }
        response = self.client.get(reverse('search'), search)
        # The date format used below for the expected values was found
        # experimentally. I think it's probably just format that you get when
        # you call str() on a datetime.date. The important thing about this
        # test isn't the date format, it's that the from and until dates on
        # the bound fields are the opposite way round to the way round that
        # they were in the query.
        self.assertEqual(
            '2001-01-25',
            response.context['form']['from_date'].value())
        self.assertEqual(
            '2001-01-27',
            response.context['form']['until_date'].value())


class SearchPageOrderingTests(LoggedInTestCase):
    needs_index = True
    tags = ['slow']

    def test_recently_added_assets_are_displayed_first(self):
        account = self.user.get_profile().account

        title = 'simple'
        asset_1 = create_asset(title=title, account=account)
        asset_2 = create_asset(title=title, account=account)
        asset_3 = create_asset(title=title, account=account)

        expected = [asset_3, asset_2, asset_1]

        results = search_page_query(self.client, {'q': title})

        self.assertListEqual(expected, results)


class SearchPageTagTests(TestCase):
    needs_index = True

    def test_tag_search_with_more_tags_and_tags(self):
        """
        The more_tags and tags should be merged into a single list before
        the search is performed.
        """
        asset = create_asset(tags=['hjkl', 'qwerty', 'asdf', 'ggg'])

        search = {'more_tags': 'hjkl, asdf', 'tags': 'qwerty, ggg'}
        expected_results = [asset]

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)

        self.assertEquals(expected_results, results)

    def test_search_by_query_and_tag_includes_asset_with_tag(self):
        """
        Search with free-text, plus a tag filter, and check that a matching
        asset is returned.
        """
        title = random_title()
        tag = 'mytag'
        asset = create_asset(title=title, tags=[tag])

        search = {'q': title, 'tags': tag}

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)
        self.assertEquals(results, [asset])

    def test_search_by_query_where_query_is_part_of_tag_containing_space_returns_asset(self):
        title = random_title()
        asset = create_asset(title=title, tags=['the world', 'qwerty'])

        search = {'q': 'the'}
        expected_results = [asset]

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)
        self.assertEquals(expected_results, results)

    def test_tag_search_with_nasty_chars_issue_175(self):
        """
        Check that search page can handle searches for tags with non-ASCII
        characters in them (Github #175).
        """

        asset = create_asset(tags=[u'something else'])

        search = {'more_tags': u'!!!!!"£$%^&*('}
        expected_results = []

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)

        self.assertEquals(expected_results, results)


class SlowSearchPageTagTests(TestCase):
    """
    Tests for searching by tag on the search page.
    """
    needs_index = True
    tags = ['slow']

    def test_search_by_query_and_tag_excludes_nonexistent_tag(self):
        """
        Ensure that when we search by free-text, and a tag filter,
        that assets with (only) a different tag are not found.
        """
        title = random_title()
        tag = 'mytag'
        asset = create_asset(title=title, tags=[tag])

        search = {'q': asset.title, 'tags': 'myothertag'}

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)
        self.assertEquals(results, [])

    def test_search_by_query_and_tag_excludes_asset_without_tag(self):
        """
        Ensure that when we search by free-text, and a tag filter,
        that assets without that tag will not be returned.
        """
        asset1 = create_asset(title='foobar', tags=['mytag'])
        asset2 = create_asset(account=asset1.account, title=asset1.title,
                              tags=['myothertag'])

        search = {'q': asset2.title, 'tags': 'myothertag'}
        expected_results = [asset2]

        self.client.login(asset1.added_by)
        results = search_page_query(self.client, search)
        self.assertEquals(expected_results, results)

    def test_search_by_tag_only(self):
        """
        Ensure that we can search by tag, without any free-text.
        """
        title = 'tagged asset'
        tag = 'mytag'
        asset = create_asset(title=title, tags=[tag])

        search = {'tags': tag}
        expected_results = [asset]

        self.client.login(asset.added_by)
        response = self.client.get(reverse('search'), search)
        results = search_results(response)

        self.assertTemplateUsed(response, 'assetcloud/pages/search.html')
        # Check that the asset is actually shown on the page (at one point
        # the page was just showing "Enter your search above" if a free-text
        # string was not part of the search parameters),
        self.assertContains(response, asset.title)
        self.assertEquals(expected_results, results)

    def test_search_by_multiple_tags(self):
        title = random_title()
        asset = create_asset(title=title, tags=['asdf', 'hjkl', 'qwerty'])

        search = {'tags': 'qwerty, asdf'}
        expected_results = [asset]

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)
        self.assertEquals(expected_results, results)

    def test_search_by_multiple_tags_including_nonexistent_tag(self):
        title = random_title()
        asset = create_asset(title=title, tags=['asdf', 'hjkl', 'qwerty'])

        search = {'tags': 'qwerty asdf notonanyasset'}
        expected_results = []

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)
        self.assertEquals(expected_results, results)

    def test_search_ignores_tag_case(self):
        title = random_title()
        asset = create_asset(title=title, tags=['ASDF', 'AsDf'])

        search = {'q': 'asdf'}
        expected_results = [asset]

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)
        self.assertEquals(expected_results, results)

    def test_tag_search_by_tag_containing_space_returns_asset(self):
        title = random_title()
        asset = create_asset(title=title, tags=['the world', 'qwerty'])

        search = {'tags': 'the world'}
        expected_results = [asset]

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)
        self.assertEquals(expected_results, results)

    def test_tag_search_with_single_more_tag(self):
        """
        More tags are just tags. We need to distinguish between tags that
        are already included in a search (tags=''), and new tags that are
        added by the user to further filter their search results (more_tags='').
        """
        asset = create_asset(tags=['qwerty'])

        search = {'more_tags': 'qwerty'}
        expected_results = [asset]

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)

        self.assertEquals(expected_results, results)

    def test_tag_search_with_multiple_more_tags(self):
        asset = create_asset(tags=['qwerty, asdf'])

        search = {'more_tags': 'qwerty, asdf'}
        expected_results = []

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)

        self.assertEquals(expected_results, results)

    def test_tag_search_with_empty_more_tags(self):
        asset = create_asset(tags=['asdf', 'hjkl', 'qwerty'])

        search = {'more_tags': ''}
        expected_results = [asset]

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)

        self.assertEquals(expected_results, results)

    def test_tag_search_with_nonexistent_more_tag(self):
        asset = create_asset(tags=['asdf', 'hjkl', 'qwerty'])

        search = {'more_tags': 'asdf, notonanyasset'}
        expected_results = []

        self.client.login(asset.added_by)
        results = search_page_query(self.client, search)

        self.assertEquals(expected_results, results)

    def test_tag_search_hidden_tags_field_is_comma_separated_tag_string(self):
        search = {'more_tags': 'hjkl, asd f, . .,,', 'tags': 'qwerty, ggg'}

        self.client.login(create_user())
        response = self.client.get(reverse('search'), search)

        tags_field_value = response.context['form']['tags'].value()
        self.assertEquals('ggg, qwerty, . ., asd f, hjkl', tags_field_value)

    def test_tag_search_more_tags_field_is_blank(self):
        search = {'more_tags': 'hjkl, asdf, . .,,', 'tags': 'qwerty, ggg'}

        self.client.login(create_user())
        response = self.client.get(reverse('search'), search)

        more_tags_field_value = response.context['form']['more_tags'].value()
        self.assertEqual('', more_tags_field_value)


class SearchPageLastUploadTests(LoggedInTestCase):
    needs_index = True

    def test_search_for_last_upload(self):
        old_upload = Upload(added_by=self.user)
        old_upload.save()
        for i in range(2):
            self.create_asset(upload=old_upload)

        last_upload = Upload(added_by=self.user)
        last_upload.save()
        last_upload_assets = [self.create_asset(upload=last_upload)
                              for i in range(3)]

        search = {'last_upload': 'True'}
        expected_results = list(last_upload_assets)
        expected_results.reverse()

        results = search_page_query(self.client, search)

        self.assertEquals(expected_results, results)


class SlowSearchPageLastUploadTests(LoggedInTestCase):
    needs_index = True
    tags = ['slow']

    def test_search_for_last_upload_after_adding_tag(self):
        """
        Adding a 'last upload' filter after adding a tag filter used to result
        in a parameter more_tags=None in the URL which would cause a search for
        a tag called 'None' to be added. This was happening because the object
        None was being converted to the string 'None' in
        SearchForm.query_string_with_last_upload().

        This test checks that that defect is fixed.
        """

        asset = self.create_asset(title='find me', tags=['cool'])
        assets = [asset]

        response = self.client.get(reverse('search'), data={
            'q': 'find',
            'more_tags': 'cool',
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(assets, search_results(response))

        response_soup = BeautifulSoup(response.content)
        # First check that the last upload link doesn't have a 'more_tags=None'
        # parameter, so we can fail early if we find one.
        last_upload_element = response_soup.find(id='last_upload_link')
        last_upload_href = last_upload_element['href']
        last_upload_query = urlparse(last_upload_href).query
        last_upload_query_dict = QueryDict(last_upload_query)
        more_tags_param = last_upload_query_dict.get('more_tags', None)
        self.assertNotEqual('None', more_tags_param)

        # Now follow the last upload link and check that some assets are found
        # (which there won't be if an erroneous search for a tag called 'None'
        # is happening').
        response = self.client.get(last_upload_href)
        self.assertEqual(200, response.status_code)
        self.assertEqual(assets, search_results(response))


class SlowSearchPagePaginationTest(LoggedInTestCase):
    needs_index = True
    tags = ['slow']

    def setUp(self):
        super(SlowSearchPagePaginationTest, self).setUp()
        # Change settings here to avoid https://github.com/jezdez/django_compressor/issues/333
        self.old_assets_per_page = settings.ASSETS_PER_PAGE
        settings.ASSETS_PER_PAGE = 2

    def tearDown(self):
        super(SlowSearchPagePaginationTest, self).tearDown()
        settings.ASSETS_PER_PAGE = self.old_assets_per_page

    def test_pagination_includes_given_parameters(self):
        for i in range(3):
            create_asset(account=self.account)
        response = self.client.get(reverse('search') + "?foo=a", follow=True)
        self.assertContains(response, '?foo=a&page=2')

    def test_pagination_works_for_no_given_parameters(self):
        for i in range(3):
            create_asset(account=self.account)
        response = self.client.get(reverse('search'), follow=True)
        self.assertContains(response, '?page=2')

    def test_pagination_includes_given_parameters_previous(self):
        for i in range(3):
            create_asset(account=self.account)
        response = self.client.get(reverse('search') + "?foo=a&page=2",
                                   follow=True)
        self.assertContains(response, '?foo=a&page=1')

    def test_pagination_works_for_no_given_parameters_previous(self):
        for i in range(3):
            create_asset(account=self.account)
        response = self.client.get(reverse('search') + "?page=2", follow=True)
        self.assertContains(response, '?page=1')


class IncrementalIndexTests(TestCase):
    """
    Tests for the mechanics of incremental indexing.
    """
    needs_index = True
    tags = ['slow']

    def test_update_index_is_incremental(self):
        """
        test_simple_search only calls update_index() once.

        This test calls it twice to make sure the second call works.
        """

        # hack to make assetcloud.index think that a request is in progress and
        # stop it from updating the index straight away
        index.status.status = index.STATUS_IN_PROGRESS

        self.assertEqual([], list(index.get_assets_to_index()))

        asset = create_asset(filename='FrivolousCat.jpg', title='Silly')

        self.assertEqual([asset], list(index.get_assets_to_index()))

        index.update_index()
        self.assertEqual([], list(index.get_assets_to_index()))

        asset2 = create_asset(title='Silly2')
        asset3 = create_asset(title='Silly3')

        self.assertEqual([asset2, asset3], list(index.get_assets_to_index()))

        index.update_index()
        self.assertEqual([], list(index.get_assets_to_index()))

        # put index.status.status back to 'no request in progress'
        index.status.status = None


def search_page_query(client, query):
    """
    Run a search query using the search view and return the search results
    that would be included on the search results page.

    `query`: the query parameters to pass to the search view
    """
    response = client.get(reverse('search'), query)
    return search_results(response)


def search_results(response):
    """
    Return the list of assets that we returned by a search result.
    """
    return assets_from_results(response.context['page'].object_list)


def random_title():
    """
    Return a random lorum ipsum title for an asset.
    """
    max_length = model_shortcuts.max_field_length(models.Asset, 'title')
    return lorem_ipsum.sentence()[:max_length]
