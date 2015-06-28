__author__ = 'jwsm'

from bs4 import BeautifulSoup
import requests
from src import urls, listing


class BetaList(listing.Listing):

    def __init__(self, url, html=None):
        """
        Construct a BetaList from a url. The html parameter is intended for testing.

        Args:
            url (string): url of the desired beta list
        """
        super().__init__(url, html)

        # Necessary source for scraping filters disappears when they're set,
        # So we need the source for a page in the listing with no filters set
        base_url = urls.remove_params(self._url)
        if base_url == self._url:
            self._base_html = self._html
        else:
            self._base_html = BeautifulSoup(requests.get(base_url).text)

        self._param_keys = {
            'beta_languageid': 'languageid',
            'beta_genreid': 'genreid',
            'beta_rating': 'rating',
        }
        self._page_key = 'ppage'
        self._params = {'ppage': self.current_page_number()}

    def languages(self):
        """
        Returns:
            {str: str} Possible values for language filter
        """
        return self._get_filter_options('beta_languageid')

    def genres(self):
        """
        Returns:
            {str: str} Possible values for genre filter
        """
        return self._get_filter_options('beta_genreid')

    def ratings(self):
        """
            {str: str} Possible values for ratings filter
        """
        return self._get_filter_options('beta_rating')

    def set_language_filter(self, language):
        """
        Set the language filter

        Args:
            language (str): The desired language
        """
        self._set_filter('beta_languageid', language)

    def set_genre_filter(self, genre):
        """
        Set the genre filter

        Args:
            genre (str): The desired genre
        """
        self._set_filter('beta_genreid', genre)

    def set_rating_filter(self, rating):
        """
        Set the rating filter

        Args:
            rating (str): The desired rating. '>>' may be used instead of '»'
        """
        rating = BetaList.translate_rating(rating)
        self._set_filter('beta_rating', rating)

    @staticmethod
    def translate_rating(rating):
        """
        The workings are obvious
        """
        return rating.replace('>>', '»')

    '''
    def build_filtered_url(self):
        """
        Return the url specified by the desired filters

        Returns:
            str: new url
        """
        url = self._url

        url = urls.remove_params(url) + '?'

        for param in self._params.keys():
            url += '&' + param + '=' + self._params[param]

        self._url = url
        return self._url
    '''


