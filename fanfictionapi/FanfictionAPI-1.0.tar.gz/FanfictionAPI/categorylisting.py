__author__ = 'jwsm'

from FanfictionAPI import urls
from FanfictionAPI.listing import Listing


class CategoryListing(Listing):
    """
    Represents a category, as found at http://www.fanfiction.net/medium/category
    Do not access member variables directly
    """

    def __init__(self, url, html=None):
        """
        Construct a category from its url. The html arg is intended for testing purposes.

        Args:
            url (str): The url of the category to construct
        """
        super().__init__(url, html)
        if urls.classify_url(self._url) != urls.Category:
            print(self._url)
            raise ValueError("Invalid url for CategoryListing object")

        self._param_keys = {
            'censorid': 'r',
            '_genreid1': 'g',
            'timerange': 't',
            'sortid': 'srt',
            'languageid': 'lan',
            'length': 'len',
            'statusid': 's',
            'verseid1': 'v1',
            'characterid1': 'c',
            'withpairing': 'pm',
        }
        self._page_key = 'p'
        self._params = {'p': self.current_page_number()}

    def sort_by_options(self):
        """
        Returns:
            {str: int}: possible values for Sort By filter
        """
        return self._get_filter_options('sortid')

    def time_range_options(self):
        """
        Returns:
            {str: int}: possible values for Time Range filter
        """
        return self._get_filter_options('timerange')

    def genre_options(self):
        """
        Returns:
            {str: int}: possible values for Genre filter
        """
        return self._get_filter_options('_genreid1')

    def ratings(self):
        """
        Returns:
            {str: int}: possible values for Ratings filter
        """
        return self._get_filter_options('censorid')

    def languages(self):
        """
        Returns:
            {str: int}: possible values for Languages filter
        """
        return self._get_filter_options('languageid')

    def length(self):
        """
        Returns:
            {str: int}: possible values for Length filter
        """
        return self._get_filter_options('length')

    def status(self):
        """
        Returns:
            {str: int}: possible values for Status filter
        """
        return self._get_filter_options('statusid')

    def worlds(self):
        """
        Returns:
            {str: int}: possible values for Worlds filter
        """
        return self._get_filter_options('verseid1')

    def characters(self):
        """
        Returns:
            {str: int}: possible values for Characters filter
        """
        chars = self._get_filter_options('characterid1')
        chars[0] = chars[0][:-4].strip()
        return chars

    def set_sorting_method(self, option):
        """
        Set the Sort By filter

        Args:
            option (str): the name of the sorting method to use
        """
        self._set_filter('sortid', option)

    def set_time_range(self, option):
        """
        Set the Time Range filter

        Args:
            option (str): the name of the time range to use
        """
        self._set_filter('timerange', option)

    def set_genre_filter(self, genre, selection, with_filter=True):
        """
        Set the Genre filter
        If with_filter is False, selection must be None.

        Args:
            genre (str): the name of the genre to use
            selection (str): 'A' or 'B', to select the appropriate genre filter
            with_filter (boolean): if True, sets With filter. If False, sets Without filter
        """
        if selection != 'A' and selection != 'B':
            raise ValueError('selection arg should be \'A\' or \'B\'')

        if selection and not with_filter:
            raise ValueError('Without Genre filter has only one option')

        self._set_filter('_genreid1', genre, selection, with_filter)

    def set_rating_filter(self, rating):
        """
        Set the Rating filter

        Args:
            rating (str): the ratings to include
        """
        self._set_filter('censorid', rating)

    def set_language_filter(self, language):
        """
        Set the Language filter

        Args:
            language (str): the language to include
        """
        self._set_filter('languageid', language)

    def set_length_filter(self, length):
        """
        Set the Length filter

        Args:
            length (str): the length to use
        """
        self._set_filter('length', length)

    def set_status_filter(self, status):
        """
        Set the Status filter

        Args:
            status (str): the length to use
        """
        self._set_filter('statusid', status)

    def set_world_filter(self, world, with_filter=True):
        """
        Set the World filter

        Args:
            world (str): the world to use
            with_filter (boolean): if True, sets With filter. Else: sets Without filter
        """
        self._set_filter('verseid1', world, None, with_filter)

    def set_character_filter(self, character, selection, with_filter=True):
        """
        Set the Character filter
        if with_filter is False, selection must be 'A' or 'B'

        Args:
            character (str): the name of the character to use
            selection (str): 'A', 'B', 'C', or 'D', to select the appropriate filter
            with_filter (boolean): if True, sets With filter. Else, sets Without filter
        """
        if selection not in ['A', 'B', 'C', 'D']:
            raise ValueError("Character selection must be 'A', 'B', 'C', or 'D'")
        if not with_filter:
            if selection not in ['A', 'B']:
                raise ValueError('Character filter only has two options')

        self._set_filter('characterid1', character, selection, with_filter)

    def set_with_pairing_filter(self, setting, with_filter=True):
        """
        Set the With_pairing filter

        Args:
            setting (Boolean): if True, filter is set. If False, turned off
            with_filter (Boolean): if True, With filter is used, If False, Without filter is used
        """
        key = 'pm'

        if not with_filter:
            key = '_' + key

        if setting is True:
            self._params[key] = '1'
        else:
            self._params.pop(key, None)

    def build_filtered_url(self):
        """
        Get the new url, based on all the applied filters

        Returns:
            str: category url
        """

        url = urls.remove_params(self._url) + '?'

        for param in self._params.keys():
            url += '&' + param + '=' + self._params[param]

        self._url = url
        return url

    def clear_filters(self):
        """
        Remove all filters, except for page number
        """
        self._params = {'p': str(self.current_page_number())}
