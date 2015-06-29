__author__ = 'jwsm'

'''
Fanfic class. The final version will use JIT attribute initialization.
Do not access member attributes directly.
'''

import datetime
import re
import requests

from bs4 import BeautifulSoup, SoupStrainer
from FanfictionAPI import urls


class Fanfic(object):
    """
    Represents a fanfic, as found at http://www.fanfiction.net/s/story_id/chapter_num/title
    This class uses JIT initialization. DO NOT access member variables directly.
    """

    def __init__(self, url, html=None):
        """
        Constructor

        Args:
            url (str): The url of the fic to construct.
        """

        self._url = urls.normalize_url(url)
        if urls.classify_url(self._url) != urls.Fanfic:
            raise ValueError("Invalid url for Fanfic object")

        if html:
            self._html = BeautifulSoup(html)
        else:
            self._html = self._get_html()

        # Don't touch! Will be initialized as needed. Just need to declare them
        # in __init__ method
        self._title = None
        self._author = None
        self._author_url = None
        self._summary = None
        self._rating = None
        self._details = None    # <span> containing Rating, Reviews, Genre, etc.
        self._language = None
        self._genres = None
        self._characters = None
        self._pairings = None
        self._chapters = None
        self._word_count = None
        self._reviews = None
        self._favorites = None
        self._follows = None
        self._updated = None
        self._published = None
        self._id = None

    def _get_html(self):
        """
        Helper function. Use BS4 library to parse a page
        Should only be called once, in __init__.
        No ill effects if called in other places, but no real reason to do so
        """

        return BeautifulSoup(requests.get(self._url).text)

    def get_title(self):
        """
        Returns:
            Title of the fic
        """
        if not self._title:
            self._title = self._html.find_all('b', 'xcontrast_txt')[0].string

        return self._title

    def get_url(self):
        """
        There is absolutely no reason to ever call this.
        But someone will find a reason anyway, so it's here.

        Returns:
            str: The url of the fic. That you passed to the constructor
        """
        return self._url

    def get_author(self):
        """
        Returns:
            The author of the fic.
        """

        if not self._author:
            # Look for a 'link' that looks like /u/[user_id]/[username]. There should only be one.
            author_candidates = self._html.find_all('a', {'href': re.compile('^' + urls.user_partial_regex)})

            self._author = author_candidates[0].string

        return self._author

    def get_author_url(self):
        """
        Another accessor.

        Returns:
            str: a url to the author's profile
        """

        if not self._author_url:
            # Find a link that looks like /u/[user_id]/[user_name]. There should only be one
            author_candidates = self._html.find_all('a', {
                'href': re.compile('^' + urls.user_partial_regex)
            })

            # Prepend http://www.fanfiction.net for a fully valid link
            self._author_url = urls.fanfiction_base_url + author_candidates[0]['href']

        return self._author_url

    def get_summary(self):
        """
        Returns:
            str: The fanfic's summary
        """

        if not self._summary:
            # This is the styling of the div containing the summary
            # If there's a better way to do this, I am unaware of it
            self._summary = self._html.find_all('div', {
                'style': 'margin-top:2px',
                'class': 'xcontrast_txt'
            })[0].string.strip()

        return self._summary

    def _get_details(self):
        """
        Helper function to make reading favorites, follows, etc. faster
        There is a <span> element that basically contains a hyphenated string
        will all the fic's details. The finds that.

        Returns:
            [str]: a list of strings containing information about the fic
        """

        if not self._details:
            self._details = self._html.find_all('span', {
                'class': 'xgray xcontrast_txt'
            })[0].text.split(' - ')

        return self._details

    def get_rating(self):
        """
        Returns:
            str: The rating of the fanfic
            Possible values: K, K+, T, M
        """

        if not self._rating:
            # rating_string will look like "Fiction  T"
            rating_string = self._get_details()[0]
            self._rating = rating_string[-1]

            if self._rating == '+':
                self._rating = rating_string[-2:]

        return self._rating

    # Assumptions: Every fic has a language
    #              Language is the first item after the Rating
    def get_language(self):
        """
        Return:
            str: The language the fanfic is written in
        """
        if not self._language:
            details = self._get_details()
            self._language = details[1].strip()
        return self._language

    def get_genres(self):
        """
        Return:
            [str]: The genres of the fanfiction
            Possible values: Adventure, Angst, Crime, Drama, Family,
                             Friendship, General, Humor, Horror, Hurt/Comfort,
                             Mystery, Parody, Poetry, Romance, Sci-Fi,
                             Spiritual, Supernatural, Suspense, Tragedy, Western

        """
        if not self._genres:
            details = self._get_details()
            self._genres = details[2].strip().split('/')

            if 'Hurt' in self._genres:
                hurt_index = self._genres.index('Hurt')
                self._genres[hurt_index] = 'Hurt/Comfort'
                self._genres[hurt_index + 1] = None
                self._genres = list(filter(None, self._genres))

        return self._genres

    def get_characters(self):
        """
        Returns:
            [str]: The characters in the fanfic
        """
        if self._characters is None:

            # Check if characters are listed at all
            # I think it's safe to assume there's no character anywhere named Chapters:
            if 'Chapters: ' in self._get_details()[3].strip():
                self._characters = []

            else:
                # " [Foo, Bar] [Baz, Qux]" -> [" [Foo", "Bar", "Baz", "Qux]"]
                # " [Foo, Bar] Baz, Qux" -> [" [Foo", "Bar", "Baz", "Qux"]
                self._characters = self._get_details()[3].\
                    replace('] [', ', ').replace('] ', ', ').split(', ')

                # [" [Foo", "Bar", "Baz", "Qux]"] - > ["Foo", "Bar", "Baz", "Qux"]
                self._characters = [character.strip().replace('[', '').replace(']', '')
                                    for character in self._characters]
        return self._characters

    def get_pairings(self):
        """
        Returns:
            [(str, str)]: Each tuple represents a pairing between characters
            No particular ordering is assumed
        """
        if self._pairings is None:
            pairings = self._get_details()[3].strip()

            if 'Chapters: ' in pairings or '[' not in pairings:
                self._pairings = []

            # We know there are either one or two pairings at this point
            else:

                # In this case, there are two pairings
                if '] [' in pairings:
                    characters = pairings.replace('] [', ', ').split(', ')
                    self._pairings = [(characters[0].replace('[', ''), characters[1]),
                                      (characters[2], characters[3].replace(']', ''))]

                # There is one pairing, and it is listed first
                else:
                    characters = pairings.replace('] ', ', ').split(', ')
                    self._pairings = [(characters[0].replace('[', ''), characters[1])]

        return self._pairings

    def get_chapters(self):
        """
        Returns:
            int: The number of chapters in the fanfic
        """
        if not self._chapters:
            chapter_index = 4
            if len(self.get_characters()) == 0:
                chapter_index = 3

            chapters = self._get_details()[chapter_index][len("Chapters: "):]
            self._chapters = int(chapters.replace(',', ''))
        return self._chapters

    def get_word_count(self):
        """
        Returns:
            int: The number of words in the fanfic
        """
        if not self._word_count:
            self._word_count = self._get_count('Words: ')

        return self._word_count

    def get_reviews(self):
        """
        Returns:
            int: The number of reviews the fanfic has
        """
        if not self._reviews:
            self._reviews = self._get_count('Reviews: ')

        return self._reviews

    def get_favorites(self):
        """
        Returns:
            int: The number of favorites the fanfic has
        """
        if not self._favorites:
            self._favorites = self._get_count('Favs: ')

        return self._favorites

    def get_follows(self):
        """
        Returns:
            int: The number of people following the fanfic
        """
        if not self._follows:
            self._follows = self._get_count('Follows: ')

        return self._follows

    def get_published_date(self):
        """
        Returns:
            Date: The date the fanfic was published

        (Note: This function has the side-effect of initializing the date the fanfic was updated)
        """
        if not self._published:
            date_key = 'data-xutime'
            dates = [date for date in self._html.find_all('span') if date.has_attr(date_key)]
            if self._get_details()[-3].startswith('Updated: '):
                self._updated = datetime.date.fromtimestamp(int(dates[0][date_key]))
                self._published = datetime.date.fromtimestamp(int(dates[1][date_key]))
            else:
                self._updated = self._published = datetime.date.fromtimestamp(int(dates[0][date_key]))
        return self._published

    def get_updated_date(self):
        """
        Returns:
            Date: The date the fanfic was updated.
                  This is equal to get_published() if the fic was never updated

        (Note: This function has the side-effect of initializing the date the fanfic was published)
        """
        if not self._updated:
            self.get_published_date()  # this will initialized self._updated
        return self._updated

    def get_id(self):
        """
        Returns:
            int: Fanfiction.net's id for the fanfic
        """
        if not self._id:
            self._id = self._get_count('id: ')

        return self._id

    def _get_count(self, prefix):
        """
        Convert a string of the form "String 123,345" to the ending number
        This needs to occur in the fanfic's information string

        Args:
            prefix (str): The substring that precedes the desired number
                          Example: "Words: "
        Returns:
            int: The number after the given prefix
        """
        candidates = [x for x in self._get_details() if x.startswith(prefix)]
        if len(candidates) == 0:
            return 0
        return int(candidates[0][len(prefix):].replace(',', ''))

    def get_reviews_url(self):
        return urls.fanfiction_base_url + '/r/' + str(self.get_id()) + '/'

    def get_reviews_dict(self, chapter=0):

        chapter_key = '/' + str(chapter) + '/'
        url = self.get_reviews_url()
        review_dict = {}
        links = BeautifulSoup(requests.get(url).text, parse_only=SoupStrainer('a'))
        num_pages = int([link for link in links if link.string and link.string.startswith('Last')][0]['href'].
                        split('/')[-2].
                        replace(',', ''))

        for i in range(num_pages):
            next_page = urls.fanfiction_base_url + '/r/' + str(self.get_id()) + chapter_key + str(i + 1) + '/'
            links = BeautifulSoup(requests.get(next_page).text).find_all('a')

            users = [link for link in links if link['href'].startswith('/u/')]

            if len(users) == 0:
                return None

            for user in users:
                if user.text in review_dict:
                    review_dict[user.text] += 1
                else:
                    review_dict[user.text] = 1

        return review_dict

