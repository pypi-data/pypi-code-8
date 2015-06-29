import requests

from bs4 import BeautifulSoup
from FanfictionAPI import urls


class Listing(object):
    def __init__(self, url, html=None):
        self._url = urls.normalize_url(url)

        if html:
            self._html = BeautifulSoup(html)
        else:
            self._html = BeautifulSoup(requests.get(self._url).text)

        self._num_pages = None
        self._current_page = None
        self._page_key = None
        self._params = None
        self._filters = {}
        self._param_keys = {}

    def num_pages(self):
        """
        Find the number of pages in the category

        Returns:
            int: Number of pages in the category
        """
        if not self._num_pages:
            nav_bar = self._html.find('center')

            # if there are no links to more pages
            if nav_bar is None:
                self._num_pages = 1
                return self._num_pages

            last_url = nav_bar.find('a', text='Last')

            # there is no link to 'Last'
            if last_url is None:
                self._num_pages = 2
                return self._num_pages

            self._num_pages = urls.extract_page_number(last_url['href'], self._page_key)
        return self._num_pages

    def current_page_number(self):
        """
        Get the number of the current page.

        Returns:
            int: page number
        """
        if not self._current_page:
            self._current_page = urls.extract_page_number(self._url, self._page_key)
        return self._current_page

    def next_page(self):
        """
        Get the next page in the category, or None if on the last page

        Returns:
            CategoryListing: next page in category
        """
        if self.current_page_number() == self.num_pages():
            return None
        return self.get_page(self.current_page_number() + 1)

    def previous_page(self):
        """
        Get the previous page in the category, or None if on the first page

        Returns:
            CategoryListing: previous page in the category
        """
        if self.current_page_number() == 1:
            return None
        return self.get_page(self.current_page_number() - 1)

    def get_page(self, page_number):
        """
        Get an arbitrary page in a category, given the page number

        Args:
            page_number (int): number of the desired page

        Returns:
            CategoryListing: the desired page
        """

        self._params[self._page_key] = page_number
        new_url = self.build_filtered_url()

        return type(self)(new_url)

    def build_filtered_url(self):
        """
        Get the new url, based on all the applied filters

        Returns:
            str: category url
        """

        url = urls.remove_params(self._url) + '?'

        for param in self._params.keys():
            url += '&' + param + '=' + str(self._params[param])

        self._url = url
        return url

    def _get_filter_options(self, filter_name):
        """
        Scrape what values a given filter can take

        Example output:
        {'Rating: All': 10,
         '(? Ratings Guide)': -1,
         'Rated K -> T': 102,
        }

        Args:
            filter_name (str): name of filter, as used by fanfiction.net source

        Returns:
            {str: str}: Mapping from filter value to corresponding url query param argument
        """
        if filter_name not in self._filters:
            options = self._html.find(attrs={'name': filter_name}).contents[1:]
            values = self._get_param_args(options)
            self._filters[filter_name] = values

        return self._filters[filter_name]

    def _set_filter(self, filter_name, option, selection=None, with_filter=True):
        """
        Set a filter for the CategoryListing by modifying the query params

        Args:
            filter_name (str): The name of the filter to set, as used in fanfiction.net's source
            option (str): The value that the filter should take. Possibly options may be found by calling
                          the appropriate accessor method
            selection (str): 'A', 'B', 'C', or 'D'. Which option to set
            with_filter (boolean): if True, method will set the With filter. If not, method will set the
                                   Without filter
        """
        selection_dict = {
            'A': '1',
            'B': '2',
            'C': '3',
            'D': '4',
        }

        if option not in self._get_filter_options(filter_name):
            raise ValueError('%s is not recognized' % option)

        key = self._param_keys[filter_name]

        if not with_filter:
            key = '_' + key

        if selection:
            key += selection_dict[selection]

        self._params[key] = self._get_filter_options(filter_name)[option]

    @staticmethod
    def _get_param_args(options):
        """
        Find which values a filter can take

        Args:
            options (BeautifulSoup?): a parsed <SELECT> tag with desired format and values

        Returns:
            {str: str}: each possible value as a key, its corresponding url code as the value
        """
        args = {}
        for option in options:

            number = option['value'].replace(',', '')
            value = option.text.replace('\n', '')

            #Remove parens?
            if value[-1] == ')':
                right_paren_location = -1 * (len(value) - value.rfind('('))
                value = value[:right_paren_location].strip()

            args[value] = number

        return args

